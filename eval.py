from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

API_ID = 
API_HASH = ""
OWNER_ID = 7110457701  # Only this user can eval

app = Client("sahil", api_id=API_ID, api_hash=API_HASH)

async def aexec(code, c, m, r, u):
    local_vars = {}
    lines = code.strip().split("\n")
    func_code = "async def __aexec(c, m, r, u):\n"
    if len(lines) == 1 and not lines[0].strip().startswith(
        ("return", "import", "for", "if", "while", "def", "async")
    ):
        func_code += f"    return {lines[0]}\n"
    else:
        for line in lines:
            func_code += f"    {line}\n"
    exec(func_code, globals(), local_vars)
    return await local_vars["__aexec"](c, m, r, u)

@app.on_message(filters.command("eval", prefixes=".") & filters.user(OWNER_ID))
async def eval_handler(client: Client, message: Message):
    c, m, r, u = client, message, message.reply_to_message, message

    # Get code from message or reply
    if message.text:
        parts = message.text.split(None, 1)
        code = parts[1] if len(parts) > 1 else ""
    else:
        code = ""

    # If still no code, try from replied text
    if not code and r and r.text:
        code = r.text

    if not code:
        return await message.reply_text("⚠️ **No code provided.**\nUse `.eval <code>` or reply to code.")

    try:
        start = time.time()
        result = str(await aexec(code, c, m, r, u)).replace("<", "").replace(">", "")
    except Exception as e:
        result = str(e).replace("<", "").replace(">", "")
    duration = f"__Duration : {time.time() - start:.5f} sec.__"

    output = (
        f"**Input :** ```\n{code}```\n\n"
        f"**Output :** ```json\n{result}```\n"
        f"{duration}"
    )

    try:
        await message.reply_text(output, disable_web_page_preview=True)
    except Exception as e:
        logging.error(e)
        await message.reply_text(f"❌ **Error sending output:** `{e}`")

app.run()
