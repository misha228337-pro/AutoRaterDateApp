"""
Конфигурационный файл для автоматаизации бота
"""

# Настройки временных интервалов (в секундах)
MIN_RATING_INTERVAL = 5.0
MAX_RATING_INTERVAL = 7.0

# Настройки оценки
HIGH_RATING_MIN = 6
HIGH_RATING_MAX = 10
LOW_RATING_MIN = 1
LOW_RATING_MAX = 5
HIGH_RATING_PROBABILITY = 0.8  # 80% вероятность высокой оценки

# Настройки распознавания изображений
IMAGE_CONFIDENCE = 0.8
SEARCH_TIMEOUT = 10

# Настройки печати
MIN_CHAR_DELAY = 0.05
MAX_CHAR_DELAY = 0.15

# Настройки для Tesseract OCR
# Укажите путь к Tesseract, если он не в системной переменной PATH
TESSERACT_PATH = None  # Пример: r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Языки для распознавания текста
OCR_LANGUAGES = 'rus+eng'

# Ключевые слова для поиска элементов интерфейса
RATE_BUTTON_TEXT = "Оценивать"
PROFILE_INDICATORS = ["лет", "город", "ищу", "анкета", "возраст"]

# Настройки логирования
LOG_LEVEL = "INFO"
LOG_FILE = "bot_automator.log"

# Горячие клавиши
STOP_KEY = 'q'

# Настройки экрана
SCREENSHOT_QUALITY = 95