#!/usr/bin/env python3
"""
Установочный скрипт для проекта автоматизации бота
"""

import subprocess
import sys
import os

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше")
        return False
    print(f"✅ Python версии {sys.version_info.major}.{sys.version_info.minor} найден")
    return True

def install_requirements():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости успешно установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при установке зависимостей: {e}")
        return False

def check_tesseract():
    """Проверка наличия Tesseract OCR"""
    try:
        import pytesseract
        # Попытка получить версию Tesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR версии {version} найден")
        return True
    except Exception as e:
        print("❌ Tesseract OCR не найден или не настроен")
        print("📝 Пожалуйста, установите Tesseract OCR:")
        print("   1. Скачайте с: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Установите, отметив русский язык")
        print("   3. При необходимости укажите путь в config.py")
        return False

def create_directories():
    """Создание необходимых директорий"""
    directories = ["logs", "screenshots"]
    for dir_name in directories:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ Директория '{dir_name}' создана")
        except Exception as e:
            print(f"❌ Ошибка при создании директории '{dir_name}': {e}")
            return False
    return True

def main():
    """Главная функция установки"""
    print("=" * 50)
    print("🚀 Установка автоматизации бота Bibinto")
    print("=" * 50)
    
    steps = [
        ("Проверка версии Python", check_python_version),
        ("Установка зависимостей Python", install_requirements),
        ("Проверка Tesseract OCR", check_tesseract),
        ("Создание директорий", create_directories),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    if failed_steps:
        print("❌ Установка не завершена. Проблемы в следующих шагах:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n📝 Пожалуйста, решите указанные проблемы и запустите установку заново")
    else:
        print("✅ Установка успешно завершена!")
        print("\n🎯 Теперь вы можете запустить программу:")
        print("   python telegram_bot_automator_v2.py")
    print("=" * 50)

if __name__ == "__main__":
    main()