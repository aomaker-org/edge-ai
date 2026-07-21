#ifndef EDGE_AI_ADB_RPC_PROTOCOL_H
#define EDGE_AI_ADB_RPC_PROTOCOL_H

#include <string>
#include <vector>

namespace edgeai {
namespace android {

struct ChatRPCRequest {
    std::string request_id;
    std::string device_target;
    std::string prompt;
    std::string system_instruction;
    int32_t max_tokens{256};
    float temperature{0.7f};
    bool use_npu{true};
    bool stream{false};
};

struct ChatRPCResponse {
    std::string request_id;
    std::string device_target;
    std::string generated_text;
    bool status_ok{true};
    std::string error_message;
    double time_to_first_token_ms{0.0};
    double tokens_per_second{0.0};
    int32_t generated_tokens{0};
    std::string backend_name;
};

class ADBRPCProtocol {
public:
    static std::string SerializeRequest(const ChatRPCRequest& req);
    static ChatRPCRequest DeserializeRequest(const std::string& json_str);

    static std::string SerializeResponse(const ChatRPCResponse& res);
    static ChatRPCResponse DeserializeResponse(const std::string& json_str);
};

} // namespace android
} // namespace edgeai

#endif // EDGE_AI_ADB_RPC_PROTOCOL_H
