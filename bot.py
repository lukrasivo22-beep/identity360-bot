"""
Бот «Идентичность 360°» — Распаковка личности и образа
Автор: создан для нутрициолога и партнёра Beverly/Shiseido
"""

import logging
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

# ─────────────────────────────────────────────
#  НАСТРОЙКИ — ЗАПОЛНИ ЭТИ ДВА ПОЛЯ
# ─────────────────────────────────────────────
BOT_TOKEN = "8704701412:AAGeAAllxQORN71IJXeslQZSPPY1EG1JHdQ"        # Вставь токен от @BotFather
ADMIN_CHAT_ID = "1689805437"       # Вставь свой числовой ID от @userinfobot

# Путь к файлу с ответами (создаётся автоматически)
ANSWERS_FILE = "answers.txt"

# ─────────────────────────────────────────────
#  ШАГИ ДИАЛОГА
# ─────────────────────────────────────────────
(
    B1_NAME, B1_AGE, B1_CITY, B1_WORK, B1_DAY, B1_CHILDREN,
    B2_ROLES, B2_MAIN_ROLE, B2_SELF, B2_DREAM_ROLE, B2_WORDS,
    B3_VALUES, B3_INSPIRE, B3_DRAIN, B3_IDOL, B3_DREAM,
    B4_STYLE_NOW, B4_STYLE_DREAM, B4_COLORS, B4_FORMAL, B4_BEST,
    B4_HATE, B4_BRANDS,
    B5_ENERGY, B5_DROPS, B5_FOOD, B5_APPEARANCE, B5_SUPPS, B5_RECOVERY,
    B6_REQUEST, B6_RESULT, B6_FEARS, B6_FORMAT,
    B7_PHOTOS_SELF, B7_PHOTOS_STYLE, B7_PHOTOS_NO,
    DONE
) = range(37)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def save_answer(user_id: str, username: str, question: str, answer: str):
    """Сохраняет ответ в текстовый файл."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{timestamp}] {user_id} (@{username}) | {question}: {answer}\n"
    with open(ANSWERS_FILE, "a", encoding="utf-8") as f:
        f.write(line)

async def send_to_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    """Отправляет сообщение тебе (администратору)."""
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение администратору: {e}")

def get_user_info(update: Update):
    user = update.effective_user
    return str(user.id), user.username or "нет username"

def yn_keyboard():
    return ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True, one_time_keyboard=True)

def remove_keyboard():
    return ReplyKeyboardRemove()

# ─────────────────────────────────────────────
#  СТАРТ
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user_id, username = get_user_info(update)

    await update.message.reply_text(
        "✨ Привет! Я помогу тебе пройти глубокую *Распаковку личности и образа*.\n\n"
        "Это займёт несколько дней в удобном для тебя темпе — без спешки.\n\n"
        "По итогам ты получишь:\n"
        "💎 Описание твоего архетипа\n"
        "👗 Рекомендации по стилю и образу\n"
        "🌿 Нутри-анализ твоей внешности и энергии\n"
        "🖼 AI-визуализацию твоего нового образа\n\n"
        "Готова начать? Поехали! 🚀\n\n"
        "*Блок 1 из 7 — О себе*",
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )

    await update.message.reply_text("Как тебя зовут? (Имя и фамилия)")
    return B1_NAME

# ─────────────────────────────────────────────
#  БЛОК 1 — О СЕБЕ
# ─────────────────────────────────────────────

async def b1_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    context.user_data["name"] = update.message.text
    save_answer(uid, uname, "Имя", update.message.text)
    await update.message.reply_text("Сколько тебе лет?")
    return B1_AGE

async def b1_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Возраст", update.message.text)
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Из какого ты города и страны?")
    return B1_CITY

async def b1_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Город/Страна", update.message.text)
    await update.message.reply_text(
        "Кем ты работаешь или чем занимаешься?\n"
        "Если есть свой бизнес — расскажи коротко."
    )
    return B1_WORK

async def b1_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Работа/Бизнес", update.message.text)
    await update.message.reply_text(
        "Опиши свой обычный день — от утра до вечера.\n"
        "Несколько предложений, как ты его проживаешь."
    )
    return B1_DAY

async def b1_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Обычный день", update.message.text)
    await update.message.reply_text(
        "Есть ли у тебя дети или внуки?\n"
        "Если да — как это влияет на твой образ жизни?"
    )
    return B1_CHILDREN

async def b1_children(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Дети/Внуки", update.message.text)

    await update.message.reply_text(
        "Отлично! Переходим ко второму блоку 💫\n\n"
        "*Блок 2 из 7 — Роли и самоощущение*\n\n"
        "В каких ролях ты сейчас живёшь?\n"
        "Например: мама, руководитель, жена, эксперт, предприниматель...\n"
        "Перечисли все, которые актуальны.",
        parse_mode="Markdown"
    )
    return B2_ROLES

# ─────────────────────────────────────────────
#  БЛОК 2 — РОЛИ И САМООЩУЩЕНИЕ
# ─────────────────────────────────────────────

async def b2_roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Роли", update.message.text)
    await update.message.reply_text(
        "Какая из этих ролей для тебя сейчас главная?\n"
        "И комфортно ли тебе в ней?"
    )
    return B2_MAIN_ROLE

async def b2_main_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Главная роль", update.message.text)
    await update.message.reply_text(
        "Как ты ощущаешь себя изнутри?\n"
        "И совпадает ли это с тем, как тебя видят другие?"
    )
    return B2_SELF

async def b2_self(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Самоощущение vs восприятие других", update.message.text)
    await update.message.reply_text(
        "Есть ли роль, в которой ты хотела бы быть,\n"
        "но пока не решаешься?"
    )
    return B2_DREAM_ROLE

async def b2_dream_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Желаемая роль", update.message.text)
    await update.message.reply_text(
        "Назови три слова, которыми ты бы описала себя *сейчас*.\n"
        "И три слова — какой ты хочешь быть *в идеале*.",
        parse_mode="Markdown"
    )
    return B2_WORDS

async def b2_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Слова о себе (сейчас/идеал)", update.message.text)

    keyboard = ReplyKeyboardMarkup(
        [["Семья", "Карьера", "Свобода"],
         ["Здоровье", "Деньги", "Признание"],
         ["Развитие", "Красота", "Покой"],
         ["Влияние", "Другое (напишу сама)"]],
        resize_keyboard=True, one_time_keyboard=False
    )
    await update.message.reply_text(
        "Замечательно! Следующий блок 🌟\n\n"
        "*Блок 3 из 7 — Ценности и жизненные ориентиры*\n\n"
        "Что для тебя самое важное в жизни прямо сейчас?\n"
        "Выбери 3–5 из списка или напиши своё.\n"
        "Когда выберешь всё нужное — напиши *Готово*.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    context.user_data["values"] = []
    return B3_VALUES

# ─────────────────────────────────────────────
#  БЛОК 3 — ЦЕННОСТИ
# ─────────────────────────────────────────────

async def b3_values(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    text = update.message.text

    if text.lower() == "готово":
        values_str = ", ".join(context.user_data.get("values", []))
        save_answer(uid, uname, "Ценности", values_str)
        await update.message.reply_text(
            "Что тебя вдохновляет и даёт энергию?",
            reply_markup=remove_keyboard()
        )
        return B3_INSPIRE
    else:
        context.user_data.setdefault("values", []).append(text)
        await update.message.reply_text(
            f"✅ Добавила: {text}\nВыбирай ещё или напиши *Готово*.",
            parse_mode="Markdown"
        )
        return B3_VALUES

async def b3_inspire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Источники вдохновения", update.message.text)
    await update.message.reply_text("Что тебя, наоборот, забирает силы?\nЧего хочется меньше в жизни?")
    return B3_DRAIN

async def b3_drain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Что забирает силы", update.message.text)
    await update.message.reply_text(
        "Есть ли у тебя женщина-ориентир?\n"
        "(реальная или публичная)\n"
        "Чем она тебя привлекает?"
    )
    return B3_IDOL

async def b3_idol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Женщина-ориентир", update.message.text)
    await update.message.reply_text(
        "Если бы деньги и время не были ограничением —\n"
        "как бы выглядела твоя жизнь через 3 года?"
    )
    return B3_DREAM

async def b3_dream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Мечта через 3 года", update.message.text)

    await update.message.reply_text(
        "Прекрасно! Переходим к образу 👗\n\n"
        "*Блок 4 из 7 — Стиль и внешний образ*\n\n"
        "Как бы ты описала свой нынешний стиль в одежде?",
        parse_mode="Markdown"
    )
    return B4_STYLE_NOW

# ─────────────────────────────────────────────
#  БЛОК 4 — СТИЛЬ
# ─────────────────────────────────────────────

async def b4_style_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Нынешний стиль", update.message.text)
    await update.message.reply_text(
        "Есть ли стиль, который тебя привлекает,\n"
        "но ты пока его «не решаешься» носить?\n"
        "Почему?"
    )
    return B4_STYLE_DREAM

async def b4_style_dream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Желаемый стиль", update.message.text)
    await update.message.reply_text(
        "Какие цвета в одежде ты носишь чаще всего?\n"
        "Есть ли цвета, которых ты избегаешь?"
    )
    return B4_COLORS

async def b4_colors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Цвета в одежде", update.message.text)
    await update.message.reply_text(
        "Как ты обычно одеваешься на важную встречу или переговоры?\n"
        "А в выходной день?"
    )
    return B4_FORMAL

async def b4_formal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Стиль на встречу / выходной", update.message.text)
    await update.message.reply_text(
        "Есть ли вещь в гардеробе, в которой ты чувствуешь себя\n"
        "лучшей версией себя? Опиши её."
    )
    return B4_BEST

async def b4_best(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Любимая вещь в гардеробе", update.message.text)
    await update.message.reply_text("Что тебя раздражает в своём гардеробе прямо сейчас?")
    return B4_HATE

async def b4_hate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Что раздражает в гардеробе", update.message.text)
    await update.message.reply_text(
        "Какие бренды ты носишь?\n"
        "Есть ли бренды мечты?"
    )
    return B4_BRANDS

async def b4_brands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Бренды", update.message.text)

    await update.message.reply_text(
        "Половина пути позади — ты молодец! 💪\n\n"
        "*Блок 5 из 7 — Здоровье, энергия и самочувствие*\n\n"
        "Как бы ты оценила свою энергию в течение дня\n"
        "по шкале от 1 до 10?",
        parse_mode="Markdown"
    )
    return B5_ENERGY

# ─────────────────────────────────────────────
#  БЛОК 5 — ЗДОРОВЬЕ
# ─────────────────────────────────────────────

async def b5_energy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Уровень энергии (1-10)", update.message.text)
    await update.message.reply_text(
        "Есть ли моменты в дне, когда энергия резко падает?\n"
        "Если да — когда именно?"
    )
    return B5_DROPS

async def b5_drops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Спады энергии", update.message.text)
    await update.message.reply_text(
        "Как ты питаешься?\n"
        "Есть ли режим или «как получится»?"
    )
    return B5_FOOD

async def b5_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Питание", update.message.text)
    await update.message.reply_text(
        "Есть ли что-то во внешности, что тебя беспокоит\n"
        "и что ты связываешь со здоровьем?\n"
        "Например: кожа, волосы, вес, отёчность, усталый вид..."
    )
    return B5_APPEARANCE

async def b5_appearance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Беспокойства по внешности", update.message.text)
    await update.message.reply_text(
        "Принимаешь ли ты сейчас какие-то добавки или витамины?\n"
        "Если да — какие и зачем?"
    )
    return B5_SUPPS

async def b5_supps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Добавки и витамины", update.message.text)
    await update.message.reply_text(
        "Как ты восстанавливаешься после нагрузок?\n"
        "Сон, спорт, отдых, ритуалы — расскажи."
    )
    return B5_RECOVERY

async def b5_recovery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Восстановление", update.message.text)

    await update.message.reply_text(
        "Почти финиш! 🌟\n\n"
        "*Блок 6 из 7 — Твой запрос и ожидания*\n\n"
        "Что тебя привело сюда?\n"
        "Что хочешь изменить или получить в первую очередь?",
        parse_mode="Markdown"
    )
    return B6_REQUEST

# ─────────────────────────────────────────────
#  БЛОК 6 — ЗАПРОС
# ─────────────────────────────────────────────

async def b6_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Запрос (зачем пришла)", update.message.text)
    await update.message.reply_text(
        "Что для тебя будет результатом этой работы?\n"
        "Как ты поймёшь, что всё прошло хорошо?"
    )
    return B6_RESULT

async def b6_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Ожидаемый результат", update.message.text)
    await update.message.reply_text(
        "Есть ли что-то, чего ты боишься или о чём\n"
        "хочешь предупредить заранее?"
    )
    return B6_FEARS

async def b6_fears(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Страхи/Предупреждения", update.message.text)

    keyboard = ReplyKeyboardMarkup(
        [["Чёткие инструкции", "Исследовать вместе"]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "Как тебе комфортнее работать?",
        reply_markup=keyboard
    )
    return B6_FORMAT

async def b6_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    save_answer(uid, uname, "Формат работы", update.message.text)

    await update.message.reply_text(
        "И последний блок — самый визуальный! 📸\n\n"
        "*Блок 7 из 7 — Фото для AI-визуализации образа*\n\n"
        "Пришли 2–3 своих фото в полный рост.\n"
        "Любые, где тебе нравится как ты выглядишь.\n\n"
        "Когда отправишь все фото — напиши *Готово*.",
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )
    context.user_data["photos_self"] = []
    return B7_PHOTOS_SELF

# ─────────────────────────────────────────────
#  БЛОК 7 — ФОТО
# ─────────────────────────────────────────────

async def b7_photos_self(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)

    if update.message.photo:
        context.user_data.setdefault("photos_self", []).append("получено")
        count = len(context.user_data["photos_self"])
        await update.message.reply_text(f"✅ Фото {count} получено! Можешь прислать ещё или напиши *Готово*.", parse_mode="Markdown")
        return B7_PHOTOS_SELF
    elif update.message.text and update.message.text.lower() == "готово":
        count = len(context.user_data.get("photos_self", []))
        save_answer(uid, uname, "Фото себя (кол-во)", str(count))
        await update.message.reply_text(
            "Теперь пришли 3–5 фото образов или стилей,\n"
            "которые тебя привлекают.\n"
            "Это могут быть картинки из Pinterest, Instagram — любые.\n\n"
            "Когда отправишь — напиши *Готово*.",
            parse_mode="Markdown"
        )
        context.user_data["photos_style"] = []
        return B7_PHOTOS_STYLE
    else:
        await update.message.reply_text("Пришли фото или напиши *Готово* чтобы продолжить.", parse_mode="Markdown")
        return B7_PHOTOS_SELF

async def b7_photos_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)

    if update.message.photo:
        context.user_data.setdefault("photos_style", []).append("получено")
        count = len(context.user_data["photos_style"])
        await update.message.reply_text(f"✅ Фото {count} получено!", parse_mode="Markdown")
        return B7_PHOTOS_STYLE
    elif update.message.text and update.message.text.lower() == "готово":
        count = len(context.user_data.get("photos_style", []))
        save_answer(uid, uname, "Фото образов (кол-во)", str(count))
        await update.message.reply_text(
            "Последнее — пришли 1–3 образа,\n"
            "которые тебе категорически *не нравятся*.\n"
            "Это тоже очень важно для точного разбора!\n\n"
            "Когда отправишь — напиши *Готово*.",
            parse_mode="Markdown"
        )
        context.user_data["photos_no"] = []
        return B7_PHOTOS_NO
    else:
        await update.message.reply_text("Пришли фото или напиши *Готово*.", parse_mode="Markdown")
        return B7_PHOTOS_STYLE

async def b7_photos_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)

    if update.message.photo:
        context.user_data.setdefault("photos_no", []).append("получено")
        count = len(context.user_data["photos_no"])
        await update.message.reply_text(f"✅ Фото {count} получено!")
        return B7_PHOTOS_NO
    elif update.message.text and update.message.text.lower() == "готово":
        count = len(context.user_data.get("photos_no", []))
        save_answer(uid, uname, "Фото антиобразов (кол-во)", str(count))
        return await finish(update, context)
    else:
        await update.message.reply_text("Пришли фото или напиши *Готово*.")
        return B7_PHOTOS_NO

# ─────────────────────────────────────────────
#  ФИНИШ — отправка карточки администратору
# ─────────────────────────────────────────────

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, uname = get_user_info(update)
    name = context.user_data.get("name", "Не указано")
    age = context.user_data.get("age", "—")

    # Сообщение клиентке
    await update.message.reply_text(
        f"🎉 *{name}, ты завершила распаковку!*\n\n"
        "Все твои ответы получены.\n\n"
        "Я изучу их внимательно и подготовлю твой персональный разбор:\n"
        "💎 Архетип и описание твоей личности\n"
        "👗 Рекомендации по стилю и образу\n"
        "🌿 Нутри-анализ и рекомендации по здоровью\n"
        "🖼 AI-визуализацию твоего нового образа\n\n"
        "Ожидай — я напишу тебе в течение 2–3 дней 🌟",
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )

    # Уведомление администратору
    admin_text = (
        f"🔔 *НОВАЯ РАСПАКОВКА ЗАВЕРШЕНА*\n\n"
        f"👤 Имя: {name}\n"
        f"🎂 Возраст: {age}\n"
        f"📱 Username: @{uname}\n"
        f"🆔 ID: {uid}\n"
        f"🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"Все ответы сохранены в файл answers.txt\n"
        f"Можешь начинать разбор! 💎"
    )
    await send_to_admin(context, admin_text)

    return ConversationHandler.END

# ─────────────────────────────────────────────
#  ОТМЕНА
# ─────────────────────────────────────────────

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Распаковка приостановлена. Напиши /start чтобы начать заново.",
        reply_markup=remove_keyboard()
    )
    return ConversationHandler.END

# ─────────────────────────────────────────────
#  ЗАПУСК БОТА
# ─────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            B1_NAME:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_name)],
            B1_AGE:         [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_age)],
            B1_CITY:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_city)],
            B1_WORK:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_work)],
            B1_DAY:         [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_day)],
            B1_CHILDREN:    [MessageHandler(filters.TEXT & ~filters.COMMAND, b1_children)],
            B2_ROLES:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b2_roles)],
            B2_MAIN_ROLE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, b2_main_role)],
            B2_SELF:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b2_self)],
            B2_DREAM_ROLE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, b2_dream_role)],
            B2_WORDS:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b2_words)],
            B3_VALUES:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b3_values)],
            B3_INSPIRE:     [MessageHandler(filters.TEXT & ~filters.COMMAND, b3_inspire)],
            B3_DRAIN:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b3_drain)],
            B3_IDOL:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b3_idol)],
            B3_DREAM:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b3_dream)],
            B4_STYLE_NOW:   [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_style_now)],
            B4_STYLE_DREAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_style_dream)],
            B4_COLORS:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_colors)],
            B4_FORMAL:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_formal)],
            B4_BEST:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_best)],
            B4_HATE:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_hate)],
            B4_BRANDS:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b4_brands)],
            B5_ENERGY:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_energy)],
            B5_DROPS:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_drops)],
            B5_FOOD:        [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_food)],
            B5_APPEARANCE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_appearance)],
            B5_SUPPS:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_supps)],
            B5_RECOVERY:    [MessageHandler(filters.TEXT & ~filters.COMMAND, b5_recovery)],
            B6_REQUEST:     [MessageHandler(filters.TEXT & ~filters.COMMAND, b6_request)],
            B6_RESULT:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b6_result)],
            B6_FEARS:       [MessageHandler(filters.TEXT & ~filters.COMMAND, b6_fears)],
            B6_FORMAT:      [MessageHandler(filters.TEXT & ~filters.COMMAND, b6_format)],
            B7_PHOTOS_SELF: [
                MessageHandler(filters.PHOTO, b7_photos_self),
                MessageHandler(filters.TEXT & ~filters.COMMAND, b7_photos_self),
            ],
            B7_PHOTOS_STYLE: [
                MessageHandler(filters.PHOTO, b7_photos_style),
                MessageHandler(filters.TEXT & ~filters.COMMAND, b7_photos_style),
            ],
            B7_PHOTOS_NO: [
                MessageHandler(filters.PHOTO, b7_photos_no),
                MessageHandler(filters.TEXT & ~filters.COMMAND, b7_photos_no),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    print("✅ Бот запущен! Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
