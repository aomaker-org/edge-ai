package com.edgeai.pixel10proxl.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.edgeai.pixel10proxl.engine.Pixel10ProXLInferenceEngine

data class ChatMessage(
    val sender: String,
    val text: String,
    val isUser: Boolean,
    val metrics: String? = null
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(deviceName: String) {
    var messages by remember { mutableStateOf(listOf(
        ChatMessage("System", "Pixel 10 Pro XL (Tensor G5 Laguna) Gemini Nano / AICore NPU Engine Initialized. ADB Bridge running on port 8080.", false)
    )) }
    var inputText by remember { mutableStateOf("") }
    var useNpu by remember { mutableStateOf(true) }
    var isGenerating by remember { mutableStateOf(false) }

    val engine = remember { Pixel10ProXLInferenceEngine() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(deviceName, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Tensor G5 TPU v5 • Gemini Nano v3 • 16GB LPDDR5X", fontSize = 12.sp, color = Color.LightGray)
                    }
                },
                actions = {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(end = 8.dp)
                    ) {
                        Text("NPU", fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Bold)
                        Switch(
                            checked = useNpu,
                            onCheckedChange = { useNpu = it },
                            colors = SwitchDefaults.colors(checkedThumbColor = MaterialTheme.colorScheme.primary)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            LazyColumn(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                reverseLayout = false
            ) {
                items(messages) { msg ->
                    ChatBubble(msg)
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }

            if (isGenerating) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp))
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = inputText,
                    onValueChange = { inputText = it },
                    placeholder = { Text("Ask Pixel 10 Pro XL Gemini Nano...") },
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(24.dp),
                    enabled = !isGenerating
                )
                Spacer(modifier = Modifier.width(8.dp))
                Button(
                    onClick = {
                        if (inputText.isNotBlank() && !isGenerating) {
                            val userPrompt = inputText
                            inputText = ""
                            messages = messages + ChatMessage("User", userPrompt, true)
                            isGenerating = true

                            engine.generateAsync(userPrompt, useNpu) { responseText, metricsStr ->
                                messages = messages + ChatMessage("Pixel10 Bot", responseText, false, metricsStr)
                                isGenerating = false
                            }
                        }
                    },
                    enabled = !isGenerating && inputText.isNotBlank(),
                    shape = RoundedCornerShape(24.dp)
                ) {
                    Text("Send")
                }
            }
        }
    }
}

@Composable
fun ChatBubble(message: ChatMessage) {
    val backgroundColor = if (message.isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer
    val alignment = if (message.isUser) Alignment.End else Alignment.Start

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = alignment
    ) {
        Box(
            modifier = Modifier
                .widthIn(max = 290.dp)
                .background(backgroundColor, shape = RoundedCornerShape(16.dp))
                .padding(12.dp)
        ) {
            Column {
                Text(
                    text = message.sender,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Gray
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(text = message.text, fontSize = 14.sp)
                if (message.metrics != null) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = message.metrics,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
}
