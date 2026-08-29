@echo off
setlocal EnableExtensions EnableDelayedExpansion

title Python Academy - Setup

echo.
echo ============================================================
echo                 PYTHON ACADEMY SETUP
echo ============================================================
echo.

set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"
set "FRONTEND_DIR=%PROJECT_DIR%frontend"
set "VENV_DIR=%PROJECT_DIR%venv"

REM ============================================================
REM 1. CHECK WINGET
REM ============================================================

echo [1/8] Checking Windows Package Manager...

where winget >nul 2>&1

if errorlevel 1 (
    echo.
    echo [ERROR] Winget is not available.
    echo Please install/update "App Installer" from Microsoft Store.
    echo.
    pause
    exit /b 1
)

echo [OK] Winget found.
echo.


REM ============================================================
REM 2. CHECK / INSTALL VS CODE
REM ============================================================

echo [2/8] Checking Visual Studio Code...

where code >nul 2>&1

if errorlevel 1 (
    echo [MISSING] VS Code not found.
    echo Installing VS Code...
    echo.

    winget install --id Microsoft.VisualStudioCode --exact --silent --accept-package-agreements --accept-source-agreements

    if errorlevel 1 (
        echo.
        echo [ERROR] VS Code installation failed.
        pause
        exit /b 1
    )

    echo [OK] VS Code installed.

    REM Refresh VS Code PATH
    if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" (
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Microsoft VS Code\bin"
    )

) else (
    echo [OK] VS Code already installed.
)

echo.


REM ============================================================
REM 3. CHECK / INSTALL PYTHON
REM ============================================================

echo [3/8] Checking Python...

where python >nul 2>&1

if errorlevel 1 (
    echo [MISSING] Python not found.
    echo Installing Python 3.11...
    echo.

    winget install --id Python.Python.3.11 --exact --silent --accept-package-agreements --accept-source-agreements

    if errorlevel 1 (
        echo.
        echo [ERROR] Python installation failed.
        pause
        exit /b 1
    )

    echo [OK] Python installed.

    REM Refresh common Python paths
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311"
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

) else (
    echo [OK] Python already installed.
)

echo.


REM ============================================================
REM 4. VERIFY PYTHON
REM ============================================================

echo Verifying Python...

python --version

if errorlevel 1 (
    echo.
    echo [ERROR] Python could not be detected after installation.
    echo Please close this window, open a new terminal and run setup.bat again.
    echo.
    pause
    exit /b 1
)

echo [OK] Python is working.
echo.


REM ============================================================
REM 5. CHECK / INSTALL PYTHON EXTENSION
REM ============================================================

echo [4/8] Checking VS Code Python extension...

where code >nul 2>&1

if errorlevel 1 (
    echo [ERROR] VS Code command "code" is not available.
    echo Please restart VS Code/terminal and run setup.bat again.
    echo.
    pause
    exit /b 1
)

code --list-extensions 2>nul | findstr /i "ms-python.python" >nul

if errorlevel 1 (
    echo [MISSING] Python extension not found.
    echo Installing Python extension...

    code --install-extension ms-python.python

    if errorlevel 1 (
        echo.
        echo [ERROR] Python extension installation failed.
        pause
        exit /b 1
    )

    echo [OK] Python extension installed.
) else (
    echo [OK] Python extension already installed.
)

echo.


REM ============================================================
REM 6. CHECK / INSTALL PYLANCE
REM ============================================================

echo [5/8] Checking Pylance...

code --list-extensions 2>nul | findstr /i "ms-python.vscode-pylance" >nul

if errorlevel 1 (
    echo [MISSING] Pylance not found.
    echo Installing Pylance...

    code --install-extension ms-python.vscode-pylance

    if errorlevel 1 (
        echo.
        echo [WARNING] Pylance installation failed.
        echo Continuing setup...
    ) else (
        echo [OK] Pylance installed.
    )
) else (
    echo [OK] Pylance already installed.
)

echo.


REM ============================================================
REM 7. CHECK / INSTALL NODE.JS
REM ============================================================

echo [6/8] Checking Node.js...

where node >nul 2>&1

if errorlevel 1 (
    echo [MISSING] Node.js not found.
    echo Installing Node.js LTS...
    echo.

    winget install --id OpenJS.NodeJS.LTS --exact --silent --accept-package-agreements --accept-source-agreements

    if errorlevel 1 (
        echo.
        echo [ERROR] Node.js installation failed.
        pause
        exit /b 1
    )

    echo [OK] Node.js installed.

    REM Refresh Node.js PATH
    set "PATH=%PATH%;C:\Program Files\nodejs"
) else (
    echo [OK] Node.js already installed.
)

echo.


REM ============================================================
REM 8. VERIFY NODE / NPM
REM ============================================================

echo Verifying Node.js...

node --version

if errorlevel 1 (
    echo.
    echo [ERROR] Node.js could not be detected.
    echo Please restart terminal and run setup.bat again.
    echo.
    pause
    exit /b 1
)

echo.

echo Verifying npm...

npm --version

if errorlevel 1 (
    echo.
    echo [ERROR] npm could not be detected.
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js and npm are working.
echo.


REM ============================================================
REM CREATE VIRTUAL ENVIRONMENT
REM ============================================================

echo ============================================================
echo Creating Python virtual environment...
echo ============================================================
echo.

if not exist "%VENV_DIR%\Scripts\python.exe" (

    echo [MISSING] venv not found.
    echo Creating venv...

    python -m venv "%VENV_DIR%"

    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )

    echo [OK] Virtual environment created.

) else (
    echo [OK] Virtual environment already exists.
)

echo.


REM ============================================================
REM UPGRADE PIP
REM ============================================================

echo Upgrading pip...

"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo [ERROR] pip upgrade failed.
    pause
    exit /b 1
)

echo [OK] pip upgraded.
echo.


REM ============================================================
REM INSTALL BACKEND REQUIREMENTS
REM ============================================================

echo ============================================================
echo Installing Django dependencies...
echo ============================================================
echo.

if not exist "%PROJECT_DIR%requirements.txt" (
    echo [ERROR] requirements.txt not found.
    echo Expected:
    echo %PROJECT_DIR%requirements.txt
    echo.
    pause
    exit /b 1
)

"%VENV_DIR%\Scripts\python.exe" -m pip install -r "%PROJECT_DIR%requirements.txt"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)

echo.
echo [OK] Python dependencies installed.
echo.


REM ============================================================
REM DJANGO CHECK
REM ============================================================

echo Checking Django project...

if not exist "%BACKEND_DIR%\manage.py" (
    echo.
    echo [ERROR] Django manage.py not found.
    echo Expected:
    echo %BACKEND_DIR%\manage.py
    echo.
    pause
    exit /b 1
)

cd /d "%BACKEND_DIR%"

"%VENV_DIR%\Scripts\python.exe" manage.py check

if errorlevel 1 (
    echo.
    echo [ERROR] Django system check failed.
    pause
    exit /b 1
)

echo.
echo [OK] Django system check passed.
echo.


REM ============================================================
REM INSTALL FRONTEND DEPENDENCIES
REM ============================================================

echo ============================================================
echo Installing React dependencies...
echo ============================================================
echo.

if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERROR] frontend\package.json not found.
    pause
    exit /b 1
)

cd /d "%FRONTEND_DIR%"

call npm install

if errorlevel 1 (
    echo.
    echo [ERROR] npm install failed.
    pause
    exit /b 1
)

echo.
echo [OK] React dependencies installed.
echo.


REM ============================================================
REM CREATE VS CODE SETTINGS
REM ============================================================

echo Configuring VS Code...

if not exist "%PROJECT_DIR%.vscode" (
    mkdir "%PROJECT_DIR%.vscode"
)

(
echo {
echo     "python.defaultInterpreterPath": "${workspaceFolder}\\venv\\Scripts\\python.exe",
echo     "python.terminal.activateEnvironment": true,
echo     "python.analysis.autoImportCompletions": true,
echo     "python.analysis.typeCheckingMode": "basic"
echo }
) > "%PROJECT_DIR%.vscode\settings.json"

echo [OK] VS Code settings configured.
echo.


REM ============================================================
REM FINISHED
REM ============================================================

cd /d "%PROJECT_DIR%"

echo.
echo ============================================================
echo               PYTHON ACADEMY SETUP COMPLETE
echo ============================================================
echo.
echo Python:
python --version

echo.
echo Node.js:
node --version

echo.
echo npm:
npm --version

echo.
echo Virtual Environment:
echo %VENV_DIR%

echo.
echo Backend:
echo %BACKEND_DIR%

echo.
echo Frontend:
echo %FRONTEND_DIR%

echo.
echo ============================================================
echo Next step: Run start.bat
echo ============================================================
echo.

pause
exit /b 0