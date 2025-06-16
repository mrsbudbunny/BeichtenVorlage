import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_GROUP_CHAT_ID = os.getenv("ADMIN_GROUP_CHAT_ID")
SECOND_ADMIN_GROUP_ID = "4906100471"  # ID deiner Bearbeitungsgruppe

# Statistik-Datei
STATS_FILE = "stats.json"

# Blacklist
BLACKLIST = [
    "mord", "vergewaltigung", "kind", "waffe", "anschlag", "bombe", "droge", "vergiften",
    "minderjährig", "kinderporno", "mutter", "vater", "schwester", "bruder",
    "cousin", "cousine", "tante", "onkel"
]

# Statistik laden
def load_stats():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f).get("count", 0)
    except FileNotFoundError:
        return 0

# Statistik speichern
def save_stats(count):
    with open(STATS_FILE, "w") as f:
        json.dump({"count": count}, f)

# Startwert
beicht_count = load_stats()

# /start-Befehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Willkommen bei den *Sündigen 18+ Beichten!*\n\n"
        "Hier kannst du deine tiefsten Gedanken, Geheimnisse, Sünden oder peinlichen Momente **völlig anonym** loswerden.\n"
        "✍️ Schreib einfach direkt deine Beichte in den Chat.\n\n"
        "🔒 Keine Namen. Keine Spuren. Nur dein Geständnis.\n\n"
        "‼️Bitte beachte, dass illegale Beichten nicht mit veröffentlicht werden.",
        parse_mode='Markdown'
    )

# Beichte empfangen
async def handle_beichte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global beicht_count
    user_text = update.message.text
    lower_text = user_text.lower()

    # Blacklist prüfen
    hits = [w for w in BLACKLIST if w in lower_text]
    warnung = "⚠️ *Achtung: Verdächtige Begriffe erkannt!*\n\n" if hits else ""

    # Buttons vorbereiten
    buttons = [
        [InlineKeyboardButton("✅ Zur Bearbeitung", callback_data=f"approve|{user_text}")],
        [InlineKeyboardButton("❌ Ablehnen", callback_data=f"reject|{user_text}")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # Nachricht an Admin-Gruppe mit Buttons
    await context.bot.send_message(
        chat_id=ADMIN_GROUP_CHAT_ID,
        text=f"{warnung}📩 *Neue Beichte:*\n\n{user_text}",
        parse_mode='Markdown',
        reply_markup=keyboard
    )

    # Statistik erhöhen
    beicht_count += 1
    save_stats(beicht_count)

    # Antwort an den Absender
    await update.message.reply_text(
        "🕯️ Danke für deine Beichte.\n"
        "Sie wurde erfolgreich anonym übermittelt.\n\n"
        "Unsere Sündenengel prüfen sie – vielleicht erscheint sie bald im Kanal.\n"
        "Bleib neugierig... 😈\n"
        "🔜 https://t.me/+6EbbhC90nKBlZTc6",
        parse_mode='Markdown'
    )

# /stats Befehl
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📈 Es wurden bisher *{beicht_count}* Beichten abgegeben.",
        parse_mode='Markdown'
    )

# Callback-Handler für Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, text = query.data.split("|", 1)

    if action == "approve":
        await context.bot.send_message(
            chat_id=SECOND_ADMIN_GROUP_ID,
            text=f"📝 *Beichte zur Bearbeitung freigegeben:*\n\n{text}",
            parse_mode='Markdown'
        )
        await query.edit_message_text("✅ Diese Beichte wurde zur Bearbeitung weitergeleitet.")
    elif action == "reject":
        await query.edit_message_text("❌ Diese Beichte wurde als ungeeignet markiert.")

# Start
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_beichte))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()
