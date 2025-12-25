import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# Քո Տվյալները
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ՍԵՐՎԵՐԻ ՀԱՏՎԱԾ (Render-ի համար) ---
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render-ը սպասում է 10000 պորտին
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

# --- ԲՈՏԻ ՀԱՏՎԱԾ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Բարև: Գրիր խնդրի համարը (1-6):")

@dp.message(F.text)
async def send_solution(message: types.Message):
    if message.text.isdigit():
        file_path = f"images/{message.text}.jpeg"
        if os.path.exists(file_path):
            wait_msg = await message.answer("Սպասման մեջ է... ⏳")
            await asyncio.sleep(3)
            photo = types.FSInputFile(file_path)
            await bot.send_photo(message.chat.id, photo)
            await wait_msg.delete()
        else:
            await message.answer("Նկարը չի գտնվել:")

async def main():
    # Միացնում ենք և՛ սերվերը, և՛ բոտը միաժամանակ
    await start_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
