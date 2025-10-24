#!/usr/bin/env python3
"""
Проверка всех зависимостей для автоматизатора
"""

import sys
import subprocess
import importlib

def check_python():
    """Проверка версии Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    print(f"   Версия: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 7):
        print("   ❌ Требуется Python 3.7 или выше")
        return False
    else:
        print("   ✅ Версия подходящая")
        return True

def check_module(module_name):
    """Проверка установки модуля"""
    try:
        importlib.import_module(module_name)
        print(f"   ✅ {module_name} - установлен")
        return True
    except ImportError:
        print(f"   ❌ {module_name} - НЕ установлен")
        return False

def check_pytesseract():
    """Специальная проверка для pytesseract"""
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ pytesseract - установлен (версия: {version})")
        return True
    except ImportError:
        print("   ❌ pytesseract - НЕ установлен")
        return False
    except Exception as e:
        print(f"   ⚠️  pytesseract - установлен, но ошибка: {e}")
        return False

def check_tesseract_binary():
    """Проверка Tesseract OCR в системе"""
    print("🔍 Проверка Tesseract OCR...")
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ Tesseract найден: {version_line}")
            return True
        else:
            print("   ❌ Tesseract не найден в PATH")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ Tesseract не найден в PATH")
        return False

def check_files():
    """Проверка наличия файлов проекта"""
    print("📁 Проверка файлов проекта...")
    
    required_files = [
        'telegram_bot_automator_v2.py',
        'config.py',
        'requirements.txt'
    ]
    
    all_found = True
    for file in required_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                pass
            print(f"   ✅ {file} - найден")
        except FileNotFoundError:
            print(f"   ❌ {file} - НЕ найден")
            all_found = False
        except Exception as e:
            print(f"   ⚠️  {file} - ошибка чтения: {e}")
            all_found = False
    
    return all_found

def install_missing():
    """Попытка установить недостающие зависимости"""
    print("\n📦 Попытка установки зависимостей...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("   ✅ Зависимости установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Ошибка установки: {e}")
        return False

def main():
    """Главная функция"""
    print("=" * 60)
    print("🔍 ПРОВЕРКА ЗАВИСИМОСТЕЙ АВТОМАТИЗАТОРА")
    print("=" * 60)
    print()
    
    # Проверка Python
    python_ok = check_python()
    print()
    
    if not python_ok:
        print("❌ Python не соответствует требованиям")
        return False
    
    # Проверка модулей
    print("📚 Проверка Python модулей...")
    modules = [
        'pyautogui',
        'cv2',  # opencv-python
        'keyboard',
        'psutil',
        'numpy',
        'PIL'   # pillow
    ]
    
    modules_ok = all(check_module(module) for module in modules)
    
    # Специальная проверка pytesseract
    pytesseract_ok = check_pytesseract()
    print()
    
    # Проверка Tesseract OCR
    tesseract_ok = check_tesseract_binary()
    print()
    
    # Проверка файлов
    files_ok = check_files()
    print()
    
    # Итог
    print("=" * 60)
    print("📊 ИТОГИ ПРОВЕРКИ:")
    print(f"   Python: {'✅' if python_ok else '❌'}")
    print(f"   Модули: {'✅' if modules_ok else '❌'}")
    print(f"   Pytesseract: {'✅' if pytesseract_ok else '❌'}")
    print(f"   Tesseract OCR: {'✅' if tesseract_ok else '❌'}")
    print(f"   Файлы: {'✅' if files_ok else '❌'}")
    
    all_ok = all([python_ok, modules_ok, pytesseract_ok, tesseract_ok, files_ok])
    
    if all_ok:
        print("\n🎉 ВСЕ КОМПОНЕНТЫ ГОТОВЫ!")
        print("   Можно запускать программу:")
        print("   python telegram_bot_automator_v2.py")
    else:
        print("\n⚠️  Есть проблемы с зависимостями:")
        
        if not modules_ok:
            print("   📦 Установите недостающие модули:")
            print("      pip install -r requirements.txt")
        
        if not tesseract_ok:
            print("   🔧 Установите Tesseract OCR:")
            print("      https://github.com/UB-Mannheim/tesseract/wiki")
        
        if not files_ok:
            print("   📁 Проверьте наличие всех файлов проекта")
    
    print("=" * 60)
    
    return all_ok

if __name__ == "__main__":
    try:
        success = main()
        input("\nНажмите Enter для выхода...")
    except KeyboardInterrupt:
        print("\n\n👋 Проверка прервана")
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        input("\nНажмите Enter для выхода...")