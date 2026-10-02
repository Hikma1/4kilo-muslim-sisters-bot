from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = "8862080298:AAEM63Kky4-YhO_eE_l6YwXl1ynzSVTXrHE"

NAME, LEVEL, DORM, YEAR_DEPARTMENT, USERNAME = range(5)


# =========================
# MAIN MENU
# =========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📖 Qirāʾāt Registration", callback_data="qirat_register")],
        [InlineKeyboardButton("❓ Any Question / Inquiry", callback_data="inquiry")],
        [InlineKeyboardButton("🌸 About Jemma", callback_data="about_jemma")],
        [InlineKeyboardButton("📖 About Qirāʾāt", callback_data="about_qirat")],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌷 Assalamu Alaikum wa Rahmatullahi wa Barakatuh!\n\n"
        "Welcome to Muslim Sisters 4Kilo Bot 🌸\n\n"
        "How can we help you?",
        reply_markup=main_menu(),
    )


# =========================
# QIRĀʾĀT REGISTRATION
# =========================

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📖 Qirāʾāt Registration\n\n"
        "Let's begin your registration 🌷\n\n"
        "What is your full name?"
    )

    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("📗 Qaida", callback_data="level_qaida")],
        [InlineKeyboardButton("📖 Nazr", callback_data="level_nazr")],
        [InlineKeyboardButton("🕌 Hifz", callback_data="level_hifz")],
    ]

    await update.message.reply_text(
        "What level of Qirāʾāt are you interested in?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return LEVEL


async def get_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    levels = {
        "level_qaida": "Qaida",
        "level_nazr": "Nazr",
        "level_hifz": "Hifz",
    }

    context.user_data["level"] = levels[query.data]

    await query.edit_message_text(
        "🏠 What is your dorm number?"
    )

    return DORM


async def get_dorm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["dorm"] = update.message.text

    await update.message.reply_text(
        "🎓 Please enter your year and department.\n\n"
        "Example: 2nd Year – Computer Science"
    )

    return YEAR_DEPARTMENT


async def get_year_department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["year_department"] = update.message.text

    await update.message.reply_text(
        "📱 Finally, please send your Telegram username.\n\n"
        "Example: @username"
    )

    return USERNAME


async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text

    data = context.user_data

    await update.message.reply_text(
        "🌷 Jazakillahu khayran for registering!\n\n"
        "Your registration information:\n\n"
        f"👤 Name: {data['name']}\n"
        f"📖 Level: {data['level']}\n"
        f"🏠 Dorm: {data['dorm']}\n"
        f"🎓 Year & Department: {data['year_department']}\n"
        f"📱 Telegram: {data['username']}\n\n"
        "Your registration has been received. "
        "We will contact you regarding the Qirāʾāt program, "
        "in shā Allah. 🌸",
        reply_markup=main_menu(),
    )

    context.user_data.clear()

    return ConversationHandler.END


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "inquiry":

        keyboard = [
            [InlineKeyboardButton("🎓 Academic", callback_data="inquiry_academic")],
            [InlineKeyboardButton("🌸 Jemma", callback_data="inquiry_jemma")],
            [InlineKeyboardButton("📖 Kitab", callback_data="inquiry_kitab")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu")],
        ]

        await query.edit_message_text(
            "❓ What is your inquiry about?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "inquiry_academic":

        await query.edit_message_text(
            "🎓 Academic Inquiry\n\n"
            "For academic-related questions, please contact "
            "the responsible sister through the official Jemma contact.\n\n"
            "🔙 Use /start to return to the main menu."
        )

    elif query.data == "inquiry_jemma":

        await query.edit_message_text(
            "🌸 Jemma Inquiry\n\n"
            "For questions about Jemma, its activities, "
            "or programs, please contact the responsible sister.\n\n"
            "🔙 Use /start to return to the main menu."
        )

    elif query.data == "inquiry_kitab":

        await query.edit_message_text(
            "📖 Kitab Inquiry\n\n"
            "For Kitab-related questions, please contact "
            "the responsible sister.\n\n"
            "🔙 Use /start to return to the main menu."
        )

    elif query.data == "back_menu":

        await query.edit_message_text(
            "🌷 Welcome to Muslim Sisters 4Kilo Bot 🌸\n\n"
            "How can we help you?",
            reply_markup=main_menu(),
        )

    elif query.data == "about_jemma":

        await query.edit_message_text(
            "🌸 About 4Kilo Muslim Students Jemma\n\n"
            "More information about Jemma will be available here.\n\n"
            "🔙 Use /start to return to the main menu."
        )

    elif query.data == "about_qirat":

        await query.edit_message_text(
            "📖 About Qirāʾāt\n\n"
            "Information about the Qirāʾāt program will be available here.\n\n"
            "🔙 Use /start to return to the main menu."
        )


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    registration_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_registration,
                pattern="^qirat_register$"
            )
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],

            LEVEL: [
                CallbackQueryHandler(
                    get_level,
                    pattern="^level_(qaida|nazr|hifz)$"
                )
            ],

            DORM: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_dorm
                )
            ],

            YEAR_DEPARTMENT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_year_department
                )
            ],

            USERNAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_username
                )
            ],
        },

        fallbacks=[
            CommandHandler("start", start)
        ],
    )

    app.add_handler(CommandHandler("start", start))

    app.add_handler(registration_handler)

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()