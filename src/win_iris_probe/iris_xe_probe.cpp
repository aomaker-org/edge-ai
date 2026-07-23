// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "=======================================================================


[200~cat << 'EOF' > ~/src/edge-ai/src/win_iris_probe/iris_xe_probe.cpp
// =============================================================================
// WIN11 DIRECT HARDWARE PROBE: Intel Iris Xe iGPU (12th Gen Intel Core)
// File: src/win_iris_probe/iris_xe_probe.cpp
// Description: Queries DXGI properties AND executes an OpenCL compute kernel
//              directly on Intel Iris Xe Execution Units via OpenCL.dll.
// =============================================================================

#include <windows.h>
#include <dxgi1_6.h>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

#pragma comment(lib, "dxgi.lib")

// --- OpenCL Dynamic Types & Constants ---
typedef int32_t cl_int;
typedef uint32_t cl_uint;
typedef uint64_t cl_ulong;
typedef void* cl_platform_id;
typedef void* cl_device_id;
typedef void* cl_context;
typedef void* cl_command_queue;
typedef void* cl_mem;
typedef void* cl_program;
typedef void* cl_kernel;
typedef uintptr_t cl_mem_flags;
typedef uintptr_t cl_properties;

#define CL_SUCCESS 0
#define CL_PLATFORM_NAME 0x0902
#define CL_DEVICE_NAME 0x102B
#define CL_DEVICE_TYPE_GPU (1 << 2)
#define CL_MEM_READ_ONLY (1 << 2)
#define CL_MEM_WRITE_ONLY (1 << 1)
#define CL_MEM_COPY_HOST_PTR (1 << 5)

// Win32 Dynamic Function Pointers for OpenCL.dll
typedef cl_int (APIENTRY *pfn_clGetPlatformIDs)(cl_uint, cl_platform_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetPlatformInfo)(cl_platform_id, cl_uint, size_t, void*, size_t*);
typedef cl_int (APIENTRY *pfn_clGetDeviceIDs)(cl_platform_id, cl_ulong, cl_uint, cl_device_id*, cl_uint*);
typedef cl_int (APIENTRY *pfn_clGetDeviceInfo)(cl_device_id, cl_uint, size_t, void*, size_t*);
typedef cl_context (APIENTRY *pfn_clCreateContext)(const cl_properties*, cl_uint, const cl_device_id*, void*, void*, cl_int*);
typedef cl_command_queue (APIENTRY *pfn_clCreateCommandQueue)(cl_context, cl_device_id, cl_ulong, cl_int*);
typedef cl_mem (APIENTRY *pfn_clCreateBuffer)(cl_context, cl_mem_flags, size_t, void*, cl_int*);
typedef cl_program (APIENTRY *pfn_clCreateProgramWithSource)(cl_context, cl_uint, const char**, const size_t*, cl_int*);
typedef cl_int (APIENTRY *pfn_clBuildProgram)(cl_program, cl_uint, const cl_device_id*, const char*, void*, void*);
typedef cl_kernel (APIENTRY *pfn_clCreateKernel)(cl_program, const char*, cl_int*);
typedef cl_int (APIENTRY *pfn_clSetKernelArg)(cl_kernel, cl_uint, size_t, const void*);
typedef cl_int (APIENTRY *pfn_clEnqueueWriteBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, const void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueNDRangeKernel)(cl_command_queue, cl_kernel, cl_uint, const size_t*, const size_t*, const size_t*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clEnqueueReadBuffer)(cl_command_queue, cl_mem, unsigned int, size_t, size_t, void*, cl_uint, const void*, void*);
typedef cl_int (APIENTRY *pfn_clFinish)(cl_command_queue);

std::string WideToNarrow(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), static_cast<int>(wstr.size()), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void PrintHeader(const std::string& title) {
    std::cout << "\n========================================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "========================================================================\n";
}

void RunOpenCLBenchmark() {
    PrintHeader("OPENCL COMPUTE KERNEL EXECUTION (IRIS XE EUs)");

    HMODULE hCL = LoadLibraryA("OpenCL.dll");
    if (!hCL) {
        std::cout << "  [NOTICE] OpenCL.dll not found in System32. Skipping OpenCL kernel test.\n";
        return;
    }

    pfn_clGetPlatformIDs clGetPlatformIDs_ptr = (pfn_clGetPlatformIDs)GetProcAddress(hCL, "clGetPlatformIDs");
    pfn_clGetDeviceIDs clGetDeviceIDs_ptr = (pfn_clGetDeviceIDs)GetProcAddress(hCL, "clGetDeviceIDs");
    pfn_clGetDeviceInfo clGetDeviceInfo_ptr = (pfn_clGetDeviceInfo)GetProcAddress(hCL, "clGetDeviceInfo");
    pfn_clCreateContext clCreateContext_ptr = (pfn_clCreateContext)GetProcAddress(hCL, "clCreateContext");
    pfn_clCreateCommandQueue clCreateCommandQueue_ptr = (pfn_clCreateCommandQueue)GetProcAddress(hCL, "clCreateCommandQueue");
    pfn_clCreateBuffer clCreateBuffer_ptr = (pfn_clCreateBuffer)GetProcAddress(hCL, "clCreateBuffer");
    pfn_clCreateProgramWithSource clCreateProgramWithSource_ptr = (pfn_clCreateProgramWithSource)GetProcAddress(hCL, "clCreateProgramWithSource");
    pfn_clBuildProgram clBuildProgram_ptr = (pfn_clBuildProgram)GetProcAddress(hCL, "clBuildProgram");
    pfn_clCreateKernel clCreateKernel_ptr = (pfn_clCreateKernel)GetProcAddress(hCL, "clCreateKernel");
    pfn_clSetKernelArg clSetKernelArg_ptr = (pfn_clSetKernelArg)GetProcAddress(hCL, "clSetKernelArg");
    pfn_clEnqueueNDRangeKernel clEnqueueNDRangeKernel_ptr = (pfn_clEnqueueNDRangeKernel)GetProcAddress(hCL, "clEnqueueNDRangeKernel");
    pfn_clEnqueueReadBuffer clEnqueueReadBuffer_ptr = (pfn_clEnqueueReadBuffer)GetProcAddress(hCL, "clEnqueueReadBuffer");
    pfn_clFinish clFinish_ptr = (pfn_clFinish)GetProcAddress(hCL, "clFinish");

    if (!clGetPlatformIDs_ptr || !clGetDeviceIDs_ptr || !clCreateContext_ptr) {
        std::cout << "  [ERROR] Failed to resolve essential OpenCL function pointers.\n";
        FreeLibrary(hCL);
        return;
    }

    cl_uint num_platforms = 0;
    clGetPlatformIDs_ptr(0, NULL, &num_platforms);
    if (num_platforms == 0) {
        std::cout << "  [NOTICE] No OpenCL platforms registered.\n";
        FreeLibrary(hCL);
        return;
    }

    std::vector<cl_platform_id> platforms(num_platforms);
    clGetPlatformIDs_ptr(num_platforms, platforms.data(), NULL);

    cl_device_id target_device = NULL;
    char dev_name[256] = {0};

    for (size_t i = 0; i < platforms.size(); ++i) {
        cl_uint num_devices = 0;
        if (clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, 0, NULL, &num_devices) == CL_SUCCESS && num_devices > 0) {
            std::vector<cl_device_id> devices(num_devices);
            clGetDeviceIDs_ptr(platforms[i], CL_DEVICE_TYPE_GPU, num_devices, devices.data(), NULL);
            target_device = devices[0];
            if (clGetDeviceInfo_ptr) {
                clGetDeviceInfo_ptr(target_device, CL_DEVICE_NAME, sizeof(dev_name), dev_name, NULL);
            }
            break;
        }
    }

    if (!target_device) {
        std::cout << "  [NOTICE] No GPU OpenCL devices found.\n";
        FreeLibrary(hCL);
        return;
    }

    std::cout << "  OpenCL Compute Device : " << dev_name << "\n";

    cl_int err = 0;
    cl_context context = clCreateContext_ptr(NULL, 1, &target_device, NULL, NULL, &err);
    cl_command_queue queue = clCreateCommandQueue_ptr(context, target_device, 0, &err);

    // Single-line string literal to eliminate MSVC line-ending parsing issues
    const char* kernel_src = "__kernel void vec_add(__global const float* A, __global const float* B, __global float* C, const int N) { int id = get_global_id(0); if (id < N) { C[id] = A[id] + B[id]; } }\n";

    cl_program program = clCreateProgramWithSource_ptr(context, 1, &kernel_src, NULL, &err);
    err = clBuildProgram_ptr(program, 1, &target_device, NULL, NULL, NULL);
    cl_kernel kernel = clCreateKernel_ptr(program, "vec_add", &err);

    const int N = 1024;
    size_t bytes = N * sizeof(float);
    std::vector<float> h_A(N), h_B(N), h_C(N, 0.0f);

    for (int i = 0; i < N; ++i) {
        h_A[i] = static_cast<float>(i) * 1.0f;
        h_B[i] = static_cast<float>(i) * 2.0f;
    }

    cl_mem d_A = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_A.data(), &err);
    cl_mem d_B = clCreateBuffer_ptr(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, bytes, h_B.data(), &err);
    cl_mem d_C = clCreateBuffer_ptr(context, CL_MEM_WRITE_ONLY, bytes, NULL, &err);

    clSetKernelArg_ptr(kernel, 0, sizeof(cl_mem), &d_A);
    clSetKernelArg_ptr(kernel, 1, sizeof(cl_mem), &d_B);
    clSetKernelArg_ptr(kernel, 2, sizeof(cl_mem), &d_C);
    clSetKernelArg_ptr(kernel, 3, sizeof(int), &N);

    size_t global_work_size = N;
    auto start_time = std::chrono::high_resolution_clock::now();

    clEnqueueNDRangeKernel_ptr(queue, kernel, 1, NULL, &global_work_size, NULL, 0, NULL, NULL);
    clFinish_ptr(queue);

    auto elapsed = std::chrono::high_resolution_clock::now() - start_time;
    double microsec = std::chrono::duration<double, std::micro>(elapsed).count();

    clEnqueueReadBuffer_ptr(queue, d_C, 1, 0, bytes, h_C.data(), 0, NULL, NULL);

    bool valid = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != (h_A[i] + h_B[i])) {
            valid = false;
            break;
        }
    }

    if (valid) {
        std::cout << "  Kernel Dispatch       : 1,024 Work Items Vector Add (C = A + B)\n";
        std::cout << "  Execution Time        : " << std::fixed << std::setprecision(2) << microsec << " us\n";
        std::cout << "  Verification Check    : PASS (C[0]=" << h_C[0] << ", C[1023]=" << h_C[1023] << ")\n";
    } else {
        std::cout << "  Verification Check    : FAIL (Compute output mismatch)\n";
    }

    FreeLibrary(hCL);
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << " INTEL IRIS XE GRAPHICS DIRECT HARDWARE TELEMETRY PROBE [DEBUG BUILD]\n";
    std::cout << "========================================================================\n";

    IDXGIFactory6* factory = nullptr;
    if (SUCCEEDED(CreateDXGIFactory1(IID_PPV_ARGS(&factory)))) {
        IDXGIAdapter1* adapter = nullptr;
        UINT adapterIndex = 0;
        PrintHeader("DXGI GPU ADAPTER ENUMERATION");

        while (factory->EnumAdapters1(adapterIndex, &adapter) != DXGI_ERROR_NOT_FOUND) {
            DXGI_ADAPTER_DESC1 desc;
            adapter->GetDesc1(&desc);
            std::string gpuName = WideToNarrow(desc.Description);

            std::cout << "\n[Adapter " << adapterIndex << "]\n";
            std::cout << "  Description         : " << gpuName << "\n";
            std::cout << "  Vendor ID           : 0x" << std::hex << desc.VendorId << std::dec;
            if (desc.VendorId == 0x8086) std::cout << " (Intel Corporation)";
            std::cout << "\n  Device ID           : 0x" << std::hex << desc.DeviceId << std::dec << "\n";
            std::cout << "  Shared System Memory: " << (desc.SharedSystemMemory / (1024 * 1024)) << " MB\n";

            adapter->Release();
            adapterIndex++;
        }
        factory->Release();
    }

    RunOpenCLBenchmark();

    std::cout << "\n========================================================================\n";
    return 0;
}
