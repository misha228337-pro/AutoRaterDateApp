@echo off
chcp 65001 >nul
echo 🚀 ЗАПУСК МИНИМАЛЬНОЙ ВЕРСИИ БОТА
echo =====================================

echo 📋 Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.11
    pause
    exit /b 1
)

echo 📋 Проверка библиотек...
python -c "import pyautogui, pytesseract, keyboard" >nul 2>&1
if errorlevel 1 (
    echo ❌ Библиотеки не найдены! Запустите install_minimal.bat
    pause
    exit /b 1
)

echo ✅ Все проверки пройдены
echo.
echo 📋 Инструкция:
echo 1. Убедитесь что Telegram запущен
echo 2. Откройте чат с @bibinto_bot
echo 3. Нажмите кнопку "Оценивать"
echo 4. Программа начнет работу автоматически
echo.
echo ⏹️ Нажмите 'q' для остановки программы
echo.

pause

echo 🔄 Переключаюсь на Telegram...
timeout /t 2 >nul
powershell -command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('%{TAB}')"
timeout /t 1 >nul

python telegram_bot_minimal.py

echo.
echo Программа завершена. Нажмите любую клавишу для выхода...
pause