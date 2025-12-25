import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

# ԿԱՐԵՎՈՐ ՓՈՓՈԽՈՒԹՅՈՒՆ Render-ի համար:
# Մենք թոքենը չենք գրում այստեղ: 
# Բոտը այն կվերցնի "BOT_TOKEN" անունով Environment Variable-ից:
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Պանակի հասցեն (աշխատում է թե՛ համակարգչիդ վրա, թե՛ սերվերում)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Բարև! 👋\n"
        "Գրի'ր խնդրի համարը (օրինակ՝ 1, 2, 3...)"
    )

@dp.message()
async def get_number(message: types.Message):
    text = message.text.strip()
    
    # Ստուգում ենք՝ արդյոք օգտատերը թիվ է գրել
    if not text.isdigit():
        await message.answer("Խնդրում եմ մուտքագրել միայն թիվ (օրինակ՝ 5):")
        return

    file_name = f"{text}.jpeg"
    image_path = os.path.join(IMAGES_FOLDER, file_name)

    if os.path.exists(image_path):
        waiting_msg = await message.answer("Սպասման մեջ է... ⏳")
        await asyncio.sleep(3)
        
        photo = FSInputFile(image_path)
        await message.answer_photo(photo=photo, caption=f"Խնդիր №{text}")
        
        # Օգտագործում ենք try/except, որ եթե հանկարծ սխալ լինի ջնջելիս, բոտը չանջատվի
        try:
            await waiting_msg.delete()
        except:
            pass
    else:
        await message.answer(f"Նկարը `{file_name}` չի գտնվել: 📘")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Բոտը կանգնեցված է")