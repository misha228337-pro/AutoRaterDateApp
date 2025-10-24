#!/usr/bin/env python3
"""
Тестовый скрипт для проверки компонентов автоматизации
"""

import pyautogui
import time
import logging
import pytesseract
import cv2
import numpy as np
import keyboard
from typing import Optional, Tuple
import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutomatorTester:
    def __init__(self):
        self.running = True
        
    def test_screen_capture(self) -> bool:
        """Тест захвата экрана"""
        try:
            logging.info("🧪 Тест захвата экрана...")
            
            screenshot = pyautogui.screenshot()
            screen_width, screen_height = pyautogui.size()
            
            logging.info(f"✅ Размер экрана: {screen_width}x{screen_height}")
            logging.info(f"✅ Скриншот успешно создан: {screenshot.size}")
            
            # Сохраняем тестовый скриншот
            screenshot.save("test_screenshot.png")
            logging.info("✅ Тестовый скриншот сохранен как 'test_screenshot.png'")
            
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка при захвате экрана: {e}")
            return False
    
    def test_tesseract_ocr(self) -> bool:
        """Тест Tesseract OCR"""
        try:
            logging.info("🧪 Тест Tesseract OCR...")
            
            # Проверяем версию Tesseract
            version = pytesseract.get_tesseract_version()
            logging.info(f"✅ Версия Tesseract: {version}")
            
            # Делаем скриншот и распознаем текст
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # Распознаем текст
            recognized_text = pytesseract.image_to_string(gray, lang=config.OCR_LANGUAGES)
            
            logging.info(f"✅ Текст успешно распознан")
            logging.info(f"📝 Распознанный текст (первые 200 символов): {recognized_text[:200]}...")
            
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка Tesseract: {e}")
            return False
    
    def test_mouse_control(self) -> bool:
        """Тест управления мышью"""
        try:
            logging.info("🧪 Тест управления мышью...")
            
            # Получаем текущую позицию мыши
            current_pos = pyautogui.position()
            logging.info(f"📍 Текущая позиция мыши: {current_pos}")
            
            # Двигаем мышь в центр экрана
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            
            logging.info(f"🎯 Перемещение мыши в центр: ({center_x}, {center_y})")
            pyautogui.moveTo(center_x, center_y, duration=1.0)
            
            time.sleep(1)
            
            # Возвращаем мышь обратно
            logging.info(f"🔙 Возврат мыши в исходную позицию: {current_pos}")
            pyautogui.moveTo(current_pos[0], current_pos[1], duration=1.0)
            
            logging.info("✅ Управление мышью работает корректно")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка управления мышью: {e}")
            return False
    
    def test_keyboard_control(self) -> bool:
        """Тест управления клавиатурой"""
        try:
            logging.info("🧪 Тест управления клавиатурой...")
            
            logging.info("⌨️  Тест ввода текста (откройте Блокнот или текстовый редактор)")
            input("Нажмите Enter когда готовы к тесту ввода...")
            
            test_text = "Hello, World! Привет, мир!"
            
            # Ввод тестового текста
            for char in test_text:
                pyautogui.press(char)
                time.sleep(0.1)
            
            time.sleep(2)
            
            logging.info("✅ Управление клавиатурой работает корректно")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка управления клавиатурой: {e}")
            return False
    
    def test_telegram_detection(self) -> bool:
        """Тест обнаружения Telegram"""
        try:
            logging.info("🧪 Тест обнаружения Telegram...")
            
            # Проверяем процессы
            import psutil
            telegram_found = False
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and any(name in proc.info['name'].lower() for name in ['telegram', 'telegram desktop']):
                    logging.info(f"✅ Найден процесс: {proc.info['name']}")
                    telegram_found = True
            
            if not telegram_found:
                logging.warning("⚠️  Процесс Telegram не найден")
                logging.info("📝 Пожалуйста, запустите Telegram Desktop")
            
            # Проверяем наличие окна через OCR
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            recognized_text = pytesseract.image_to_string(gray, lang=config.OCR_LANGUAGES).lower()
            
            telegram_ui_elements = ["поиск", "чаты", "контакты", "telegram"]
            found_elements = [elem for elem in telegram_ui_elements if elem in recognized_text]
            
            if found_elements:
                logging.info(f"✅ Найдены элементы интерфейса Telegram: {found_elements}")
            else:
                logging.warning("⚠️  Элементы интерфейса Telegram не найдены")
            
            return telegram_found or len(found_elements) > 0
        except Exception as e:
            logging.error(f"❌ Ошибка при обнаружении Telegram: {e}")
            return False
    
    def test_rating_algorithm(self) -> bool:
        """Тест алгоритма генерации оценок"""
        try:
            logging.info("🧪 Тест алгоритма генерации оценок...")
            
            # Генерируем 100 оценок для анализа
            ratings = []
            for _ in range(100):
                rand = random.random()
                if rand < 0.7:  # 70% - оценки 8-10
                    rating = random.choices([8, 9, 10], weights=[0.3, 0.4, 0.3])[0]
                elif rand < 0.85:  # 15% - оценки 6-7
                    rating = random.choices([6, 7], weights=[0.6, 0.4])[0]
                elif rand < 0.95:  # 10% - оценки 3-5
                    rating = random.choices([3, 4, 5], weights=[0.2, 0.3, 0.5])[0]
                else:  # 5% - очень низкие оценки
                    rating = random.choices([1, 2], weights=[0.6, 0.4])[0]
                
                ratings.append(rating)
            
            # Анализируем распределение
            from collections import Counter
            rating_counts = Counter(ratings)
            
            logging.info("📊 Распределение оценок (100 тестовых генераций):")
            for rating in sorted(rating_counts.keys()):
                percentage = (rating_counts[rating] / 100) * 100
                logging.info(f"   Оценка {rating}: {rating_counts[rating]} раз ({percentage:.1f}%)")
            
            high_ratings = sum(rating_counts[r] for r in [8, 9, 10])
            low_ratings = sum(rating_counts[r] for r in [1, 2, 3, 4, 5])
            
            logging.info(f"📈 Высокие оценки (8-10): {high_ratings}%")
            logging.info(f"📉 Низкие оценки (1-5): {low_ratings}%")
            
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка при тесте алгоритма оценок: {e}")
            return False
    
    def interactive_test(self) -> None:
        """Интерактивный тест с пользователем"""
        print("\n" + "="*50)
        print("🧪 ИНТЕРАКТИВНЫЙ ТЕСТ АВТОМАТИЗАТОРА")
        print("="*50)
        
        tests = [
            ("Захват экрана", self.test_screen_capture),
            ("Tesseract OCR", self.test_tesseract_ocr),
            ("Управление мышью", self.test_mouse_control),
            ("Управление клавиатурой", self.test_keyboard_control),
            ("Обнаружение Telegram", self.test_telegram_detection),
            ("Алгоритм оценок", self.test_rating_algorithm),
        ]
        
        for i, (test_name, test_func) in enumerate(tests, 1):
            print(f"\n{i}. {test_name}")
            
            choice = input("   Выполнить тест? (y/n): ").lower()
            if choice == 'y':
                try:
                    success = test_func()
                    if success:
                        print(f"   ✅ Тест '{test_name}' пройден")
                    else:
                        print(f"   ❌ Тест '{test_name}' не пройден")
                except Exception as e:
                    print(f"   ❌ Ошибка в тесте '{test_name}': {e}")
            else:
                print(f"   ⏭️  Тест '{test_name}' пропущен")
        
        print("\n" + "="*50)
        print("🏁 Тестирование завершено")
        print("="*50)
    
    def quick_test(self) -> bool:
        """Быстрая проверка основных компонентов"""
        logging.info("🚀 Быстрая проверка компонентов...")
        
        critical_tests = [
            ("Захват экрана", self.test_screen_capture),
            ("Tesseract OCR", self.test_tesseract_ocr),
        ]
        
        all_passed = True
        for test_name, test_func in critical_tests:
            if not test_func():
                logging.error(f"❌ Критический тест '{test_name}' не пройден")
                all_passed = False
            else:
                logging.info(f"✅ Тест '{test_name}' пройден")
        
        return all_passed

def main():
    """Главная функция тестирования"""
    import random
    
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ АВТОМАТИЗАТОРА БИБИНТО")
    print("=" * 60)
    
    print("Выберите режим тестирования:")
    print("1. Быстрая проверка (критические компоненты)")
    print("2. Интерактивный тест (все компоненты)")
    print("3. Выход")
    
    choice = input("\nВаш выбор (1-3): ").strip()
    
    tester = AutomatorTester()
    
    if choice == "1":
        if tester.quick_test():
            print("\n✅ Все критические тесты пройдены! Программа готова к работе.")
        else:
            print("\n❌ Есть проблемы, которые нужно решить перед использованием.")
    
    elif choice == "2":
        tester.interactive_test()
    
    elif choice == "3":
        print("👋 Выход из тестирования")
    
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()