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

# =========================================================
# BOT TOKEN
# =========================================================

BOT_TOKEN = "8862080298:AAEM63Kky4-YhO_eE_l6YwXl1ynzSVTXrHE"


# =========================================================
# CONVERSATION STATES
# =========================================================

NAME, LEVEL, DORM, YEAR_DEPARTMENT, USERNAME = range(5)

INQUIRY = 5


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📖 Qirāʾāt Registration",
                callback_data="qirat_register"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Any Question / Inquiry",
                callback_data="inquiry"
            )
        ],
        [
            InlineKeyboardButton(
                "🌸 About Jemma",
                callback_data="about_jemma"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 About Qirāʾāt",
                callback_data="about_qirat"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🌷 Assalamu Alaikum wa Rahmatullahi wa Barakatuh!\n\n"
        "Welcome to Muslim Sisters 4Kilo Bot 🌸\n\n"
        "How can we help you?",
        reply_markup=main_menu(),
    )


# =========================================================
# QIRĀʾĀT REGISTRATION
# =========================================================

async def start_registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📖 Qirāʾāt Registration\n\n"
        "Let's begin your registration 🌷\n\n"
        "What is your full name?\n\n"
        "You can type /cancel at any time to cancel."
    )

    return NAME


# =========================================================
# GET NAME
# =========================================================

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["name"] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton(
                "📗 Qaida",
                callback_data="level_qaida"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 Nazr",
                callback_data="level_nazr"
            )
        ],
        [
            InlineKeyboardButton(
                "🕌 Hifz",
                callback_data="level_hifz"
            )
        ],
    ]

    await update.message.reply_text(
        "What level of Qirāʾāt are you interested in?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return LEVEL


# =========================================================
# GET LEVEL
# =========================================================

async def get_level(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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


# =========================================================
# GET DORM
# =========================================================

async def get_dorm(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["dorm"] = update.message.text

    await update.message.reply_text(
        "🎓 Please enter your year and department.\n\n"
        "Example:\n"
        "2nd Year – Computer Science"
    )

    return YEAR_DEPARTMENT


# =========================================================
# GET YEAR & DEPARTMENT
# =========================================================

async def get_year_department(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["year_department"] = update.message.text

    await update.message.reply_text(
        "📱 Finally, please send your Telegram username.\n\n"
        "Example: @username"
    )

    return USERNAME


# =========================================================
# GET TELEGRAM USERNAME
# =========================================================

async def get_username(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
        "Your registration has been received.\n"
        "We will contact you regarding the Qirāʾāt program, "
        "in shā Allah. 🌸",
        reply_markup=main_menu(),
    )

    context.user_data.clear()

    return ConversationHandler.END


# =========================================================
# INQUIRY
# =========================================================

async def start_inquiry(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "❓ Any Question / Inquiry\n\n"
        "Feel free to ask us anything! 🌸\n\n"
        "You can ask about Jemma, academics, Qirāʾāt, "
        "campus life, activities, programs, or anything "
        "else you'd like to know.\n\n"
        "💬 Please type your question below.\n\n"
        "You can type /cancel to return to the main menu."
    )

    return INQUIRY


# =========================================================
# RECEIVE INQUIRY
# =========================================================

async def receive_inquiry(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    question = update.message.text

    await update.message.reply_text(
        "🌷 Jazakillahu khayran for your question!\n\n"
        "We have received your inquiry:\n\n"
        f"💬 {question}\n\n"
        "We will get back to you regarding your question, "
        "in shā Allah. 🤍",
        reply_markup=main_menu(),
    )

    context.user_data.clear()

    return ConversationHandler.END


# =========================================================
# ABOUT JEMMA
# =========================================================

async def show_about_jemma(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🌸 About 4Kilo Muslim Students Jemma\n\n"
        "بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ\n\n"

        "Jemma is a community of Muslim students at "
        "Addis Ababa University, 4 Kilo Campus, working "
        "to strengthen sisterhood through Deen and "
        "mutual support. 🤍\n\n"

        "🕌 DEEN & UNITY\n"
        "Helping Muslim students remain firm in their "
        "faith, strengthen their unity, and support "
        "one another.\n\n"

        "🤝 SISTERHOOD\n"
        "Creating a community where sisters learn, "
        "support, and grow together.\n\n"

        "🛡️ SUPPORT & RIGHTS\n"
        "Working together to address challenges and "
        "rights-related concerns faced by Muslim "
        "students because of their faith.\n\n"

        "📖 ISLAMIC LEARNING\n"
        "Coordinating beneficial Islamic learning "
        "opportunities for students through nearby "
        "masjids and other programs.\n\n"

        "🎓 ACADEMIC GROWTH\n"
        "Supporting sisters in their academic journey "
        "through mentorship, tutoring, study materials, "
        "and other initiatives.\n\n"

        "🌷 Together in Deen. Together in Sisterhood. "
        "Together in Growth.",

        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="back_menu"
                )
            ]
        ])
    )


# =========================================================
# ABOUT QIRĀʾĀT
# =========================================================

async def show_about_qirat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📖 About Qirāʾāt\n\n"
        "The Qirāʾāt program provides an opportunity "
        "for sisters to learn and improve their Qur'an "
        "recitation.\n\n"

        "Available levels:\n\n"
        "📗 Qaida\n"
        "📖 Nazr\n"
        "🕌 Hifz\n\n"

        "🌷 Learn • Recite • Improve\n\n"
        "May Allah make the Qur'an the light of our "
        "hearts. 🤲",

        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📝 Register for Qirāʾāt",
                    callback_data="qirat_register"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="back_menu"
                )
            ],
        ])
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    # -------------------------
    # ABOUT JEMMA
    # -------------------------

    if query.data == "about_jemma":

        await show_about_jemma(update, context)

    # -------------------------
    # ABOUT QIRĀʾĀT
    # -------------------------

    elif query.data == "about_qirat":

        await show_about_qirat(update, context)

    # -------------------------
    # BACK TO MAIN MENU
    # -------------------------

    elif query.data == "back_menu":

        await query.edit_message_text(
            "🌷 Welcome to Muslim Sisters 4Kilo Bot 🌸\n\n"
            "How can we help you?",
            reply_markup=main_menu(),
        )


# =========================================================
# CANCEL
# =========================================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Cancelled.\n\n"
        "You are back at the main menu. 🌸",
        reply_markup=main_menu(),
    )

    return ConversationHandler.END


# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(BOT_TOKEN).build()


    # -----------------------------------------------------
    # QIRĀʾĀT REGISTRATION CONVERSATION
    # -----------------------------------------------------

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
            CommandHandler("cancel", cancel)
        ],
    )


    # -----------------------------------------------------
    # INQUIRY CONVERSATION
    # -----------------------------------------------------

    inquiry_handler = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                start_inquiry,
                pattern="^inquiry$"
            )
        ],

        states={

            INQUIRY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_inquiry
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )


    # -----------------------------------------------------
    # START COMMAND
    # -----------------------------------------------------

    app.add_handler(
        CommandHandler("start", start)
    )


    # -----------------------------------------------------
    # QIRĀʾĀT REGISTRATION
    # -----------------------------------------------------

    app.add_handler(
        registration_handler
    )


    # -----------------------------------------------------
    # INQUIRY
    # -----------------------------------------------------

    app.add_handler(
        inquiry_handler
    )


    # -----------------------------------------------------
    # OTHER BUTTONS
    # -----------------------------------------------------

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )


    # -----------------------------------------------------
    # RUN BOT
    # -----------------------------------------------------

    print("Bot is running...")

    app.run_polling()


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    main()

