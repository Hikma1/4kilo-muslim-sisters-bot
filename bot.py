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
from telegram.error import TelegramError


# =========================================================
# BOT SETTINGS
# =========================================================

BOT_TOKEN = "YOUR_NEW_TOKEN"

# Put your Telegram numeric Chat ID here
ADMIN_CHAT_ID = 123456789


# =========================================================
# CONVERSATION STATES
# =========================================================

NAME, LEVEL, DORM, YEAR_DEPARTMENT, USERNAME = range(5)

INQUIRY = 5

ADMIN_REPLY = 6


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

    telegram_user = update.effective_user

    telegram_id = telegram_user.id
    telegram_name = telegram_user.full_name

    # -----------------------------------------------------
    # ADMIN NOTIFICATION
    # -----------------------------------------------------

    admin_message = (
        "📥 NEW QIRĀʾĀT REGISTRATION\n\n"

        f"👤 Full Name: {data['name']}\n"
        f"📖 Level: {data['level']}\n"
        f"🏠 Dorm: {data['dorm']}\n"
        f"🎓 Year & Department: {data['year_department']}\n"
        f"📱 Telegram Username: {data['username']}\n\n"

        "──────────────\n"

        "👤 Telegram Information\n"
        f"Name: {telegram_name}\n"
        f"User ID: {telegram_id}"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 Reply to Sister",
                callback_data=f"reply_to_{telegram_id}"
            )
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message,
        reply_markup=keyboard
    )

    # -----------------------------------------------------
    # USER CONFIRMATION
    # -----------------------------------------------------

    await update.message.reply_text(
        "🌷 Jazakillahu khayran for registering!\n\n"
        "Your registration information:\n\n"
        f"👤 Name: {data['name']}\n"
        f"📖 Level: {data['level']}\n"
        f"🏠 Dorm: {data['dorm']}\n"
        f"🎓 Year & Department: {data['year_department']}\n"
        f"📱 Telegram: {data['username']}\n\n"
        "✅ Your registration has been received.\n\n"
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

    telegram_user = update.effective_user

    telegram_id = telegram_user.id
    telegram_name = telegram_user.full_name

    if telegram_user.username:
        telegram_username = f"@{telegram_user.username}"
    else:
        telegram_username = "Not provided"

    # -----------------------------------------------------
    # ADMIN NOTIFICATION
    # -----------------------------------------------------

    admin_message = (
        "❓ NEW INQUIRY\n\n"

        f"💬 Question:\n{question}\n\n"

        "──────────────\n"

        "👤 User Information\n"
        f"Name: {telegram_name}\n"
        f"Username: {telegram_username}\n"
        f"User ID: {telegram_id}"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 Reply to Sister",
                callback_data=f"reply_to_{telegram_id}"
            )
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message,
        reply_markup=keyboard
    )

    # -----------------------------------------------------
    # USER CONFIRMATION
    # -----------------------------------------------------

    await update.message.reply_text(
        "🌷 Jazakillahu khayran for your question!\n\n"
        "Your inquiry has been received. 🤍\n\n"
        "We will get back to you regarding your question, "
        "in shā Allah.",
        reply_markup=main_menu(),
    )

    context.user_data.clear()

    return ConversationHandler.END


# =========================================================
# ADMIN REPLY — START
# =========================================================

async def start_admin_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    # -----------------------------------------------------
    # SECURITY CHECK
    # -----------------------------------------------------

    if query.from_user.id != ADMIN_CHAT_ID:

        await query.answer(
            "You are not authorized to use this.",
            show_alert=True
        )

        return ConversationHandler.END

    # -----------------------------------------------------
    # GET TARGET USER ID
    # -----------------------------------------------------

    try:
        target_user_id = int(
            query.data.replace("reply_to_", "")
        )
    except ValueError:

        await query.edit_message_text(
            "❌ Unable to identify the user."
        )

        return ConversationHandler.END

    # Save target user
    context.user_data["reply_to_user"] = target_user_id

    await query.message.reply_text(
        "💬 Reply to Sister\n\n"
        "Please type the message you want to send.\n\n"
        "Type /cancel to cancel."
    )

    return ADMIN_REPLY


# =========================================================
# SEND ADMIN REPLY TO SISTER
# =========================================================

async def send_admin_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # -----------------------------------------------------
    # SECURITY CHECK
    # -----------------------------------------------------

    if update.effective_user.id != ADMIN_CHAT_ID:

        return ConversationHandler.END

    target_user_id = context.user_data.get(
        "reply_to_user"
    )

    if not target_user_id:

        await update.message.reply_text(
            "❌ I couldn't find the sister you're replying to."
        )

        return ConversationHandler.END

    message = update.message.text

    # -----------------------------------------------------
    # SEND MESSAGE TO SISTER
    # -----------------------------------------------------

    try:

        await context.bot.send_message(
            chat_id=target_user_id,
            text=(
                "🌸 Message from Muslim Sisters 4Kilo Jemma\n\n"
                f"{message}"
            )
        )

    except TelegramError:

        await update.message.reply_text(
            "❌ I couldn't send the message.\n\n"
            "The sister may have blocked the bot or "
            "the conversation is no longer available."
        )

        context.user_data.clear()

        return ConversationHandler.END

    # -----------------------------------------------------
    # CONFIRM TO ADMIN
    # -----------------------------------------------------

    await update.message.reply_text(
        "✅ Your message has been sent to the sister."
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

    # -----------------------------------------------------
    # ABOUT JEMMA
    # -----------------------------------------------------

    if query.data == "about_jemma":

        await show_about_jemma(update, context)

    # -----------------------------------------------------
    # ABOUT QIRĀʾĀT
    # -----------------------------------------------------

    elif query.data == "about_qirat":

        await show_about_qirat(update, context)

    # -----------------------------------------------------
    # BACK TO MAIN MENU
    # -----------------------------------------------------

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
    # QIRĀʾĀT REGISTRATION
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
    # INQUIRY
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
    # ADMIN REPLY
    # -----------------------------------------------------

    admin_reply_handler = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                start_admin_reply,
                pattern=r"^reply_to_\d+$"
            )
        ],

        states={

            ADMIN_REPLY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    send_admin_reply
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    # -----------------------------------------------------
    # START
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
    # ADMIN REPLY
    # -----------------------------------------------------

    app.add_handler(
        admin_reply_handler
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

