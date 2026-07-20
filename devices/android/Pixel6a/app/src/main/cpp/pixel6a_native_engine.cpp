#include <jni.h>
#include <string>
#include <android/log.h>
#include "ai_inference_engine.h"

#define LOG_TAG "Pixel6aNativeEngine"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_edgeai_pixel6a_engine_Pixel6aInferenceEngine_nativeGenerate(
        JNIEnv* env,
        jobject /* this */,
        jstring promptObj) {

    const char* promptCStr = env->GetStringUTFChars(promptObj, nullptr);
    std::string prompt(promptCStr ? promptCStr : "");
    if (promptCStr) env->ReleaseStringUTFChars(promptObj, promptCStr);

    LOGI("Processing prompt on Pixel 6a (Tensor G1 / Mali-G78 GPU): %s", prompt.c_str());

    auto engine = edgeai::android::EngineFactory::CreateEngine("Pixel6a");
    edgeai::android::InferenceConfig config;
    config.backend = edgeai::android::HardwareBackend::GPU_VULKAN;
    engine->Initialize(config);

    auto response = engine->Generate(prompt);
    return env->NewStringUTF(response.text.c_str());
}
