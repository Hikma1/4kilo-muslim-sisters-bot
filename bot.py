import os

from dotenv import load_dotenv
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


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))


# ============================================================
# CONVERSATION STATES
# ============================================================

NAME, LEVEL, DORM, YEAR_DEPARTMENT, USERNAME = range(5)
INQUIRY = 5
ADMIN_REPLY = 6


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📖 Qirat Registration", callback_data="register"),
        ],
        [
            InlineKeyboardButton("❓ Any Question / Inquiry", callback_data="inquiry"),
        ],
        [
            InlineKeyboardButton("🌸 About Jemma", callback_data="about_jemma"),
        ],
        [
            InlineKeyboardButton("📖 About Qirat", callback_data="about_qiraat"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Clear old conversation data
    context.user_data.clear()

    welcome_message = (
        "🌸 *Welcome to Muslim Sisters 4Kilo Jemma Bot!*\n\n"
        "Asalamualaikum warahmatullahi wabarakatullah 🌷\n\n"
        "This bot is here to help sisters connect with Jemma, "
        "register for Qirat, ask questions, and learn more about our activities.\n\n"
        "Please choose an option below:"
    )

    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


# ============================================================
# QIRĀʾĀT REGISTRATION
# ============================================================

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    await query.message.reply_text(
        "📖 *Qirat Registration*\n\n"
        "Let's start your registration.\n\n"
        "👤 Please enter your *full name*:",
        parse_mode="Markdown",
    )

    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "📖 What is your Qirat level?\n\n"
        "Please choose one:\n\n"
        "• Qaida\n"
        "• Nazr\n"
        "• Hifz"
    )

    return LEVEL


async def get_level(update: Update, context: ContextTypes.DEFAULT_TYPE):

    level = update.message.text.strip()

    context.user_data["level"] = level

    await update.message.reply_text(
        "🏠 Please enter your *dorm number*:",
        parse_mode="Markdown",
    )

    return DORM


async def get_dorm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["dorm"] = update.message.text

    await update.message.reply_text(
        "🎓 Please enter your *year and department*.\n\n"
        "Example:\n"
        "2nd Year - Software Engineering",
        parse_mode="Markdown",
    )

    return YEAR_DEPARTMENT


async def get_year_department(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["year_department"] = update.message.text

    await update.message.reply_text(
        "📱 Please enter your *Telegram username*.\n\n"
        "Example: @username",
        parse_mode="Markdown",
    )

    return USERNAME


async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["username"] = update.message.text

    user = update.effective_user

    # Get information
    name = context.user_data["name"]
    level = context.user_data["level"]
    dorm = context.user_data["dorm"]
    year_department = context.user_data["year_department"]
    username = context.user_data["username"]

    # ========================================================
    # SEND REGISTRATION TO ADMIN
    # ========================================================

    admin_message = (
        "📥 *NEW QIRĀʾĀT REGISTRATION*\n\n"
        f"👤 *Full Name:* {name}\n"
        f"📖 *Level:* {level}\n"
        f"🏠 *Dorm:* {dorm}\n"
        f"🎓 *Year & Department:* {year_department}\n"
        f"📱 *Telegram Username:* {username}\n\n"
        "──────────────\n"
        "👤 *Telegram Information*\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'No username'}\n"
        f"User ID: `{user.id}`"
    )

    reply_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💬 Reply to Sister",
                    callback_data=f"reply_to_{user.id}",
                )
            ]
        ]
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode="Markdown",
            reply_markup=reply_button,
        )

    except TelegramError as error:
        print(f"Error sending registration to admin: {error}")

    # ========================================================
    # SEND CONFIRMATION TO USER
    # ========================================================

    confirmation_message = (
        "🌸 *Registration Submitted Successfully!*\n\n"
        "Jazakillahu Khayran for registering for Qirāʾāt. 🤍\n\n"
        "Your information has been sent to the Jemma team.\n\n"
        "May Allah make the Qur’an the light of our hearts "
        "and guide us through it. آمين 🤲"
    )

    await update.message.reply_text(
        confirmation_message,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

    context.user_data.clear()

    return ConversationHandler.END


# ============================================================
# INQUIRY
# ============================================================

async def start_inquiry(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "❓ *Any Question / Inquiry*\n\n"
        "You can ask us anything related to:\n\n"
        "🌸 Jemma\n"
        "📚 Academics\n"
        "📖 Qirāʾāt\n"
        "🏫 Campus life\n"
        "🤝 Activities\n"
        "📢 Programs\n"
        "💬 Or anything else related to our sisters' community.\n\n"
        "Please type your question below:"
        ,
        parse_mode="Markdown",
    )

    return INQUIRY


async def receive_inquiry(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    question = update.message.text

    username = f"@{user.username}" if user.username else "No username"

    admin_message = (
        "❓ *NEW INQUIRY*\n\n"
        "💬 *Question:*\n"
        f"{question}\n\n"
        "──────────────\n"
        "👤 *User Information*\n"
        f"Name: {user.full_name}\n"
        f"Username: {username}\n"
        f"User ID: `{user.id}`"
    )

    reply_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💬 Reply to Sister",
                    callback_data=f"reply_to_{user.id}",
                )
            ]
        ]
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode="Markdown",
            reply_markup=reply_button,
        )

    except TelegramError as error:
        print(f"Error sending inquiry to admin: {error}")

    await update.message.reply_text(
        "🌸 *Your question has been sent!*\n\n"
        "Jazakillahu Khayran. A sister from the Jemma team "
        "will respond to you through this bot, in shā Allah. 🤍",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

    return ConversationHandler.END


# ============================================================
# ADMIN REPLY
# ============================================================

async def start_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # Only admin can use this button
    if query.from_user.id != ADMIN_CHAT_ID:
        await query.message.reply_text(
            "⛔ You are not authorized to use this function."
        )
        return ConversationHandler.END

    # Extract target user ID
    try:
        target_user_id = int(query.data.replace("reply_to_", ""))

    except ValueError:
        await query.message.reply_text(
            "❌ Could not identify the user."
        )
        return ConversationHandler.END

    context.user_data["reply_to_user"] = target_user_id

    await query.message.reply_text(
        "💬 Please type the message you want to send to the sister:"
    )

    return ADMIN_REPLY


async def send_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Security check
    if update.effective_user.id != ADMIN_CHAT_ID:
        return ConversationHandler.END

    target_user_id = context.user_data.get("reply_to_user")

    if not target_user_id:
        await update.message.reply_text(
            "❌ No recipient was found."
        )
        return ConversationHandler.END

    admin_message = update.message.text

    message_to_user = (
        "🌸 *Message from Muslim Sisters 4Kilo Jemma*\n\n"
        f"{admin_message}"
    )

    try:

        await context.bot.send_message(
            chat_id=target_user_id,
            text=message_to_user,
            parse_mode="Markdown",
        )

        await update.message.reply_text(
            "✅ Message sent successfully."
        )

    except TelegramError as error:

        print(f"Error sending admin reply: {error}")

        await update.message.reply_text(
            "❌ The message could not be sent.\n\n"
            "The user may have blocked the bot or the conversation "
            "may no longer be available."
        )

    context.user_data.pop("reply_to_user", None)

    return ConversationHandler.END


# ============================================================
# ABOUT JEMMA
# ============================================================

async def about_jemma(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    message = (
        "بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ\n\n"
        "🌸 *About 4Kilo Muslim Students Jemma*\n\n"
        
        "🤍 *Deen & Unity*\n"
        "Helping Muslim students at Addis Ababa University, "
        "4Kilo Campus, remain firm in their faith, strengthen "
        "their unity, and support one another.\n\n"

        "🌷 *Sisterhood*\n"
        "Creating a community where sisters learn, support, "
        "and grow together.\n\n"

        "🤝 *Support & Rights*\n"
        "Working together to address challenges and rights-related "
        "concerns faced by Muslim students because of their faith.\n\n"

        "📖 *Islamic Learning*\n"
        "Coordinating beneficial Islamic learning opportunities "
        "through nearby masjids and programs.\n\n"

        "📚 *Academic Growth*\n"
        "Supporting sisters through mentorship, tutoring, study "
        "materials, and other academic opportunities.\n\n"

        "✨ *Together in Deen. Together in Sisterhood. "
        "Together in Growth.*"
    )

    back_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Back to Menu",
                    callback_data="back_menu",
                )
            ]
        ]
    )

    await query.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=back_button,
    )


# ============================================================
# ABOUT QIRĀʾĀT
# ============================================================

async def about_qiraat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    message = (
        "📖 *About Qirāʾāt*\n\n"

        "The Qirāʾāt program provides sisters with an opportunity "
        "to learn and improve their Qur’an recitation in a supportive "
        "environment. 🤍\n\n"

        "📚 *Available Levels:*\n\n"
        "• Qaida\n"
        "• Nazr\n"
        "• Hifz\n\n"

        "🌸 *Learn • Recite • Improve*\n\n"

        "May Allah make the Qur’an the light of our hearts, "
        "the source of our guidance, and a means of drawing "
        "closer to Him. آمين 🤲"
    )

    back_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Back to Menu",
                    callback_data="back_menu",
                )
            ]
        ]
    )

    await query.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=back_button,
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "about_jemma":
        await about_jemma(update, context)

    elif query.data == "about_qiraat":
        await about_qiraat(update, context)

    elif query.data == "back_menu":

        await query.message.reply_text(
            "🌸 *Main Menu*\n\n"
            "Please choose an option:",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )


# ============================================================
# CANCEL
# ============================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ The process has been cancelled.\n\n"
        "You can start again anytime.",
        reply_markup=main_menu(),
    )

    return ConversationHandler.END


# ============================================================
# MAIN
# ============================================================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Please check your .env file."
        )

    if not ADMIN_CHAT_ID:
        raise ValueError(
            "ADMIN_CHAT_ID is missing. Please check your .env file."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    # --------------------------------------------------------
    # QIRĀʾĀT REGISTRATION CONVERSATION
    # --------------------------------------------------------

    registration_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_registration,
                pattern="^register$",
            )
        ],

        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name,
                )
            ],

            LEVEL: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_level,
                )
            ],

            DORM: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_dorm,
                )
            ],

            YEAR_DEPARTMENT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_year_department,
                )
            ],

            USERNAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_username,
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    # --------------------------------------------------------
    # INQUIRY CONVERSATION
    # --------------------------------------------------------

    inquiry_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_inquiry,
                pattern="^inquiry$",
            )
        ],

        states={
            INQUIRY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_inquiry,
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    # --------------------------------------------------------
    # ADMIN REPLY CONVERSATION
    # --------------------------------------------------------

    admin_reply_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_admin_reply,
                pattern=r"^reply_to_\d+$",
            )
        ],

        states={
            ADMIN_REPLY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    send_admin_reply,
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    # --------------------------------------------------------
    # ADD HANDLERS
    # --------------------------------------------------------

    app.add_handler(CommandHandler("start", start))

    app.add_handler(registration_handler)

    app.add_handler(inquiry_handler)

    app.add_handler(admin_reply_handler)

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # --------------------------------------------------------
    # START BOT
    # --------------------------------------------------------

    print("🌸 Muslim Sisters 4Kilo Jemma Bot is running...")

    app.run_polling()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()