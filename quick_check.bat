@echo off
chcp 65001 >nul
title ⚡ Быстрая проверка зависимостей

echo.
echo ================================================
echo ⚡ БЫСТРАЯ ПРОВЕРКА ЗАВИСИМОСТЕЙ
echo ================================================
echo.

echo 📋 Проверка Python...
python --version
if errorlevel 1 (
    echo ❌ Python не найден!
    goto :end
)

echo.
echo 📋 Проверка основных библиотек...
echo.

python -c "import pyautogui" 2>nul && echo ✅ pyautogui - OK || echo ❌ pyautogui - НЕ УСТАНОВЛЕН
python -c "import pytesseract" 2>nul && echo ✅ pytesseract - OK || echo ❌ pytesseract - НЕ УСТАНОВЛЕН
python -c "import cv2" 2>nul && echo ✅ opencv-python - OK || echo ❌ opencv-python - НЕ УСТАНОВЛЕН
python -c "import keyboard" 2>nul && echo ✅ keyboard - OK || echo ❌ keyboard - НЕ УСТАНОВЛЕН
python -c "import psutil" 2>nul && echo ✅ psutil - OK || echo ❌ psutil - НЕ УСТАНОВЛЕН

echo.
echo 📋 Проверка Tesseract...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Tesseract OCR не найден в PATH
) else (
    echo ✅ Tesseract OCR - OK
)

echo.
echo 📋 Проверка файлов проекта...
if exist "telegram_bot_automator_v2.py" (
    echo ✅ Основной файл - OK
) else (
    echo ❌ Основной файл НЕ НАЙДЕН
)

if exist "config.py" (
    echo ✅ Конфигурация - OK
) else (
    echo ❌ Конфигурация НЕ НАЙДЕНА
)

echo.
echo 📋 Рекомендации:
echo 1. Если есть ❌ - запустите: pip install -r requirements.txt
echo 2. Если Tesseract не найден - установите с официального сайта
echo 3. Запускайте программу от имени администратора

:end
echo.
echo ================================================
echo ⚡ ПРОВЕРКА ЗАВЕРШЕНА
echo ================================================
echo.
pause