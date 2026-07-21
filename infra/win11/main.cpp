#include <iostream>

extern void edge_ai_init();

int main(int argc, char** argv) {
    std::cout << "======================================================" << std::endl;
    std::cout << " edge-ai Native Windows 11 Build Target" << std::endl;
    std::cout << "======================================================" << std::endl;
    edge_ai_init();
    std::cout << "[edge-ai] Execution finished cleanly." << std::endl;
    return 0;
}
