api_id = 12345
api_hash = "1ksksdoeoekxmxxmdmemmr"
sudo_users = ["me", 8101867786]
send_text_output = False
bot_token = "8343128787:AAG_Itvf97Yi-BAqUs_qky4KdieF-pn-sno"
import aiohttp
import pyrogram
import logging
import uvloop, httpx
from pyrogram import Client, filters, idle
import time, random, os, asyncio, sys, io, base64, json
from pyrogram.types import LinkPreviewOptions
logging.basicConfig(level=logging.INFO)
async def binpaste(data):
    url = "https://batbin.me/api/v2/paste"
    async with aiohttp.ClientSession() as client:
        resp = await client.post(url, data=data)
        if "application/json" in resp.headers.get("content-type", ""):
            return f"https://batbin.me/{(await resp.json())['message']}"
        return resp.text
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
async def xevalfnc(client, message):
    if message.reply_to_message_id:
       message.reply_to_message = await client.get_messages(message.chat.id, message.reply_to_message_id)
    c,m,r,u = client, message, message.reply_to_message, message.reply_to_message.from_user if message.reply_to_message else None
    text = m.text[6:]
    try:
       start_time = time.time()
       output = str(await aexec(text, c, m, r, u)).replace('<','').replace('>','')
    except Exception as e:
       output = str(e).replace('<','').replace('>','')
    link = await binpaste(json.dumps(str(output)))
    total_time = time.time() - start_time
    formatted_time = f"__Duration : {total_time:.5f} sec.__"
    try:
       if message.from_user.id == client.me.id:
           await message.edit_text(f"""**Input :** `{message.text}`\n\n**Output :** ```json\n{str(output)}```\n{formatted_time}  |  [𝕎𝕖𝕓𝕧𝕚𝕖𝕨]({link})""", link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
       else:
           await message.reply_text(f"""**Input :** `{message.text}`\n\n**Output :** ```json\n{str(output)}```\n{formatted_time}  |  [𝕎𝕖𝕓𝕧𝕚𝕖𝕨]({link})""", link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
    except Exception as e2:
       if message.from_user.id == client.me.id:
           await message.edit_text(f"""**Input :** `{message.text}`\n\n**Output :** ```json\n{str(e2)}```\n{formatted_time}  |  [𝕎𝕖𝕓𝕧𝕚𝕖𝕨]({link})""",link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
       else:
           await message.reply_text(f"""**Input :** `{message.text}`\n\n**Output :** ```json\n{str(e2)}```\n{formatted_time}  |  [𝕎𝕖𝕓𝕧𝕚𝕖𝕨]({link})""",link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
       if send_text_output:
           file = io.BytesIO(str(vc).encode())
           file.name = "output.txt"
           try: 
              await message.reply_document(document=file, caption="Couldn't send as text.")
           except Exception as e3: 
              print(e3)
async def main():
    global bot, app
    app = Client("userbot", api_id, api_hash)
    bot = Client("testingbot", api_id, api_hash, bot_token=bot_token)
    @app.on_message(filters.command("eval",["!","/","."]) & filters.user(sudo_users))
    @bot.on_message(filters.command("eval",["!","/","."]) & filters.user(sudo_users))
    async def evalfnc(client, message):
        asyncio.create_task(xevalfnc(client, message))
    await app.start()
    
    await bot.start()
    
    await idle()
    
    await app.start()
    
    await bot.stop()

uvloop.run(main())      
