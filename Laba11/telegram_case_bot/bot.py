"""Telegram-бот для лабораторной работы №11.

Бот реализует мини CASE-систему через команды:
- выбор F1/F2/F3,
- расчет y = F1(F2(F3(x))),
- генерация VBA-кода.
"""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .functions import FUNCTIONS, calculate_chain, human_formula
from .storage import UserConfigStore
from .vba_generator import generate_vba_code


HELP_TEXT = (
    "Доступные команды:\n"
    "/start - запуск и краткая инструкция\n"
    "/help - показать справку\n"
    "/show - показать текущую конфигурацию F1/F2/F3\n"
    "/setf1 <sqrt|reciprocal|exp> - выбрать F1\n"
    "/setf2 <sqrt|reciprocal|exp> - выбрать F2\n"
    "/setf3 <sqrt|reciprocal|exp> - выбрать F3\n"
    "/calc <x> - вычислить y = F1(F2(F3(x)))\n"
    "/code - сгенерировать VBA код\n\n"
    "Также можно работать кнопками внизу чата."
)


BTN_SHOW = "Показать конфигурацию"
BTN_F1 = "Выбрать F1"
BTN_F2 = "Выбрать F2"
BTN_F3 = "Выбрать F3"
BTN_CALC = "Вычислить"
BTN_CODE = "Сгенерировать VBA"
BTN_HELP = "Помощь"


class CaseBot:
    """Инкапсулирует приложение Telegram-бота и его обработчики."""

    def __init__(self, token: str) -> None:
        self._store = UserConfigStore()
        self._app = Application.builder().token(token).build()
        self._register_handlers()

    @property
    def app(self) -> Application:
        """Возвращает объект Application для запуска/тестирования."""
        return self._app

    def _register_handlers(self) -> None:
        """Регистрирует все команды бота."""
        self._app.add_handler(CommandHandler("start", self.start))
        self._app.add_handler(CommandHandler("help", self.help))
        self._app.add_handler(CommandHandler("show", self.show))
        self._app.add_handler(CommandHandler("setf1", self.setf1))
        self._app.add_handler(CommandHandler("setf2", self.setf2))
        self._app.add_handler(CommandHandler("setf3", self.setf3))
        self._app.add_handler(CommandHandler("calc", self.calc))
        self._app.add_handler(CommandHandler("code", self.code))
        self._app.add_handler(CallbackQueryHandler(self.on_callback, pattern=r"^set:f[123]:(sqrt|reciprocal|exp)$"))
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_text))

    @staticmethod
    def _main_keyboard() -> ReplyKeyboardMarkup:
        """Создает нижнюю клавиатуру с основными операциями."""
        return ReplyKeyboardMarkup(
            keyboard=[
                [BTN_SHOW, BTN_HELP],
                [BTN_F1, BTN_F2, BTN_F3],
                [BTN_CALC, BTN_CODE],
            ],
            resize_keyboard=True,
        )

    @staticmethod
    def _function_keyboard(func_position: str) -> InlineKeyboardMarkup:
        """Создает inline-клавиатуру выбора функции для F1/F2/F3."""
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("sqrt", callback_data=f"set:{func_position}:sqrt")],
                [
                    InlineKeyboardButton(
                        "reciprocal", callback_data=f"set:{func_position}:reciprocal"
                    )
                ],
                [InlineKeyboardButton("exp", callback_data=f"set:{func_position}:exp")],
            ]
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Приветствие и минимальная инструкция."""
        user_id = update.effective_user.id
        cfg = self._store.get(user_id)
        context.user_data["await_x"] = False
        text = (
            "Мини CASE-система запущена.\n"
            f"Текущая формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}\n\n"
            "Выберите действие кнопками внизу или командами."
        )
        await update.message.reply_text(text, reply_markup=self._main_keyboard())

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Выводит список команд."""
        await update.message.reply_text(HELP_TEXT, reply_markup=self._main_keyboard())

    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Показывает выбранные функции пользователя."""
        user_id = update.effective_user.id
        cfg = self._store.get(user_id)
        await update.message.reply_text(
            "Текущая конфигурация:\n"
            f"F1 = {cfg.f1}\n"
            f"F2 = {cfg.f2}\n"
            f"F3 = {cfg.f3}\n"
            f"Формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}"
        )

    async def _show_for_user(self, update: Update) -> None:
        """Показывает текущую конфигурацию в ответ на кнопки и callback."""
        user_id = update.effective_user.id
        cfg = self._store.get(user_id)
        await update.effective_message.reply_text(
            "Текущая конфигурация:\n"
            f"F1 = {cfg.f1}\n"
            f"F2 = {cfg.f2}\n"
            f"F3 = {cfg.f3}\n"
            f"Формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}"
        )

    async def _set_function(self, update: Update, func_position: str, value: str) -> None:
        """Общая логика выбора функции для F1/F2/F3."""
        if value not in FUNCTIONS:
            await update.effective_message.reply_text(
                "Неверное значение. Допустимо: sqrt, reciprocal, exp"
            )
            return

        cfg = self._store.get(update.effective_user.id)
        if func_position == "f1":
            cfg.f1 = value
        elif func_position == "f2":
            cfg.f2 = value
        else:
            cfg.f3 = value

        await update.effective_message.reply_text(
            f"Установлено {func_position.upper()} = {value}\n"
            f"Новая формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}"
        )

    async def setf1(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Устанавливает функцию F1."""
        if not context.args:
            await update.message.reply_text("Использование: /setf1 <sqrt|reciprocal|exp>")
            return
        await self._set_function(update, "f1", context.args[0].strip())

    async def setf2(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Устанавливает функцию F2."""
        if not context.args:
            await update.message.reply_text("Использование: /setf2 <sqrt|reciprocal|exp>")
            return
        await self._set_function(update, "f2", context.args[0].strip())

    async def setf3(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Устанавливает функцию F3."""
        if not context.args:
            await update.message.reply_text("Использование: /setf3 <sqrt|reciprocal|exp>")
            return
        await self._set_function(update, "f3", context.args[0].strip())

    async def calc(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Вычисляет значение цепочки для заданного x."""
        if not context.args:
            await update.message.reply_text("Использование: /calc <число>")
            return

        try:
            x = float(context.args[0])
        except ValueError:
            await update.message.reply_text("Ошибка: x должен быть числом.")
            return

        cfg = self._store.get(update.effective_user.id)
        result = calculate_chain(cfg.f1, cfg.f2, cfg.f3, x)
        if result.error:
            await update.message.reply_text(result.error)
            return

        steps = "\n".join(result.steps)
        await update.message.reply_text(
            f"Формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}\n"
            f"Результат: {result.value:.6f}\n\n"
            f"Шаги:\n{steps}"
        )

    async def _calc_with_value(self, update: Update, x: float) -> None:
        """Вычисляет выражение для переданного x (используется при кнопочном режиме)."""
        cfg = self._store.get(update.effective_user.id)
        result = calculate_chain(cfg.f1, cfg.f2, cfg.f3, x)
        if result.error:
            await update.effective_message.reply_text(result.error)
            return

        steps = "\n".join(result.steps)
        await update.effective_message.reply_text(
            f"Формула: {human_formula(cfg.f1, cfg.f2, cfg.f3)}\n"
            f"Результат: {result.value:.6f}\n\n"
            f"Шаги:\n{steps}"
        )

    async def code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Генерирует и отправляет VBA код в сообщении."""
        cfg = self._store.get(update.effective_user.id)
        code = generate_vba_code(cfg.f1, cfg.f2, cfg.f3)

        # Telegram ограничивает длину одного сообщения, поэтому делим код на части.
        max_chunk = 3500
        for i in range(0, len(code), max_chunk):
            chunk = code[i : i + max_chunk]
            await update.message.reply_text(chunk)

    async def on_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает нажатия inline-кнопок выбора F1/F2/F3."""
        query = update.callback_query
        await query.answer()

        _, func_position, value = query.data.split(":")
        await self._set_function(update, func_position, value)

    async def on_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает текст кнопок и режим ожидания значения x."""
        text = (update.message.text or "").strip()

        if context.user_data.get("await_x"):
            try:
                x = float(text)
            except ValueError:
                await update.message.reply_text(
                    "Нужно ввести число. Пример: 2 или 0.5"
                )
                return

            context.user_data["await_x"] = False
            await self._calc_with_value(update, x)
            return

        if text == BTN_SHOW:
            await self._show_for_user(update)
            return

        if text == BTN_HELP:
            await self.help(update, context)
            return

        if text == BTN_F1:
            await update.message.reply_text(
                "Выберите функцию для F1:",
                reply_markup=self._function_keyboard("f1"),
            )
            return

        if text == BTN_F2:
            await update.message.reply_text(
                "Выберите функцию для F2:",
                reply_markup=self._function_keyboard("f2"),
            )
            return

        if text == BTN_F3:
            await update.message.reply_text(
                "Выберите функцию для F3:",
                reply_markup=self._function_keyboard("f3"),
            )
            return

        if text == BTN_CALC:
            context.user_data["await_x"] = True
            await update.message.reply_text("Введите значение x числом:")
            return

        if text == BTN_CODE:
            await self.code(update, context)
            return


def run_bot(token: str) -> None:
    """Запускает long-polling Telegram-бота."""
    case_bot = CaseBot(token)
    case_bot.app.run_polling()
