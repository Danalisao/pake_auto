@echo off
title Création d'un exécutable Pake GUI
echo.
echo ==========================================
echo      Création d'un exécutable
echo ==========================================
echo.

REM Vérifier si PyInstaller est installé
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation de PyInstaller
        pause
        exit /b 1
    )
)

echo 🔨 Création de l'exécutable...
pyinstaller --onefile --windowed --name "PakeGUI" --icon=icon.ico pake_gui.py

if errorlevel 1 (
    echo ❌ Erreur lors de la création de l'exécutable
    pause
    exit /b 1
)

echo.
echo ✅ Exécutable créé avec succès!
echo 📁 Fichier disponible dans: dist\PakeGUI.exe
echo.
pause
