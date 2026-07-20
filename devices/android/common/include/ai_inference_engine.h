#ifndef EDGE_AI_AI_INFERENCE_ENGINE_H
#define EDGE_AI_AI_INFERENCE_ENGINE_H

#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <cstdint>

namespace edgeai {
namespace android {

enum class HardwareBackend {
    CPU_NEON,
    GPU_VULKAN,
    GPU_OPENCL,
    NPU_TENSOR_TPU,
    AICORE_GEMINI_NANO
};

struct InferenceConfig {
    std::string model_path;
    HardwareBackend backend{HardwareBackend::CPU_NEON};
    int32_t max_tokens{256};
    float temperature{0.7f};
    float top_p{0.9f};
    int32_t threads{4};
    bool verbose_telemetry{true};
};

struct InferenceMetrics {
    double time_to_first_token_ms{0.0};
    double tokens_per_second{0.0};
    int32_t prompt_tokens{0};
    int32_t generated_tokens{0};
    uint64_t memory_used_bytes{0};
    std::string backend_used;
};

struct InferenceResponse {
    std::string request_id;
    std::string text;
    bool status_ok{true};
    std::string error_message;
    InferenceMetrics metrics;
};

using TokenCallback = std::function<void(const std::string& token)>;

class AIInferenceEngine {
public:
    virtual ~AIInferenceEngine() = default;

    virtual bool Initialize(const InferenceConfig& config) = 0;
    virtual InferenceResponse Generate(const std::string& prompt, TokenCallback callback = nullptr) = 0;
    virtual std::string GetDeviceName() const = 0;
    virtual HardwareBackend GetActiveBackend() const = 0;
    virtual bool IsNPUAvailable() const = 0;
};

// Engine Factory
class EngineFactory {
public:
    static std::unique_ptr<AIInferenceEngine> CreateEngine(const std::string& device_model);
};

} // namespace android
} // namespace edgeai

#endif // EDGE_AI_AI_INFERENCE_ENGINE_H
