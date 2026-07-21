#include "ai_inference_engine.h"
#include "adb_rpc_protocol.h"
#include <iostream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    std::string prompt = "Explain on-device mobile AI acceleration on Tensor G1.";
    std::string backend_str = "vulkan";

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if ((arg == "--prompt" || arg == "-p") && i + 1 < argc) {
            prompt = argv[++i];
        } else if ((arg == "--backend" || arg == "-b") && i + 1 < argc) {
            backend_str = argv[++i];
        }
    }

    std::cout << "==================================================================" << std::endl;
    std::cout << " Pixel 6a (Tensor G1) Native Inference CLI Testbed" << std::endl;
    std::cout << " Device Architecture: 2x Cortex-X1 + 2x A78 + 4x A55 | Arm Mali-G78 MP20" << std::endl;
    std::cout << " Target Backend: " << backend_str << std::endl;
    std::cout << "==================================================================" << std::endl;

    auto engine = edgeai::android::EngineFactory::CreateEngine("Pixel6a");
    
    edgeai::android::InferenceConfig config;
    config.backend = edgeai::android::HardwareBackend::GPU_VULKAN;
    config.max_tokens = 256;
    config.temperature = 0.7f;

    if (!engine->Initialize(config)) {
        std::cerr << "[Pixel6a CLI] Error initializing engine!" << std::endl;
        return 1;
    }

    std::cout << "\n[Prompt] " << prompt << std::endl;
    std::cout << "[Inference Output] ";

    auto response = engine->Generate(prompt, [](const std::string& token) {
        std::cout << token << std::flush;
    });

    std::cout << "\n\n--- Performance Metrics ---" << std::endl;
    std::cout << " Status: " << (response.status_ok ? "SUCCESS" : "FAILED") << std::endl;
    std::cout << " Backend: " << response.metrics.backend_used << std::endl;
    std::cout << " Time to First Token (TTFT): " << response.metrics.time_to_first_token_ms << " ms" << std::endl;
    std::cout << " Generation Speed: " << response.metrics.tokens_per_second << " tokens/sec" << std::endl;
    std::cout << " Total Generated Tokens: " << response.metrics.generated_tokens << std::endl;
    std::cout << " Memory Footprint: " << (response.metrics.memory_used_bytes / (1024 * 1024)) << " MB" << std::endl;
    std::cout << "==================================================================" << std::endl;

    return 0;
}
