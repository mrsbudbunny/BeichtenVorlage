from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

# 🔐 Holt den Token und die Admin-Gruppen-ID aus Railway (Umgebungsvariablen)
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_GROUP_CHAT_ID = int(os.environ["ADMIN_GROUP_CHAT_ID"])

# 👋 Begrüßungstext bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*👋 Willkommen beim Beichtbot!*\n\n"
        "Hier kannst du deine tiefsten Gedanken, Geheimnisse, Sünden oder peinlichen Momente **völlig anonym** loswerden.  \n"
        "✍️ Schreib einfach direkt deine Beichte in den Chat.\n\n"
        "🔒 Keine Namen. Keine Spuren. Nur dein Geständnis.\n\n"
         parse_mode='Markdown'
        )

# ✍️ Beichte verarbeiten und weiterleiten
async def handle_beichte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        user_text = update.message.text

        # 📨 Beichte in deine Admin-Gruppe weiterleiten
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_CHAT_ID,
            text=f"🧾 *Neue Beichte:*\n\n{user_text}",
            parse_mode='Markdown'
        )

        # ✅ Bestätigung an den Absender
        await update.message.reply_text(
            "🕯️ Danke für deine Beichte.  \n"
            "Sie wurde erfolgreich anonym übermittelt.\n\n"
            "Unsere Sündenengel prüfen sie – vielleicht erscheint sie bald im Kanal.  \n"
            "Bleib neugierig... 😈",
            parse_mode='Markdown'
        )

# 🧠 Bot starten und Funktionen verbinden
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 📌 /start-Befehl → Begrüßung
app.add_handler(CommandHandler("start", start))

# 📌 Alle normalen Textnachrichten → als Beichte behandeln
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_beichte))

# 🚀 Bot starten
app.run_polling()
