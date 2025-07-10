from pyrogram import Client, filters
from async_eval import eval as async_eval
import pyrogram
from pyrogram.enums import ChatMemberStatus, ChatType, ParseMode
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)

# Bot credentials and allowed users
bot = "7583570260:AAGbgYgCCBP0FphuEIIDl5f0KpMsEFY8-nA"
users = [7967897421]

# Initialize Client
app = Client("my_account", api_id=3184293, api_hash="437f365b4e18d43b8218adc7a6577345")

# Eval command
@app.on_message(filters.command("eval", prefixes=[".", "!", "$"]) & filters.user(users))
async def eval_command(client, message):
    global c, m, r
    c, m, r = client, message, message.reply_to_message

    text = m.text[6:]
    try:
        vc = str(await async_eval(text))
    except Exception as e:
        vc = str(e)

    try:
        await message.reply(
            f"**Input:** `{m.text}`\n\n**Output (json):**\n`{vc}`",
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        try:
            await message.reply(
                f"**Input:** `{m.text}`\n\n**Error:**\n`{e}`",
                disable_web_page_preview=True,
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass

    # Save result to file
    with open("Result.txt", "w") as g:
        g.write(str(vc))

    # Check bot member status in groups
    if m.chat.type == ChatType.SUPERGROUP:
        x = (await app.get_chat_member(m.chat.id, (await app.get_me()).id)).status
        if x in [ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]:
            return

    # Send result file
    try:
        await message.reply_document("Result.txt")
    except:
        return

# Start the bot
app.run()
