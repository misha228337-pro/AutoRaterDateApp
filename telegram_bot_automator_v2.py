import pyautogui
import time
import random
import logging
import pytesseract
import cv2
import numpy as np
import keyboard
import psutil
import re
from typing import Optional, Tuple, List
import os
import config

# Настройка пути к Tesseract если указан в конфиге
if config.TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

class TelegramBotAutomator:
    def __init__(self):
        self.running = True
        self.confidence = config.IMAGE_CONFIDENCE
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
        
    def find_telegram_window(self) -> bool:
        """Поиск окна Telegram среди запущенных процессов"""
        logging.info("Поиск окна Telegram...")
        
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and any(name in proc.info['name'].lower() for name in ['telegram', 'telegram desktop']):
                    logging.info(f"Найден процесс Telegram: {proc.info['name']}")
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.warning(f"Ошибка при поиске процессов: {e}")
        
        logging.error("Telegram не найден в запущенных процессах")
        return False
    
    def activate_telegram_window(self) -> bool:
        """Активация окна Telegram"""
        try:
            logging.info("Активация окна Telegram...")
            
            # Попытка переключиться на Telegram через Alt+Tab
            pyautogui.hotkey('alt', 'tab')
            time.sleep(2)
            
            # Пробуем несколько раз Alt+Tab, чтобы найти Telegram
            for i in range(3):
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)
            
            # Упрощенная проверка - просто считаем, что активация прошла успешно
            # если процесс Telegram найден
            logging.info("Окно Telegram активировано (проверка по процессу)")
            return True
                
        except Exception as e:
            logging.error(f"Ошибка при активации Telegram: {e}")
            return False
    
    def look_for_telegram_elements(self) -> bool:
        """Поиск характерных элементов интерфейса Telegram"""
        try:
            # Ищем типичные элементы интерфейса Telegram
            telegram_elements = ["поиск", "чаты", "контакты", "настройки"]
            
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            recognized_text = pytesseract.image_to_string(gray, lang=config.OCR_LANGUAGES)
            
            found_elements = [elem for elem in telegram_elements if elem.lower() in recognized_text.lower()]
            
            if found_elements:
                logging.info(f"Найдены элементы Telegram: {found_elements}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Ошибка при поиске элементов Telegram: {e}")
            return False
    
    def find_text_coordinates(self, text: str, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
        """Поиск координат текста на экране"""
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # Используем pytesseract для поиска данных
            data = pytesseract.image_to_data(gray, lang=config.OCR_LANGUAGES, output_type=pytesseract.Output.DICT)
            
            # Ищем нужный текст
            for i in range(len(data['text'])):
                if text.lower() in data['text'][i].lower():
                    x = data['left'][i] + (data['width'][i] // 2)
                    y = data['top'][i] + (data['height'][i] // 2)
                    
                    if region:
                        x += region[0]
                        y += region[1]
                    
                    logging.info(f"Текст '{text}' найден в координатах: ({x}, {y})")
                    return (x, y)
            
            return None
            
        except Exception as e:
            logging.error(f"Ошибка при поиске координат текста '{text}': {e}")
            return None
    
    def click_text(self, text: str) -> bool:
        """Клик по тексту на экране"""
        try:
            coordinates = self.find_text_coordinates(text)
            if coordinates:
                pyautogui.click(coordinates[0], coordinates[1])
                time.sleep(1)
                return True
            else:
                logging.warning(f"Текст '{text}' не найден для клика")
                return False
        except Exception as e:
            logging.error(f"Ошибка при клике на текст '{text}': {e}")
            return False
    
    def type_message_human_like(self, message: str) -> None:
        """Ввод сообщения с эмуляцией человеческой печати"""
        try:
            # Очистка поля ввода
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            # Ввод сообщения с случайной задержкой между символами
            for char in message:
                pyautogui.press(char)
                time.sleep(random.uniform(config.MIN_CHAR_DELAY, config.MAX_CHAR_DELAY))
            
            logging.info(f"Введено сообщение: {message}")
        except Exception as e:
            logging.error(f"Ошибка при вводе сообщения '{message}': {e}")
    
    def generate_smart_rating(self) -> str:
        """Генерация оценки с реалистичным распределением"""
        # Более реалистичное распределение оценок
        rand = random.random()
        
        if rand < 0.7:  # 70% - оценки 8-10
            rating = random.choices([8, 9, 10], weights=[0.3, 0.4, 0.3])[0]
        elif rand < 0.85:  # 15% - оценки 6-7
            rating = random.choices([6, 7], weights=[0.6, 0.4])[0]
        elif rand < 0.95:  # 10% - оценки 3-5
            rating = random.choices([3, 4, 5], weights=[0.2, 0.3, 0.5])[0]
        else:  # 5% - очень низкие оценки
            rating = random.choices([1, 2], weights=[0.6, 0.4])[0]
        
        return str(rating)
    
    def wait_realistic_interval(self) -> None:
        """Ожидание реалистичного интервала времени"""
        # Более реалистичные интервалы с небольшими вариациями
        base_interval = random.uniform(config.MIN_RATING_INTERVAL, config.MAX_RATING_INTERVAL)
        
        # Добавляем небольшую случайную задержку
        extra_delay = random.uniform(0, 2)
        total_interval = base_interval + extra_delay
        
        logging.info(f"Ожидание {total_interval:.1f} секунд...")
        time.sleep(total_interval)
    
    def start_bot_session(self) -> bool:
        """Начало сессии с ботом"""
        try:
            logging.info("Начало работы с ботом...")
            
            # Проверяем, что мы в чате с нужным ботом
            if self.verify_bot_chat():
                # Отправляем команду /start
                self.type_message_human_like("/start")
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(3)
                
                logging.info("Команда /start отправлена")
                return True
            else:
                logging.error("Не удалось подтвердить, что мы в чате с ботом @bibinto_bot")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка при начале сессии с ботом: {e}")
            return False
    
    def verify_bot_chat(self) -> bool:
        """Проверка, что мы в чате с ботом @bibinto_bot"""
        try:
            logging.info("Проверка чата с ботом @bibinto_bot...")
            
            # Даем пользователю время убедиться, что в правильном чате
            time.sleep(2)
            
            # Упрощенная проверка - считаем, что если пользователь запустил программу,
            # то он уже в нужном чате
            logging.info("Предполагаем, что пользователь в чате с ботом @bibinto_bot")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при проверке чата с ботом: {e}")
            return False
    
    def find_and_click_rate_button_smart(self) -> bool:
        """Умный поиск и нажатие кнопки 'Оценивать'"""
        try:
            logging.info(f"Поиск кнопки '{config.RATE_BUTTON_TEXT}'...")
            
            # Сначала пробуем найти текст и кликнуть на него
            if self.click_text(config.RATE_BUTTON_TEXT):
                time.sleep(2)
                
                # Проверяем, появилась ли новая анкета
                if self.check_for_new_profile_smart():
                    logging.info("Кнопка 'Оценивать' успешно нажата")
                    return True
            
            # Если не сработало, пробуем найти по координатам
            return self.try_click_rate_button_by_position()
                
        except Exception as e:
            logging.error(f"Ошибка при поиске кнопки 'Оценивать': {e}")
            return False
    
    def try_click_rate_button_by_position(self) -> bool:
        """Попытка нажать кнопку по типовым позициям"""
        try:
            screen_width, screen_height = pyautogui.size()
            
            # Различные возможные позиции кнопки
            button_positions = [
                (screen_width // 2, screen_height - 100),  # Центр внизу
                (screen_width // 2, screen_height - 150),  # Чуть выше
                (screen_width // 2, screen_height - 200),  # Еще выше
                (screen_width // 2, screen_height - 250),  # Еще выше
                (screen_width - 150, screen_height - 100),  # Справа внизу
                (screen_width - 200, screen_height - 150),  # Справа чуть выше
            ]
            
            for i, pos in enumerate(button_positions):
                logging.info(f"Попытка {i+1}: клик в позиции {pos}")
                pyautogui.click(pos[0], pos[1])
                time.sleep(2)
                
                if self.check_for_new_profile_smart():
                    logging.info(f"Кнопка найдена в позиции {pos}")
                    return True
            
            return False
            
        except Exception as e:
            logging.error(f"Ошибка при поиске кнопки по позициям: {e}")
            return False
    
    def check_for_new_profile_smart(self) -> bool:
        """Умная проверка наличия новой анкеты"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # Улучшенное распознавание текста
            recognized_text = pytesseract.image_to_string(gray, lang=config.OCR_LANGUAGES).lower()
            
            logging.info(f"Распознанный текст: {recognized_text[:200]}...")
            
            # Расширенный список индикаторов анкеты
            profile_indicators = [
                "лет", "год", "возраст", "лет", "лет", "город", "страна",
                "ищу", "поиск", "знакомства", "анкета", "профиль",
                "photo", "фото", "изображение", "имя", "name"
            ]
            
            # Проверяем наличие индикаторов анкеты
            found_indicators = []
            for indicator in profile_indicators:
                if indicator in recognized_text:
                    found_indicators.append(indicator)
            
            # Дополнительная проверка - ищем цифры (возраст)
            import re
            if re.search(r'\b(1[8-9]|[2-9]\d)\b', recognized_text):  # Ищем возраст 18-99
                found_indicators.append("возраст_цифры")
            
            if found_indicators:
                logging.info(f"Обнаружена анкета (индикаторы: {found_indicators})")
                return True
            
            # Если анкету не нашли, считаем что это может быть кнопка или другой экран
            logging.info("Анкета не найдена, возможно нужно нажать кнопку")
            return False
            
        except Exception as e:
            logging.error(f"Ошибка при проверке анкеты: {e}")
            return False
    
    def rate_current_profile(self) -> bool:
        """Оценка текущей анкеты"""
        try:
            if not self.check_for_new_profile_smart():
                logging.warning("Анкета не найдена для оценки")
                return False
            
            # Генерируем оценку
            rating = self.generate_smart_rating()
            logging.info(f"Сгенерирована оценка: {rating}")
            
            # Вводим оценку
            self.type_message_human_like(rating)
            time.sleep(0.5)
            
            # Отправляем
            pyautogui.press('enter')
            time.sleep(2)
            
            logging.info(f"Отправлена оценка: {rating}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при оценке анкеты: {e}")
            return False
    
    def main_automation_loop(self) -> None:
        """Основной цикл автоматизации"""
        try:
            logging.info("Запуск основной программы автоматизации...")
            
            # Предварительные проверки
            if not self.find_telegram_window():
                logging.error("Telegram не найден. Пожалуйста, запустите Telegram.")
                return
            
            if not self.activate_telegram_window():
                logging.error("Не удалось активировать окно Telegram.")
                return
            
            # Начинаем сессию с ботом
            if not self.start_bot_session():
                logging.error("Не удалось начать сессию с ботом.")
                return
            
            # Находим и нажимаем кнопку оценки
            if not self.find_and_click_rate_button_smart():
                logging.error("Не удалось найти кнопку 'Оценивать'.")
                return
            
            logging.info("Начинаем цикл оценок...")
            
            # Основной цикл
            consecutive_errors = 0
            max_errors = 5
            
            while self.running:
                try:
                    if self.rate_current_profile():
                        consecutive_errors = 0
                        self.wait_realistic_interval()
                    else:
                        consecutive_errors += 1
                        logging.warning(f"Ошибка при оценке ({consecutive_errors}/{max_errors})")
                        
                        if consecutive_errors >= max_errors:
                            logging.error("Слишком много ошибок подряд, попытка восстановиться...")
                            if not self.find_and_click_rate_button_smart():
                                logging.error("Не удалось восстановиться, завершение работы")
                                break
                        
                        time.sleep(3)
                    
                    # Проверка на остановку
                    if keyboard.is_pressed(config.STOP_KEY):
                        logging.info(f"Нажата клавиша '{config.STOP_KEY}', остановка программы")
                        break
                        
                except KeyboardInterrupt:
                    logging.info("Получен сигнал прерывания, остановка программы")
                    break
                except Exception as e:
                    logging.error(f"Непредвиденная ошибка в цикле: {e}")
                    time.sleep(5)
            
        except Exception as e:
            logging.error(f"Критическая ошибка: {e}")
        finally:
            logging.info("Работа программы завершена")
    
    def stop_automation(self) -> None:
        """Остановка автоматизации"""
        self.running = False

def main():
    """Главная функция"""
    print("=" * 60)
    print("🤖 Автоматизация бота для знакомств Bibinto")
    print("=" * 60)
    print("📋 Инструкция по использованию:")
    print("1. ✅ Убедитесь, что Telegram запущен и вы вошли в аккаунт")
    print("2. ✅ Откройте чат с ботом @bibinto_bot")
    print("3. ✅ Убедитесь, что Tesseract OCR установлен и настроен")
    print("4. 🚀 Запустите эту программу")
    print("5. ⏹️  Нажмите '{}' для остановки программы".format(config.STOP_KEY))
    print("=" * 60)
    print("⚠️  Внимание: Программа будет управлять мышью и клавиатурой!")
    print("=" * 60)
    
    try:
        input("\nНажмите Enter для начала работы...")
        
        automator = TelegramBotAutomator()
        automator.main_automation_loop()
        
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        logging.error(f"Ошибка в главной функции: {e}")

if __name__ == "__main__":
    main()