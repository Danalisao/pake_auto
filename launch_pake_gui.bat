@echo off
title Pake GUI - Lanceur
echo.
echo ====================================
echo        Pake GUI - Lanceur
echo ====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Lancer l'application
echo Lancement de Pake GUI...
python pake_gui.py

REM Pause en cas d'erreur
if errorlevel 1 (
    echo.
    echo Une erreur s'est produite
    pause
)
