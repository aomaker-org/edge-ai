@echo off
REM ==============================================================================
REM Filename:     infra/win11/config_win11.bat
REM Purpose:      Native Windows 11 CMD/Batch Environment Loader for edge-ai
REM Type:         Invoked (cmd.exe /k or call)
REM Attribution:  fekerr & Antigravity (20260720 / Initial Win11 Native Pass)
REM ==============================================================================
REM
REM Usage:
REM   1. Open "Developer Command Prompt for VS 2022" (or VS 2026)
REM   2. Navigate to edge-ai root:  cd /d C:\Users\feker\src\edge-ai
REM   3. Invoke:  call infra\win11\config_win11.bat
REM   4. Optional arguments:
REM        call infra\win11\config_win11.bat force       - Force reload
REM        call infra\win11\config_win11.bat unset       - Tear down env
REM        call infra\win11\config_win11.bat <tag>       - Set prompt tag
REM
REM ==============================================================================

setlocal enabledelayedexpansion

REM ---------------------------------------------------------------
REM 1. Argument Processing
REM ---------------------------------------------------------------
set "_ACTION=%~1"
set "_TAG=%~2"

if /i "%_ACTION%"=="unset" goto :do_unset
if /i "%_ACTION%"=="force" (
    echo [!] Force reload detected. Cycling environment state...
    set "EDGEAI_READY="
    if not "%_TAG%"=="" (
        endlocal & set "EDGEAI_PROMPT_TAG=%_TAG%"
        goto :continue_load
    )
    endlocal
    goto :continue_load
)
if not "%_ACTION%"=="" (
    endlocal & set "EDGEAI_PROMPT_TAG=%_ACTION%"
    goto :continue_load
)
endlocal

:continue_load

REM ---------------------------------------------------------------
REM 2. Idempotency Guard
REM ---------------------------------------------------------------
if defined EDGEAI_READY (
    echo [!] edge-ai environment already loaded. Use 'call %~f0 force' to re-verify.
    goto :eof
)

REM ---------------------------------------------------------------
REM 3. Project Root Anchoring (Absolute, Never Relative)
REM ---------------------------------------------------------------
REM Resolve to repository root: this script lives at infra\win11\config_win11.bat
REM So PROJECT_ROOT = two levels up from script location
set "EDGEAI_SCRIPT_DIR=%~dp0"
for %%I in ("%EDGEAI_SCRIPT_DIR%\..\..\") do set "EDGEAI_ROOT=%%~fI"
REM Strip trailing backslash for consistency
if "%EDGEAI_ROOT:~-1%"=="\" set "EDGEAI_ROOT=%EDGEAI_ROOT:~0,-1%"

set "PROJECT_ROOT=%EDGEAI_ROOT%"
echo [+] PROJECT_ROOT anchored to: %PROJECT_ROOT%

REM ---------------------------------------------------------------
REM 4. Validate Inherited Toolchains (VS Developer Environment)
REM ---------------------------------------------------------------
echo [*] Verifying inherited Visual Studio developer environment...

where cl.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Validated: Microsoft C/C++ Compiler ^(cl.exe^) is active.
) else (
    echo [-] WARNING: cl.exe not detected.
    echo     Ensure you launched from "Developer Command Prompt for VS 2022/2026"
    echo     or chained vcvarsall.bat in your terminal profile.
)

where cmake.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Validated: CMake is available.
) else (
    echo [-] WARNING: cmake.exe not found. Install CMake or add to PATH.
)

where ninja.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Validated: Ninja build system available.
) else (
    echo [i] Info: Ninja not found. CMake will use default generator.
)

REM ---------------------------------------------------------------
REM 5. Intel oneAPI Detection (Optional Enhancement)
REM ---------------------------------------------------------------
if defined ONEAPI_ROOT (
    echo [+] Validated: Intel oneAPI root detected at %ONEAPI_ROOT%.
) else if defined MKLROOT (
    echo [+] Validated: Intel MKL environment detected.
) else (
    echo [i] Info: Intel oneAPI not detected. SYCL targets will be unavailable.
)

REM ---------------------------------------------------------------
REM 6. Configure Build Environment Variables
REM ---------------------------------------------------------------
set "EDGEAI_PLATFORM=win11_native_cmd"
set "EDGEAI_BUILD_DIR=%PROJECT_ROOT%\build"
set "EDGEAI_LOGS_DIR=%PROJECT_ROOT%\logs"

REM Centralized Model Target Interpolation
if not defined EDGEAI_MODELS_DIR set "EDGEAI_MODELS_DIR=%PROJECT_ROOT%\..\models"
if not defined EDGEAI_TEST_MODEL set "EDGEAI_TEST_MODEL=%EDGEAI_MODELS_DIR%\tinyllama-1.1b-chat-v1.0.Q4_0.gguf"

REM Ensure out-of-tree build directories exist
if not exist "%EDGEAI_BUILD_DIR%" mkdir "%EDGEAI_BUILD_DIR%"
if not exist "%EDGEAI_LOGS_DIR%" mkdir "%EDGEAI_LOGS_DIR%"

REM ---------------------------------------------------------------
REM 7. Load Local Overrides (Machine-Specific, Git-Ignored)
REM ---------------------------------------------------------------
if exist "%PROJECT_ROOT%\config_local.bat" (
    echo [*] Loading machine-specific overrides from config_local.bat...
    call "%PROJECT_ROOT%\config_local.bat"
)

REM ---------------------------------------------------------------
REM 8. Convenience Build Functions via DOSKEY
REM ---------------------------------------------------------------
doskey edgeai_cmake=cmake -S "%PROJECT_ROOT%" -B "%EDGEAI_BUILD_DIR%\$1" -G "Ninja" -DCMAKE_BUILD_TYPE=$2 $3 $4 $5
doskey edgeai_build=cmake --build "%EDGEAI_BUILD_DIR%\$1" --config $2 -j $3
doskey edgeai_clean=if exist "%EDGEAI_BUILD_DIR%\$1" rmdir /s /q "%EDGEAI_BUILD_DIR%\$1"

REM ---------------------------------------------------------------
REM 9. Custom Prompt
REM ---------------------------------------------------------------
if not defined EDGEAI_PROMPT_TAG set "EDGEAI_PROMPT_TAG=default"
prompt [edge-ai:%EDGEAI_PROMPT_TAG%] $P$_$G$S

REM ---------------------------------------------------------------
REM 10. Final Readiness
REM ---------------------------------------------------------------
set "EDGEAI_READY=1"
echo.
echo ==================================================================
echo  edge-ai Windows 11 CMD Environment Ready
echo  Root:     %PROJECT_ROOT%
echo  Build:    %EDGEAI_BUILD_DIR%
echo  Platform: %EDGEAI_PLATFORM%
echo ==================================================================
echo.
goto :eof

REM ---------------------------------------------------------------
REM Unset Handler
REM ---------------------------------------------------------------
:do_unset
echo [!] Tearing down edge-ai CMD environment...
set "EDGEAI_READY="
set "EDGEAI_ROOT="
set "PROJECT_ROOT="
set "EDGEAI_PLATFORM="
set "EDGEAI_BUILD_DIR="
set "EDGEAI_LOGS_DIR="
set "EDGEAI_MODELS_DIR="
set "EDGEAI_TEST_MODEL="
set "EDGEAI_PROMPT_TAG="
prompt
echo [+] edge-ai CMD environment unset.
endlocal
goto :eof
