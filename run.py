import logging
import csv
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from elasticsearch import Elasticsearch
from telegram.ext import MessageHandler, filters

from telegram import Update, InputFile
from telegram.ext import CallbackContext

# ✅ Configure Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# ✅ Replace with your actual bot token
BOT_TOKEN = "7619265335:AAEBEY3e2ZMN_WYovTxNIkYgldYCinGBPZM"

INDEX_NAME = "telegram_bot_users"

def get_allowed_users():
    try:
        result = es.get(index=INDEX_NAME, id=ALLOWED_USER)
        allowed_users = set(result["_source"]["users"])
        logging.info(f"Allowed users retrieved: {allowed_users}")
        return allowed_users
    except Exception as e:
        logging.error(f"Error retrieving allowed users: {e}")
        return {ALLOWED_USER}

def save_allowed_users():
    try:
        es.index(index=INDEX_NAME, id=ALLOWED_USER, body={"users": list(ALLOWED_USERS)})
        logging.info(f"Allowed users saved: {ALLOWED_USERS}")
    except Exception as e:
        logging.error(f"Error saving allowed users: {e}")

ALLOWED_USER = "Hamkurr"  # Only this user can use the bot
ALLOWED_USERS = get_allowed_users()
PRIVATE_GROUP_ID = -1002327087494

async def is_authorized(update: Update, context: CallbackContext) -> bool:
    if update.message.from_user.username not in ALLOWED_USERS:
        logging.info("User is not authorized")
        await context.bot.send_message(chat_id=update.message.chat_id, text="🚫 Sorry, you are not authorized to use this bot.", parse_mode="Markdown")
        return False
    logging.info("User is authorized")
    return True





import shodan
import socket

# ✅ Shodan API Key (Replace with your key)
SHODAN_API_KEY = "2uLPozHkyVG0xob9YaIx9sqq7i4XTvOO"

# ✅ Function to resolve a domain to an IP address
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None



# ✅ Function to fetch Shodan data for an IP address
def get_shodan_data(ip_address):
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        host_details = api.host(ip_address)
        response = f"🔎 *Shodan Report for {ip_address}*\n\n"
        response += f"📡 *IP:* `{ip_address}`\n"

        if "os" in host_details:
            response += f"💻 *OS:* `{host_details['os']}`\n"
        if "org" in host_details:
            response += f"🏢 *Org:* `{host_details['org']}`\n"
        if "ports" in host_details:
            response += f"🚪 *Ports:* `{', '.join(map(str, host_details['ports']))}`\n"

        # Display vulnerabilities
        if "vulns" in host_details:
            response += "\n⚠️ *Vulnerabilities:*\n"
            for vuln in host_details["vulns"]:
                response += f"  - `{vuln}`\n"

        # Display technologies
        if "data" in host_details:
            response += "\n🛠 *Technologies:*\n"
            for item in host_details["data"]:
                if "product" in item:
                    tech_info = f"  - `{item['product']}`"
                    if "version" in item:
                        tech_info += f" (v{item['version']})"
                    response += f"{tech_info}\n"

        return response

    except shodan.APIError as e:
        return f"❌ *Error:* `{e}`"

# ✅ Command Handler for /shodan
async def shodan_command(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/shodan <domain>`", parse_mode="Markdown")
        return

    domain = context.args[0]
    await update.message.reply_text(f"🔍 Resolving `{domain}`...", parse_mode="Markdown")

    ip_address = resolve_domain(domain)
    if not ip_address:
        await update.message.reply_text(f"❌ Could not resolve `{domain}`.", parse_mode="Markdown")
        return

    await update.message.reply_text(f"📡 `{domain}` → `{ip_address}`\n🔎 Fetching Shodan data...", parse_mode="Markdown")

    shodan_data = get_shodan_data(ip_address)
    await update.message.reply_text(shodan_data, parse_mode="Markdown")





# ✅ Function to Check User Authorization
async def is_authorized(update: Update) -> bool:
    return update.message.from_user.username in ALLOWED_USERS

async def add_user(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if update.message.from_user.username != ALLOWED_USER:
        await update.message.reply_text("🚫 Sorry, you can't add new users! Only the chosen one (Hamkurr) can do that. 😎", parse_mode="Markdown")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/adduser <username>`", parse_mode="Markdown")
        return

    new_user = context.args[0]
    ALLOWED_USERS.add(new_user)
    save_allowed_users()
    await update.message.reply_text(f"✅ User `{new_user}` has been added to the club! 🎉", parse_mode="Markdown")
    logging.info(f"New user added: {new_user}")

async def remove_user(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if update.message.from_user.username != ALLOWED_USER:
        await update.message.reply_text("🚫 Sorry, you can't remove users! Only the chosen one (Hamkurr) can do that. 😎", parse_mode="Markdown")
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/rmuser <username>`", parse_mode="Markdown")
        return

    user_to_remove = context.args[0]
    if user_to_remove in ALLOWED_USERS:
        ALLOWED_USERS.remove(user_to_remove)
        save_allowed_users()
        await update.message.reply_text(f"✅ User `{user_to_remove}` has been removed from the club. 😢", parse_mode="Markdown")
        logging.info(f"User removed: {user_to_remove}")
    else:
        await update.message.reply_text(f"❌ User `{user_to_remove}` not found in the club. 🤔", parse_mode="Markdown")

async def reset_users(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if update.message.from_user.username != ALLOWED_USER:
        await update.message.reply_text("🚫 Sorry, you can't reset the users! Only the chosen one (Hamkurr) can do that. 😎", parse_mode="Markdown")
        return

    ALLOWED_USERS.clear()
    ALLOWED_USERS.add(ALLOWED_USER)
    save_allowed_users()
    await update.message.reply_text("✅ All users have been reset. Only the chosen one remains. 🌟", parse_mode="Markdown")
    logging.info("All users reset")
    
async def list_all_users(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    users_list = "\n".join(ALLOWED_USERS)
    await update.message.reply_text(f"👥 Here are the users in the club:\n\n{users_list}", parse_mode="Markdown")

# ✅ Function to search Elasticsearch
def search_leaked_data(search_term, page=0, page_size=5, fields=None):
    if fields is None:
        fields = ["domain", "user", "password"]

    query = {
        "query": {
            "multi_match": {
                "query": search_term,
                "fields": fields
            }
        },
        "size": page_size,
        "from": page * page_size
    }

    results = es.search(index="leaked_data", body=query)
    hits = results["hits"]["hits"]

    if not hits:
        return None, 0

    response = f"🔍 *Leaked Data for:* `{search_term}`\n"
    for i, hit in enumerate(hits, start=1):
        response += f"\n📌 *Result {page * page_size + i}:*\n"
        response += f"🌐 *{hit['_source']['domain']} ({hit['_source']['path']})*\n"
        response += f"👤 *User:* `{hit['_source']['user']}`\n🔑 *Password:* `{hit['_source']['password']}`\n"

    total_hits = results["hits"]["total"]["value"]
    return response, total_hits

# ✅ Function to generate pagination buttons
def generate_buttons(search_term, page, page_size, total_hits, fields):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"prev_{search_term}_{page - 1}_{page_size}_{'_'.join(fields)}"))
    if (page + 1) * page_size < total_hits:
        buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"next_{search_term}_{page + 1}_{page_size}_{'_'.join(fields)}"))

    return InlineKeyboardMarkup([buttons]) if buttons else None

# ✅ Command Handler for /getuser
async def getuser(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/getuser <username or domain> [fields] [page_size]`", parse_mode="Markdown")
        return

    search_term = context.args[0]
    fields = context.args[1].split(",") if len(context.args) > 1 else ["domain", "user", "password"]
    page_size = int(context.args[2]) if len(context.args) > 2 else 5

    await update.message.reply_text(f"🔍 Searching for: *{search_term}*... 🤓", parse_mode="Markdown")

    result, total_hits = search_leaked_data(search_term, page=0, page_size=page_size, fields=fields)

    if result:
        reply_markup = generate_buttons(search_term, page=0, page_size=page_size, total_hits=total_hits, fields=fields)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)
        
        # Generate and send the HTML and CSV files
        html_file = generate_html(search_term, fields)
        csv_file = generate_csv(search_term, fields)
        if html_file:
            with open(html_file, "rb") as file:
                await update.message.reply_document(InputFile(file), filename=f"{search_term}_leaked_data.html")
        if csv_file:
            with open(csv_file, "rb") as file:
                await update.message.reply_document(InputFile(file), filename=f"{search_term}_leaked_data.csv")

    else:
        await update.message.reply_text(f"✅ No leaked data found for `{search_term}`. 🕵️‍♂️", parse_mode="Markdown")

# ✅ Callback function for pagination (Next/Previous buttons)
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action, search_term, page, page_size, *fields = data
    page = int(page)
    page_size = int(page_size)

    result, total_hits = search_leaked_data(search_term, page=page, page_size=page_size, fields=fields)

    if result:
        reply_markup = generate_buttons(search_term, page, page_size=page_size, total_hits=total_hits, fields=fields)
        await query.edit_message_text(result, parse_mode="Markdown", reply_markup=reply_markup)

# ✅ Function to generate HTML file with all data
def generate_html(search_term, fields):
    result, total_hits = search_leaked_data(search_term, page=0, page_size=1000, fields=fields)
    if result:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Leaked Data for {search_term}</title>
        </head>
        <body>
            <h1>Leaked Data for {search_term}</h1>
            <pre>{result}</pre>
        </body>
        </html>
        """
        file_name = f"{search_term}_leaked_data.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)
        return file_name
    return None

# ✅ Function to generate CSV file with all data
def generate_csv(search_term, fields):
    result, total_hits = search_leaked_data(search_term, page=0, page_size=1000, fields=fields)
    if result:  # Fixed indentation here
        file_name = f"{search_term}_leaked_data.csv"
        with open(file_name, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Domain", "Path", "User", "Password"])

            for line in result.split("\n\n")[1:]:
                details = line.split("\n")
                domain = details[1].split(" ")[1]
                path = details[1].split("(")[1][:-1]
                user = details[2].split("`")[1]
                password = details[3].split("`")[1]
                writer.writerow([domain, path, user, password])

        return file_name
    return None
    
    
def chat_with_ai(user_query):
    url = "https://www.ninjachat.ai/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        # Check if response is empty
        if not response.text.strip():
            return "Error: Received an empty response from AI API."

        # Format response for Telegram users
        formatted_response = ""
        lines = response.text.split("\n")
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    formatted_response += f"{line.strip()}\n"
                    in_code_block = False
                else:
                    formatted_response += f"{line.strip()}\n"
                    in_code_block = True
            elif in_code_block or line.strip().startswith("<") or line.strip().startswith("&lt;") or line.strip().startswith("&gt;") or line.strip().startswith("**"):
                formatted_response += f"`{line.strip()}`\n"
            else:
                formatted_response += f"{line.strip()}\n"

        return formatted_response

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"


# ✅ Async Handler for AI Bot Messages
async def ai_chat(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/chat <text>`", parse_mode="Markdown")
        return

    user_query = " ".join(context.args)

    if user_query:
        # Run chat_with_ai in a separate thread to prevent blocking
        from asyncio import to_thread
        response = await to_thread(chat_with_ai, user_query)

        if response:
            try:
                await update.message.reply_text(response, parse_mode="Markdown")
            except Exception as e:
                await update.message.reply_text("Error: Unable to send AI response.")
        else:
            await update.message.reply_text("Error: No response from AI.")
    else:
        await update.message.reply_text("❌ Please provide a message after the `/chat` command.")
          

def fetch_subdomains(domain):
    url = f"https://shrewdeye.app/domains/{domain}.txt"
    response = requests.get(url)

    if response.status_code == 200:
        file_name = f"{domain}_subdomains.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(response.text)
        return file_name
    else:
        return None

# ✅ Command Handler for /subdomains
async def subdomains(update: Update, context: CallbackContext) -> None:
    if not await is_authorized(update):
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ *Usage:* `/subdomains <domain>`", parse_mode="Markdown")
        return

    domain = context.args[0]
    file_name = fetch_subdomains(domain)

    if file_name:
        with open(file_name, "rb") as file:
            await update.message.reply_document(
                document=InputFile(file, filename=f"{domain}_subdomains.txt")
            )
        await update.message.reply_text(f"✅ Subdomains for `{domain}` have been sent! 📄", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ No subdomains found for `{domain}`. 😕", parse_mode="Markdown")


# ✅ Start Command
async def start(update: Update, context: CallbackContext) -> None:
    introduction = (
        "👋 Welcome to our Telegram bot! Here are the commands you can use:\n\n"
        "**/getuser <username>** [fields] [page_size] - Search leaked data for a specific user.\n\n"
        "**/subdomains <domain>** - Fetch subdomains for a specific domain.\n\n"
        "**/chat <text>** - Chat with the AI.\n\n"
        "**/shodan <query>** - Search Shodan for a specific query.\n\n"
        "Feel free to use any of these commands to interact with the bot!\n\n"
        "To use this bot, contact @hamkurr."
    )
    await update.message.reply_text(introduction, parse_mode="Markdown")



  
            
# ✅ Set up the Telegram bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getuser", getuser))
    app.add_handler(CommandHandler("adduser", add_user))  # Add command handler for /adduser
    app.add_handler(CommandHandler("rmuser", remove_user))  # Add command handler for /rmuser
    app.add_handler(CommandHandler("reset", reset_users))  # Add command handler for /reset
    app.add_handler(CommandHandler("subdomains", subdomains))  # Add command handler for /subdomains
    app.add_handler(CallbackQueryHandler(button_handler))
    #app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    app.add_handler(CommandHandler("allusers", list_all_users))
    app.add_handler(CommandHandler("chat", ai_chat))
    app.add_handler(CommandHandler("shodan", shodan_command))


    print("🚀 Telegram bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
