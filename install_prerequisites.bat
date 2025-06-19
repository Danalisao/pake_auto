@echo off
title Installation des prérequis Pake GUI
echo.
echo ==========================================
echo    Installation des prérequis Pake GUI
echo ==========================================
echo.

REM Vérifier si on est administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ATTENTION: Certaines installations peuvent nécessiter des droits administrateur
    echo.
)

echo 1. Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non installé
    echo 📥 Ouverture de la page de téléchargement Python...
    start https://python.org/downloads/
    echo Veuillez installer Python et relancer ce script
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python installé: %PYTHON_VERSION%
)

echo.
echo 2. Vérification de Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js non installé
    echo 📥 Ouverture de la page de téléchargement Node.js...
    start https://nodejs.org/
    echo Veuillez installer Node.js et relancer ce script
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js installé: %NODE_VERSION%
)

echo.
echo 3. Vérification de Rust...
rustc --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Rust non installé
    echo 📥 Ouverture de la page d'installation Rust...
    start https://www.rust-lang.org/tools/install
    echo Veuillez installer Rust et relancer ce script
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('rustc --version 2^>^&1') do set RUST_VERSION=%%i
    echo ✅ Rust installé: %RUST_VERSION%
)

echo.
echo 4. Configuration PowerShell pour npm...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" >nul 2>&1
echo ✅ Politique d'exécution PowerShell configurée

echo.
echo 5. Installation de Pake CLI...
pake --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de pake-cli via npm...
    call npm install -g pake-cli
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation de Pake CLI
        echo Essayez manuellement: npm install -g pake-cli
        pause
        exit /b 1
    ) else (
        echo ✅ Pake CLI installé avec succès
    )
) else (
    for /f "tokens=1" %%i in ('pake --version 2^>^&1') do set PAKE_VERSION=%%i
    echo ✅ Pake CLI déjà installé: %PAKE_VERSION%
)

echo.
echo ==========================================
echo       Installation terminée! 🎉
echo ==========================================
echo.
echo Tous les prérequis sont installés.
echo Vous pouvez maintenant lancer Pake GUI avec:
echo   launch_pake_gui.bat
echo.
pause
