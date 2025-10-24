import pyautogui
import time
import random
import logging
import pytesseract
import keyboard
import psutil
import re
from typing import Optional, Tuple, List
import os
import config
from PIL import Image

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
            logging.info("Проверка, что окно Telegram активно...")
            
            # НЕ используем Alt+Tab - считаем, что пользователь уже в окне Telegram
            time.sleep(1)
            
            logging.info("Окно Telegram считается активным (пользователь должен быть в чате)")
            return True
                
        except Exception as e:
            logging.error(f"Ошибка при активации Telegram: {e}")
            return False
    
    def image_to_grayscale(self, image: Image.Image) -> Image.Image:
        """Преобразование изображения в градации серого через PIL"""
        return image.convert('L')
    
    def extract_text_from_image(self, image: Image.Image) -> str:
        """Извлечение текста из изображения через PIL и pytesseract"""
        try:
            gray_image = self.image_to_grayscale(image)
            text = pytesseract.image_to_string(gray_image, lang=config.OCR_LANGUAGES)
            return text
        except Exception as e:
            logging.error(f"Ошибка при извлечении текста: {e}")
            return ""
    
    def find_text_coordinates_simple(self, text: str) -> Optional[Tuple[int, int]]:
        """Упрощенный поиск текста без OpenCV"""
        try:
            screenshot = pyautogui.screenshot()
            recognized_text = self.extract_text_from_image(screenshot)
            
            if text.lower() in recognized_text.lower():
                logging.info(f"Текст '{text}' найден на экране")
                # Возвращаем центр экрана для простоты
                screen_width, screen_height = pyautogui.size()
                return (screen_width // 2, screen_height // 2)
            
            return None
            
        except Exception as e:
            logging.error(f"Ошибка при поиске текста '{text}': {e}")
            return None
    
    def click_text_simple(self, text: str) -> bool:
        """Упрощенный клик по тексту"""
        try:
            coordinates = self.find_text_coordinates_simple(text)
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
        base_interval = random.uniform(config.MIN_RATING_INTERVAL, config.MAX_RATING_INTERVAL)
        extra_delay = random.uniform(0, 2)
        total_interval = base_interval + extra_delay
        
        logging.info(f"Ожидание {total_interval:.1f} секунд...")
        time.sleep(total_interval)
    
    def check_for_profile_simple(self) -> bool:
        """Упрощенная проверка наличия анкеты через PIL"""
        try:
            screenshot = pyautogui.screenshot()
            recognized_text = self.extract_text_from_image(screenshot).lower()
            
            logging.info(f"Распознанный текст: {recognized_text[:200]}...")
            
            # Упрощенные индикаторы анкеты
            profile_indicators = ["лет", "год", "город", "ищу", "знакомства", "анкета", "photo", "фото"]
            
            found_indicators = [elem for elem in profile_indicators if elem in recognized_text]
            
            # Проверяем возраст
            if re.search(r'\b(1[8-9]|[2-9]\d)\b', recognized_text):
                found_indicators.append("возраст_цифры")
            
            if found_indicators:
                logging.info(f"Обнаружена анкета (индикаторы: {found_indicators})")
                return True
            
            logging.info("Анкета не найдена")
            return False
            
        except Exception as e:
            logging.error(f"Ошибка при проверке анкеты: {e}")
            return False
    
    def rate_current_profile(self) -> bool:
        """Оценка текущей анкеты"""
        try:
            if not self.check_for_profile_simple():
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
                            time.sleep(5)
                            consecutive_errors = 0
                        
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
    print("🤖 Автоматизация бота для знакомств Bibinto (МИНИМАЛЬНАЯ ВЕРСИЯ)")
    print("=" * 60)
    print("📋 Инструкция по использованию:")
    print("1. ✅ Убедитесь, что Telegram запущен и вы вошли в аккаунт")
    print("2. ✅ Откройте чат с ботом @bibinto_bot")
    print("3. ✅ Убедитесь, что Tesseract OCR установлен и настроен")
    print("4. 🚀 Запустите эту программу")
    print("5. ⏹️  Нажмите '{}' для остановки программы".format(config.STOP_KEY))
    print("=" * 60)
    print("⚠️  Внимание: Программа будет управлять мышью и клавиатурой!")
    print("🔧 Эта версия не использует OpenCV для упрощения установки")
    print("=" * 60)
    
    try:
        input("\nНажмите Enter для начала работы...")
        
        print("🔄 Переключаюсь на Telegram через Alt+Tab...")
        time.sleep(2)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        print("✅ Переключение выполнено, начинаю работу...")
        
        automator = TelegramBotAutomator()
        automator.main_automation_loop()
        
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        logging.error(f"Ошибка в главной функции: {e}")

if __name__ == "__main__":
    main()