#include <jni.h>
#include <string>
#include <android/log.h>
#include "ai_inference_engine.h"

#define LOG_TAG "Pixel10NativeEngine"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_edgeai_pixel10proxl_engine_Pixel10ProXLInferenceEngine_nativeGenerate(
        JNIEnv* env,
        jobject /* this */,
        jstring promptObj,
        jboolean useNpu) {

    const char* promptCStr = env->GetStringUTFChars(promptObj, nullptr);
    std::string prompt(promptCStr ? promptCStr : "");
    if (promptCStr) env->ReleaseStringUTFChars(promptObj, promptCStr);

    LOGI("Processing prompt on Pixel 10 Pro XL (Tensor G5 / Gemini Nano TPU v5): %s [NPU=%d]", prompt.c_str(), useNpu);

    auto engine = edgeai::android::EngineFactory::CreateEngine("Pixel10ProXL");
    edgeai::android::InferenceConfig config;
    config.backend = useNpu ? edgeai::android::HardwareBackend::AICORE_GEMINI_NANO : edgeai::android::HardwareBackend::CPU_NEON;
    engine->Initialize(config);

    auto response = engine->Generate(prompt);
    return env->NewStringUTF(response.text.c_str());
}
