#include "adb_rpc_protocol.h"
#include <sstream>
#include <regex>

namespace edgeai {
namespace android {

// Simple robust JSON serializer & parser (dependency-free C++)
static std::string ExtractJsonField(const std::string& json, const std::string& key) {
    std::regex re("\"" + key + "\"\\s*:\\s*\"([^\"]*)\"");
    std::smatch match;
    if (std::regex_search(json, match, re) && match.size() > 1) {
        return match[1].str();
    }
    return "";
}

static int ExtractJsonInt(const std::string& json, const std::string& key, int default_val) {
    std::regex re("\"" + key + "\"\\s*:\\s*([0-9]+)");
    std::smatch match;
    if (std::regex_search(json, match, re) && match.size() > 1) {
        return std::stoi(match[1].str());
    }
    return default_val;
}

static bool ExtractJsonBool(const std::string& json, const std::string& key, bool default_val) {
    std::regex re("\"" + key + "\"\\s*:\\s*(true|false)");
    std::smatch match;
    if (std::regex_search(json, match, re) && match.size() > 1) {
        return match[1].str() == "true";
    }
    return default_val;
}

std::string ADBRPCProtocol::SerializeRequest(const ChatRPCRequest& req) {
    std::ostringstream ss;
    ss << "{\n"
       << "  \"request_id\": \"" << req.request_id << "\",\n"
       << "  \"device_target\": \"" << req.device_target << "\",\n"
       << "  \"prompt\": \"" << req.prompt << "\",\n"
       << "  \"system_instruction\": \"" << req.system_instruction << "\",\n"
       << "  \"max_tokens\": " << req.max_tokens << ",\n"
       << "  \"temperature\": " << req.temperature << ",\n"
       << "  \"use_npu\": " << (req.use_npu ? "true" : "false") << ",\n"
       << "  \"stream\": " << (req.stream ? "true" : "false") << "\n"
       << "}";
    return ss.str();
}

ChatRPCRequest ADBRPCProtocol::DeserializeRequest(const std::string& json_str) {
    ChatRPCRequest req;
    req.request_id = ExtractJsonField(json_str, "request_id");
    req.device_target = ExtractJsonField(json_str, "device_target");
    req.prompt = ExtractJsonField(json_str, "prompt");
    req.system_instruction = ExtractJsonField(json_str, "system_instruction");
    req.max_tokens = ExtractJsonInt(json_str, "max_tokens", 256);
    req.use_npu = ExtractJsonBool(json_str, "use_npu", true);
    req.stream = ExtractJsonBool(json_str, "stream", false);
    return req;
}

std::string ADBRPCProtocol::SerializeResponse(const ChatRPCResponse& res) {
    std::ostringstream ss;
    ss << "{\n"
       << "  \"request_id\": \"" << res.request_id << "\",\n"
       << "  \"device_target\": \"" << res.device_target << "\",\n"
       << "  \"generated_text\": \"" << res.generated_text << "\",\n"
       << "  \"status_ok\": " << (res.status_ok ? "true" : "false") << ",\n"
       << "  \"error_message\": \"" << res.error_message << "\",\n"
       << "  \"time_to_first_token_ms\": " << res.time_to_first_token_ms << ",\n"
       << "  \"tokens_per_second\": " << res.tokens_per_second << ",\n"
       << "  \"generated_tokens\": " << res.generated_tokens << ",\n"
       << "  \"backend_name\": \"" << res.backend_name << "\"\n"
       << "}";
    return ss.str();
}

ChatRPCResponse ADBRPCProtocol::DeserializeResponse(const std::string& json_str) {
    ChatRPCResponse res;
    res.request_id = ExtractJsonField(json_str, "request_id");
    res.device_target = ExtractJsonField(json_str, "device_target");
    res.generated_text = ExtractJsonField(json_str, "generated_text");
    res.status_ok = ExtractJsonBool(json_str, "status_ok", true);
    res.error_message = ExtractJsonField(json_str, "error_message");
    res.backend_name = ExtractJsonField(json_str, "backend_name");
    res.generated_tokens = ExtractJsonInt(json_str, "generated_tokens", 0);
    return res;
}

} // namespace android
} // namespace edgeai
