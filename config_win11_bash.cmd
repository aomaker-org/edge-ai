@echo off
:: ============================================================================
:: launch-dev-bash.cmd
:: Reusable launcher for Visual Studio + Intel oneAPI + Git Bash
:: ============================================================================

:: 1. Load Visual Studio 2022 Developer Environment
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" (
    call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" -arch=amd64
) else (
    echo [ERROR] Visual Studio 2022 VsDevCmd.bat not found.
    exit /b 1
)

:: 2. Conditionally Load Intel oneAPI Environment
if /i "%~1"=="--oneapi" (
    if exist "C:\Program Files (x86)\Intel\oneAPI\setvars.bat" (
        call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
    ) else (
        echo [WARNING] Intel oneAPI setvars.bat not found. Skipping oneAPI setup...
    )
)

:: 3. Launch Git Bash (Inherits all CMD environment variables)
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" --login -i
) else (
    echo [ERROR] Git Bash executable not found at expected path.
    exit /b 1
)
