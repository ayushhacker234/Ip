from pyrogram import Client, filters
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied

# अपनी API ID, Hash और Bot Token यहाँ डालें
API_ID = 32935354# अपनी API ID बदलें
API_HASH = "375de2b26c22a6dd164faace06590a92"
BOT_TOKEN = "8808386462:AAFvgMfK7nXuRDWkywZqE0f7W3SS5IB0zH4"  # BotFather से मिला हुआ टोकन

# बोट क्लाइंट को इनिशियलाइज़ करें
app = Client("username_finder_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "नमस्ते! मुझे किसी भी यूज़र का @username भेजें, मैं उसकी Telegram ID ढूंढ दूंगा।\n"
        "नोट: प्राइवेसी के कारण किसी का मोबाइल नंबर निकालना संभव नहीं है।"
    )

@app.on_message(filters.text & filters.private)
async def get_user_details(client, message):
    text = message.text.strip()
    
    # अगर यूज़र ने @ के साथ यूज़रनेम भेजा है तो @ हटा दें
    if text.startswith("@"):
        username = text[1:]
    else:
        username = text

    await message.reply_text("🔍 जानकारी खोजी जा रही है...")

    try:
        # यूज़रनेम से जानकारी निकालें
        user = await client.get_users(username)
        
        # मैसेज तैयार करें (नंबर सिर्फ तभी दिखेगा अगर वो आपका कॉन्टैक्ट हो या उसका नंबर पब्लिक हो)
        phone = user.phone_number if user.phone_number else "प्राइवेसी के कारण छुपा हुआ है"
        
        response = (
            f"✅ **यूज़र मिल गया!**\n\n"
            f"🆔 **Telegram ID:** `{user.id}`\n"
            f"👤 **नाम:** {user.first_name} {user.last_name or ''}\n"
            f"📞 **मोबाइल नंबर:** {phone}\n"
            f"🔗 **यूज़रनेम:** @{user.username}"
        )
        await message.reply_text(response)

    except UsernameInvalid:
        await message.reply_text("❌ यह यूज़रनेम अमान्य (Invalid) है।")
    except UsernameNotOccupied:
        await message.reply_text("❌ इस यूज़रनेम से कोई भी टेलीग्राम अकाउंट नहीं मिला।")
    except Exception as e:
        await message.reply_text(f"❌ कोई एरर आया: {e}")

# बोट चालू करें
app.run()
