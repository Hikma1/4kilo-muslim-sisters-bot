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

async def start_registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
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


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    # -------------------------
    # INQUIRY MENU
    # -------------------------

    if query.data == "inquiry":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎓 Academic",
                    callback_data="inquiry_academic"
                )
            ],
            [
                InlineKeyboardButton(
                    "🌸 Jemma",
                    callback_data="inquiry_jemma"
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 Kitab",
                    callback_data="inquiry_kitab"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="back_menu"
                )
            ],
        ]

        await query.edit_message_text(
            "❓ What is your inquiry about?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # -------------------------
    # ACADEMIC
    # -------------------------

    elif query.data == "inquiry_academic":

        await query.edit_message_text(
            "🎓 Academic Support\n\n"
            "Jemma supports sisters throughout their academic "
            "journey through:\n\n"
            "📚 Freshers' common-course modules\n"
            "🤝 Mentorship with senior sisters\n"
            "👩‍🏫 Tutoring opportunities\n"
            "📝 Past exams and study materials\n\n"
            "Our goal is to help sisters learn, support one "
            "another, and grow together academically. 🌷",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back to Inquiries",
                        callback_data="inquiry"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_menu"
                    )
                ],
            ])
        )

    # -------------------------
    # JEMMA INQUIRY
    # -------------------------

    elif query.data == "inquiry_jemma":

        await query.edit_message_text(
            "🌸 Jemma Inquiry\n\n"
            "For questions about Jemma, its activities, "
            "or programs, please contact the responsible "
            "sister.\n\n"
            "May Allah bless your efforts. 🤍",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back to Inquiries",
                        callback_data="inquiry"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_menu"
                    )
                ],
            ])
        )

    # -------------------------
    # KITAB
    # -------------------------

    elif query.data == "inquiry_kitab":

        await query.edit_message_text(
            "📖 Kitab\n\n"
            "Our Kitab program is coming soon, in shā Allah. 🌷\n\n"
            "Stay connected with Jemma for updates.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back to Inquiries",
                        callback_data="inquiry"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_menu"
                    )
                ],
            ])
        )

    # -------------------------
    # ABOUT JEMMA
    # -------------------------

    elif query.data == "about_jemma":

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

    # -------------------------
    # ABOUT QIRĀʾĀT
    # -------------------------

    elif query.data == "about_qirat":

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

    # -------------------------
    # BACK TO MAIN MENU
    # -------------------------

    elif query.data == "back_menu":

        await query.edit_message_text(
            "🌷 Welcome to Muslim Sisters 4Kilo Bot 🌸\n\n"
            "How can we help you?",
            reply_markup=main_menu(),
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

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        registration_handler
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()