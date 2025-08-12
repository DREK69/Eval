from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# 🔐 User Account Login (No Bot Token)
API_ID = 25723056
API_HASH = "cbda56fac135e92b755e1243aefe9697"
OWNER_ID = 7967897421  # Only this user can eval

# Initialize User Client (not bot)
app = Client("user_session", api_id=API_ID, api_hash=API_HASH)

# Async eval function
async def aexec(code, c, m, r, u):
    local_vars = {}
    lines = code.strip().split("\n")
    func_code = "async def __aexec(c, m, r, u):\n"
    if len(lines) == 1 and not lines[0].strip().startswith(("return", "import", "for", "if", "while", "def", "async")):
        func_code += f"    return {lines[0]}\n"
    else:
        for line in lines:
            func_code += f"    {line}\n"
    exec(func_code, globals(), local_vars)
    return await local_vars["__aexec"](c, m, r, u)

# Eval command
@app.on_message(filters.command("eval", prefixes=".") & filters.user(OWNER_ID))
async def eval_handler(client: Client, message: Message):
    c, m, r, u = client, message, message.reply_to_message, message
    code = message.text.split(None, 1)
    if len(code) < 2:
        return await message.reply_text("**`No code provided.`**")
    code = code[1]
    try:
        start = time.time()
        result = str(await aexec(code, c, m, r, u)).replace("<", "").replace(">", "")
    except Exception as e:
        result = str(e).replace("<", "").replace(">", "")
    duration = f"__Duration : {time.time() - start:.5f} sec.__"
    try:
        await message.reply_text(
            f"*Input :* `{message.text}`\n\n"
            f"*Output :* ```json\n{result}```\n"
            f"{duration}",
            disable_web_page_preview=True,
        )
    except Exception as e:
        try:
            await message.reply_text(
                f"*Input :* `{message.text}`\n\n"
                f"*Output :* ```json\n{str(e)}```\n"
                f"{duration}",
                disable_web_page_preview=True,
            )
        except Exception as e:
            logging.error(e)

# Run userbot
app.run()
