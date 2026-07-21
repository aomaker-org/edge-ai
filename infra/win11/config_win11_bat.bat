@echo off
REM ==============================================================================
REM Filename:     infra/win11/config_win11_bat.bat
REM Purpose:      Native Windows 11 CMD/Batch Environment Loader for edge-ai
REM Type:         Invoked (call infra\win11\config_win11_bat.bat)
REM Attribution:  fekerr & Antigravity (20260720 / Consolidated Win11 Stack)
REM ==============================================================================

setlocal enabledelayedexpansion

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

if defined EDGEAI_READY (
    echo [!] edge-ai environment already loaded. Use 'call %~f0 force' to re-verify.
    goto :eof
)

set "EDGEAI_SCRIPT_DIR=%~dp0"
for %%I in ("%EDGEAI_SCRIPT_DIR%\..\..\") do set "EDGEAI_ROOT=%%~fI"
if "%EDGEAI_ROOT:~-1%"=="\" set "EDGEAI_ROOT=%EDGEAI_ROOT:~0,-1%"

set "PROJECT_ROOT=%EDGEAI_ROOT%"
echo [+] PROJECT_ROOT anchored to: %PROJECT_ROOT%

where cl.exe >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%PROJECT_ROOT%\.edgeai_env.bat" (
        echo [*] Injected cached MSVC build environment from .edgeai_env.bat...
        call "%PROJECT_ROOT%\.edgeai_env.bat"
    ) else if exist "%PROJECT_ROOT%\infra\win11\capture_env.py" (
        where python >nul 2>&1
        if !errorlevel! equ 0 (
            echo [*] Auto-running environment capturer (capture_env.py)...
            python "%PROJECT_ROOT%\infra\win11\capture_env.py" --output-dir "%PROJECT_ROOT%" >nul 2>&1
            if exist "%PROJECT_ROOT%\.edgeai_env.bat" call "%PROJECT_ROOT%\.edgeai_env.bat"
        )
    )
)

where cl.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Validated: Microsoft C/C++ Compiler ^(cl.exe^) is active.
) else (
    echo [-] WARNING: cl.exe not detected. Ensure VS2022 Dev tools are installed.
)

where cmake.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Validated: CMake is available.
) else (
    echo [-] WARNING: cmake.exe not found.
)

set "EDGEAI_PLATFORM=win11_native_cmd"
set "EDGEAI_BUILD_DIR=%PROJECT_ROOT%\build"
set "EDGEAI_LOGS_DIR=%PROJECT_ROOT%\logs"

if not defined EDGEAI_MODELS_DIR set "EDGEAI_MODELS_DIR=%PROJECT_ROOT%\..\models"
if not defined EDGEAI_TEST_MODEL set "EDGEAI_TEST_MODEL=%EDGEAI_MODELS_DIR%\tinyllama-1.1b-chat-v1.0.Q4_0.gguf"

if not exist "%EDGEAI_BUILD_DIR%" mkdir "%EDGEAI_BUILD_DIR%"
if not exist "%EDGEAI_LOGS_DIR%" mkdir "%EDGEAI_LOGS_DIR%"

if exist "%PROJECT_ROOT%\config_local.bat" (
    echo [*] Loading machine-specific overrides from config_local.bat...
    call "%PROJECT_ROOT%\config_local.bat"
)

doskey edgeai_cmake=cmake -S "%PROJECT_ROOT%" -B "%EDGEAI_BUILD_DIR%\$1" -G "Ninja" -DCMAKE_BUILD_TYPE=$2 $3 $4 $5
doskey edgeai_build=cmake --build "%EDGEAI_BUILD_DIR%\$1" --config $2 -j $3
doskey edgeai_clean=if exist "%EDGEAI_BUILD_DIR%\$1" rmdir /s /q "%EDGEAI_BUILD_DIR%\$1"

if not defined EDGEAI_PROMPT_TAG set "EDGEAI_PROMPT_TAG=default"
prompt [edge-ai:%EDGEAI_PROMPT_TAG%] $P$_$G$S

set "EDGEAI_READY=1"
echo.
echo ==================================================================
echo  edge-ai Windows 11 CMD Environment Ready
echo  Root:     %PROJECT_ROOT%
echo  Build:    %EDGEAI_BUILD_DIR%
echo  Platform: %EDGEAI_PLATFORM%
echo  Tag:      %EDGEAI_PROMPT_TAG%
echo ==================================================================
echo.
goto :eof

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
