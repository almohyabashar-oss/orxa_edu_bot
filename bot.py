"""
أكاديمية أوركسا - Orxa Education Academy
Telegram Bot - @orxa_edu_bot
"""

import os
import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============ Configuration ============
TOKEN = os.environ.get("BOT_TOKEN", "8376517624:AAG6xYHoPsw57JmSFaFaJwTAMDrYtdadrrY")
OWNER_ID = int(os.environ.get("OWNER_ID", "8329587970"))
ADMIN_USERNAME = "@WRBd9"
ADMIN_URL = "https://t.me/WRBd9"
CHANNEL_URL = "https://t.me/orxa_edu"  # Channel for work samples & reviews

# ============ Logging ============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============ Services Data ============
SERVICES = [
    {
        "callback_data": "homework",
        "text": "📚 واجبات ومشاريع جامعية",
        "price": "50 - 300",
    },
    {
        "callback_data": "research",
        "text": "🔬 بحوث علمية",
        "price": "80 - 500",
    },
    {
        "callback_data": "exams",
        "text": "✏️ حل اختبارات",
        "price": "30 - 150",
    },
    {
        "callback_data": "summaries",
        "text": "📝 ملخصات",
        "price": "20 - 80",
    },
    {
        "callback_data": "reports",
        "text": "📊 إعداد التقارير",
        "price": "60 - 100",
    },
    {
        "callback_data": "cv",
        "text": "📄 السيرة الذاتية",
        "price": "30 - 80",
    },
    {
        "callback_data": "presentations",
        "text": "🎯 العروض التقديمية",
        "price": "50 - 300",
    },
    {
        "callback_data": "design",
        "text": "🎨 التصاميم والجرافيكس",
        "price": "80 - 500",
    },
]

# ============ Helper: Forward to Owner ============
async def forward_to_owner(text: str, user_id: int = 0, user_name: str = ""):
    """Send a copy of the interaction to the owner."""
    try:
        user_info = f"👤 المستخدم: {user_name} (ID: {user_id})" if user_id else ""
        await Application.bot.get_current().send_message(
            chat_id=OWNER_ID,
            text=f"📨 تفاعل جديد:\n{user_info}\n\n{text}",
        )
    except Exception as e:
        logger.error(f"Error forwarding to owner: {e}")


# ============ Helper: Main Menu ============
def get_main_menu_keyboard():
    """Build the main services keyboard."""
    keyboard = []
    for service in SERVICES:
        keyboard.append(
            [InlineKeyboardButton(service["text"], callback_data=service["callback_data"])]
        )
    return InlineKeyboardMarkup(keyboard)


# ============ Handlers ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    first_name = user.first_name or ""

    welcome_text = (
        f"أهلاً وسهلاً {first_name} 🎓\n\n"
        f"🏫 <b>أكاديمية أوركسا | Orxa Education Academy</b>\n\n"
        f"نقدم لكم أفضل الخدمات الأكاديمية بجودة عالية وأسعار مناسبة.\n\n"
        f"📌 <b>اختر الخدمة المطلوبة:</b>"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )

    # Forward to owner
    await forward_to_owner(
        text=f"🆕 مستخدم جديد: {first_name}\nUsername: @{user.username or 'N/A'}\n/ تم الدخول للقائمة الرئيسية",
        user_id=user.id,
        user_name=first_name,
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button clicks."""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = query.data

    # ============ Handle Service Selection ============
    for service in SERVICES:
        if data == service["callback_data"]:
            service_text = (
                f"📌 <b>{service['text']}</b>\n\n"
                f"💰 <b>السعر:</b> من {service['price']} ريال\n"
                f"✅ مع إمكانية التخفيض\n\n"
                f"💳 <b>طريقة الدفع:</b> بالاتفاق مع المشرف\n\n"
                f"للتواصل والطلب، تواصل مع المشرف مباشرة عبر الزر أدناه 👇"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "💬 تواصل مع المشرف",
                        url=ADMIN_URL,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📁 نماذج أعمالنا وآراء الطلاب",
                        url=CHANNEL_URL,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🔙 رجوع للقائمة الرئيسية",
                        callback_data="back_to_menu",
                    ),
                ],
            ]

            await query.edit_message_text(
                text=service_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML",
            )

            await forward_to_owner(
                text=f"اختار خدمة: {service['text']}\nالسعر: {service['price']} ريال",
                user_id=user.id,
                user_name=user.first_name or "",
            )
            return

    # ============ Handle Back to Menu ============
    if data == "back_to_menu":
        first_name = user.first_name or ""
        text = (
            f"🏫 <b>أكاديمية أوركسا | Orxa Education Academy</b>\n\n"
            f"📌 <b>اختر الخدمة المطلوبة:</b>"
        )

        await query.edit_message_text(
            text=text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML",
        )

        await forward_to_owner(
            text="🔙 رجع للقائمة الرئيسية",
            user_id=user.id,
            user_name=user.first_name or "",
        )
        return

    # ============ Unknown Callback ============
    await query.edit_message_text(
        text="⚠️ حدث خطأ. الرجاء البدء من جديد.",
        reply_markup=get_main_menu_keyboard(),
    )


async def echo_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text messages from users."""
    user = update.effective_user
    text = update.message.text

    reply_text = (
        "🤖 أهلاً بك في <b>أكاديمية أوركسا</b>\n\n"
        "للبدء، الرجاء الضغط على زر /start من الأسفل\n\n"
        "للتواصل المباشر مع المشرف:\n"
        f"{ADMIN_URL}"
    )

    await update.message.reply_text(reply_text, parse_mode="HTML")

    # Forward to owner
    await forward_to_owner(
        text=f"رسالة: {text[:200]}",
        user_id=user.id,
        user_name=user.first_name or "",
    )


# ============ Main ============
def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_messages))

    logger.info("🚀 Orxa Education Academy Bot is running...")
    logger.info(f"👤 Owner ID: {OWNER_ID}")
    logger.info(f"📱 Admin: {ADMIN_USERNAME}")

    # Run with polling (suitable for Render free tier)
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        poll_interval=1.0,
    )


if __name__ == "__main__":
    main()
