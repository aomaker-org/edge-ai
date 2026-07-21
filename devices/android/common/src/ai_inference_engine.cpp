#include "ai_inference_engine.h"
#include <iostream>
#include <chrono>
#include <thread>
#include <sstream>

namespace edgeai {
namespace android {

class GenericPixelEngine : public AIInferenceEngine {
public:
    explicit GenericPixelEngine(std::string device_name, std::string backend_name, bool npu_avail)
        : device_name_(std::move(device_name)), backend_name_(std::move(backend_name)), npu_available_(npu_avail) {}

    bool Initialize(const InferenceConfig& config) override {
        config_ = config;
        initialized_ = true;
        std::cout << "[" << device_name_ << "] Engine initialized with model: " 
                  << (config.model_path.empty() ? "<embedded_default>" : config.model_path)
                  << " using backend: " << backend_name_ << std::endl;
        return true;
    }

    InferenceResponse Generate(const std::string& prompt, TokenCallback callback) override {
        InferenceResponse res;
        res.request_id = "req_260720_001";
        
        if (!initialized_) {
            res.status_ok = false;
            res.error_message = "Engine not initialized";
            return res;
        }

        auto start_time = std::chrono::high_resolution_clock::now();

        // Simulate prompt processing & generation
        std::ostringstream ss;
        ss << "[" << device_name_ << " Engine / " << backend_name_ << "] Answer to: \"" << prompt << "\" -> ";
        
        std::vector<std::string> simulated_tokens = {
            "On-device ", "inference ", "on ", device_name_, " running ",
            "accelerated ", backend_name_, " backend ", "succeeded. ",
            "Response ", "generated ", "with ", "high ", "efficiency."
        };

        double ttft = 45.2; // ms
        res.metrics.time_to_first_token_ms = ttft;

        for (size_t i = 0; i < simulated_tokens.size(); ++i) {
            ss << simulated_tokens[i];
            if (callback) {
                callback(simulated_tokens[i]);
            }
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        double elapsed_sec = std::chrono::duration<double>(end_time - start_time).count();

        res.text = ss.str();
        res.status_ok = true;
        res.metrics.generated_tokens = static_cast<int32_t>(simulated_tokens.size());
        res.metrics.prompt_tokens = static_cast<int32_t>(prompt.length() / 4);
        res.metrics.tokens_per_second = (elapsed_sec > 0.0) ? (res.metrics.generated_tokens / elapsed_sec) : 48.5;
        res.metrics.backend_used = backend_name_;
        res.metrics.memory_used_bytes = 420 * 1024 * 1024; // 420 MB

        return res;
    }

    std::string GetDeviceName() const override { return device_name_; }
    HardwareBackend GetActiveBackend() const override { return config_.backend; }
    bool IsNPUAvailable() const override { return npu_available_; }

private:
    std::string device_name_;
    std::string backend_name_;
    bool npu_available_{false};
    bool initialized_{false};
    InferenceConfig config_;
};

std::unique_ptr<AIInferenceEngine> EngineFactory::CreateEngine(const std::string& device_model) {
    if (device_model == "Pixel6a") {
        return std::make_unique<GenericPixelEngine>("Pixel 6a (Tensor G1)", "LiteRT GPU / OpenCL", false);
    } else if (device_model == "Pixel10ProXL" || device_model == "Pixel10") {
        return std::make_unique<GenericPixelEngine>("Pixel 10 Pro XL (Tensor G5)", "Gemini Nano / AICore TPU", true);
    }
    return std::make_unique<GenericPixelEngine>("Generic Android Device", "CPU NEON", false);
}

} // namespace android
} // namespace edgeai
