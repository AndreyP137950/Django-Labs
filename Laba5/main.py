import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from cbr_parser import get_currency_rate
"""

"""
# Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Константы для текста кнопок (Вариант 1: три заранее установленные валюты)
BTN_USD = "Курс USD"
BTN_EUR = "Курс EUR"
BTN_CNY = "Курс CNY"

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает и возвращает основную клавиатуру бота.
    Согласно требованиям, эмодзи не используются.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # Создаем кнопки
    btn1 = KeyboardButton(BTN_USD)
    btn2 = KeyboardButton(BTN_EUR)
    btn3 = KeyboardButton(BTN_CNY)
    
    # Добавляем кнопки на клавиатуру
    markup.add(btn1, btn2, btn3)
    return markup


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    """
    Обработчик команд /start и /help.
    Отправляет приветственное сообщение и показывает клавиатуру.
    """
    welcome_text = (
        "Здравствуйте! Это бот для получения информации о текущих курсах валют "
        "по данным Центрального банка Российской Федерации (ЦБ РФ).\n\n"
        "Выберите интересующую вас валюту, нажав на соответствующую кнопку ниже."
    )
    bot.send_message(
        chat_id=message.chat.id, 
        text=welcome_text, 
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda message: message.text in [BTN_USD, BTN_EUR, BTN_CNY])
def handle_currency_request(message: telebot.types.Message):
    """
    Обработчик нажатий на кнопки с валютами.
    Извлекает код валюты из текста кнопки и обращается к парсеру.
    """
    # Сообщаем пользователю, что запрос обрабатывается (чтобы бот не казался "зависшим")
    bot.send_message(message.chat.id, "Получаю актуальные данные...")
    
    # Определяем код валюты, отрезая слово "Курс " (первые 5 символов)
    currency_code = message.text[5:]
    
    # Получаем результат от нашего модуля парсинга
    result_text = get_currency_rate(currency_code)
    
    # Отправляем результат пользователю
    bot.send_message(message.chat.id, result_text)


@bot.message_handler(func=lambda message: True)
def handle_unknown_messages(message: telebot.types.Message):
    """
    Метод для обработки любых других текстовых сообщений, которые бот не распознает.
    """
    bot.send_message(
        chat_id=message.chat.id, 
        text="Пожалуйста, используйте кнопки для выбора валюты.",
        reply_markup=get_main_keyboard()
    )

if __name__ == '__main__':
    print("Бот запускается...")
    try:
        # Запуск постоянного опроса серверов Telegram
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")













"""
# Проверяем, ввел ли пользователь токен
if BOT_TOKEN == "ВАШ_ТОКЕН_ЗДЕСЬ":
    print("ВНИМАНИЕ: Вы не указали токен бота в файле config.py!")
    print("Пожалуйста, вставьте токен и перезапустите программу.")
    exit(1)"""