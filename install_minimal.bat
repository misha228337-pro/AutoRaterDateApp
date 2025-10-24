@echo off
chcp 65001 >nul
echo 🔧 УСТАНОВКА МИНИМАЛЬНОЙ ВЕРСИИ (без OpenCV)
echo ===============================================

echo 📋 Шаг 1: Удаление проблемных библиотек...
pip uninstall numpy opencv-python -y
echo.

echo 📋 Шаг 2: Установка стабильной версии numpy...
pip install numpy==1.24.3
if errorlevel 1 (
    echo ⚠️ Ошибка! Пробую альтернативный способ...
    pip install --only-binary=all numpy==1.24.3
)
echo.

echo 📋 Шаг 3: Установка остальных библиотек...
pip install pyautogui
pip install pytesseract
pip install keyboard
pip install psutil
pip install pillow
echo.

echo ✅ Установка завершена!
echo 💡 Теперь запустите минимальную версию:
echo    python telegram_bot_minimal.py
echo.
pause