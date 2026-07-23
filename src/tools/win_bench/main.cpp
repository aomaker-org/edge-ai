#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>

#if defined(_WIN32) || defined(_WIN64)
    #define OS_NAME "Windows (Win64 PE)"
#elif defined(__linux__)
    #define OS_NAME "Linux (Ubuntu ELF)"
#else
    #define OS_NAME "Unknown Target OS"
#endif

int main() {
    std::cout << "================================================================================" << std::endl;
    std::cout << " EDGE-AI DUAL-TARGET CROSS-BOUNDARY BENCHMARK" << std::endl;
    std::cout << " Compiled Target OS : " << OS_NAME << std::endl;
    std::cout << " C++ Standard       : " << __cplusplus << std::endl;
    std::cout << "================================================================================" << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    // Perform 10 Million Iteration Memory & Math Matrix Loop
    const size_t N = 10'000'000;
    std::vector<uint64_t> data(N);
    for (size_t i = 0; i < N; ++i) {
        data[i] = (i * 3) ^ (i >> 2);
    }

    uint64_t sum = std::accumulate(data.begin(), data.end(), 0ULL);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;

    std::cout << " Processing Results :" << std::endl;
    std::cout << "   - Elements Processed : " << N << std::endl;
    std::cout << "   - Checksum Hash     : 0x" << std::hex << sum << std::dec << std::endl;
    std::cout << "   - Execution Time    : " << elapsed.count() << " ms" << std::endl;
    std::cout << "================================================================================" << std::endl;

    return 0;
}
