import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
ADMIN_ID = 6292662642  # Bemni

PRODUCTS_FILE = "products.json"


def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    message = "🍽️ *Kana Foods Menu:*\n\n"
    for name, price in products.items():
        message += f"• {name}: {price} birr\n"
    await update.message.reply_text(message, parse_mode="Markdown")


async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    if not products:
        await update.message.reply_text("No products found.")
        return
    message = "📦 *Product List:*\n\n"
    for name, price in products.items():
        message += f"{name} — {price} birr\n"
    await update.message.reply_text(message, parse_mode="Markdown")


async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized to add products.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addproduct <name> <price>")
        return

    name = " ".join(context.args[:-1])
    try:
        price = float(context.args[-1])
    except ValueError:
        await update.message.reply_text("Price must be a number.")
        return

    products = load_products()
    products[name] = price
    save_products(products)
    await update.message.reply_text(f"✅ Added/updated product: {name} — {price} birr")


async def remove_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized to remove products.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /removeproduct <name>")
        return

    name = " ".join(context.args)
    products = load_products()
    if name not in products:
        await update.message.reply_text("Product not found.")
        return

    del products[name]
    save_products(products)
    await update.message.reply_text(f"🗑️ Removed product: {name}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("listproducts", list_products))
    app.add_handler(CommandHandler("addproduct", add_product))
    app.add_handler(CommandHandler("removeproduct", remove_product))
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
