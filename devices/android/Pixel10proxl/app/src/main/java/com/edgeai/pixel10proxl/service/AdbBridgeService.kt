package com.edgeai.pixel10proxl.service

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import com.edgeai.pixel10proxl.engine.Pixel10ProXLInferenceEngine
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.ServerSocket
import java.net.Socket
import kotlin.concurrent.thread

class AdbBridgeService : Service() {

    private val TAG = "AdbBridgeService"
    private var serverSocket: ServerSocket? = null
    private var isRunning = false
    private val engine = Pixel10ProXLInferenceEngine()

    override fun onCreate() {
        super.onCreate()
        startHttpBridge(8080)
    }

    private fun startHttpBridge(port: Int) {
        isRunning = true
        thread {
            try {
                serverSocket = ServerSocket(port)
                Log.i(TAG, "ADB Bridge HTTP Server listening on port $port")
                while (isRunning) {
                    val client: Socket = serverSocket?.accept() ?: break
                    handleClient(client)
                }
            } catch (e: Exception) {
                Log.e(TAG, "Server error: ${e.message}")
            }
        }
    }

    private fun handleClient(socket: Socket) {
        thread {
            try {
                val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                val writer = OutputStreamWriter(socket.getOutputStream())

                var line: String? = reader.readLine()
                var contentLength = 0
                while (line != null && line.isNotEmpty()) {
                    if (line.lowercase().startsWith("content-length:")) {
                        contentLength = line.substring(15).trim().toInt()
                    }
                    line = reader.readLine()
                }

                val bodyChars = CharArray(contentLength)
                if (contentLength > 0) {
                    reader.read(bodyChars, 0, contentLength)
                }
                val requestBody = String(bodyChars)

                val prompt = if (requestBody.contains("\"prompt\":")) {
                    requestBody.substringAfter("\"prompt\":").substringAfter("\"").substringBefore("\"")
                } else {
                    "Hello Pixel 10 Pro XL"
                }

                val useNpu = !requestBody.contains("\"use_npu\": false")

                engine.generateAsync(prompt, useNpu) { responseText, metrics ->
                    val jsonResponse = """
                        {
                          "request_id": "req_260720_001",
                          "device_target": "Pixel10ProXL",
                          "generated_text": "$responseText",
                          "status_ok": true,
                          "metrics": "$metrics"
                        }
                    """.trimIndent()

                    writer.write("HTTP/1.1 200 OK\r\n")
                    writer.write("Content-Type: application/json\r\n")
                    writer.write("Content-Length: ${jsonResponse.length}\r\n")
                    writer.write("\r\n")
                    writer.write(jsonResponse)
                    writer.flush()
                    socket.close()
                }
            } catch (e: Exception) {
                Log.e(TAG, "Client handler error: ${e.message}")
            }
        }
    }

    override fun onDestroy() {
        isRunning = false
        serverSocket?.close()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
