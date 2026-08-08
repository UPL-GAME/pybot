import asyncio
import json
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import firebase_admin
from firebase_admin import credentials, db

from github import Github, Auth

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
firebase_data = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(firebase_data)
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://test-82a8a-default-rtdb.firebaseio.com/"}
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not BOT_TOKEN or not GITHUB_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN yoki GITHUB_TOKEN Railway Variables'da topilmadi."
    )

g = Github(auth=Auth.Token(GITHUB_TOKEN))
bot = Bot(token=BOT_TOKEN)
z = Dispatcher()

# State (Holat) sinfi

class Form(StatesGroup):
    fA = State()
    fTime = State()

@z.message(Command("clear"))
async def c(message: Message):
    db.reference("/").delete()
    await message.answer("Baza toza")

@z.message(Command("inf"))
async def c(message: Message):
    await message.answer("""https://upl-game.github.io/dasfafafadasdajavoblarvaraqasi-dd-d-d-d-d-d-d-dfbbhf/
https://upl-game.github.io/adgsgsfdzgfdgdzfggzfdgdzgzdfgzdfgzdfgdzfgdzfgzdfgzdfgzdfgz/""")

@z.message(Command("cranswer"))
async def cran(message: Message, state: FSMContext):
    await state.set_state(Form.fA)
    await message.answer("To'g'ri javobni kiriting t.me/idrisxonacademy_robot/json!")

@z.message(Form.fA)
async def cd(message: Message, state: FSMContext):
    tx = message.text
    await state.clear()
    try:
        repo = g.get_repo("UPL-ANIME/bazemath")
        content = repo.get_contents("correctanwers", ref="main")
        repo.update_file(content.path, "ss", tx, content.sha, branch="main")
        await message.answer("kiritildi")
    except Exception as e:
        await message.answer(f"GitHub'ga yozishda xatolik: {e}")

@z.message(Command("time"))
async def c_time(message: Message, state: FSMContext):
    await state.set_state(Form.fTime)
    await message.answer("Test tugash vaqtini kiriting ! t.me/idrisxonacademy_robot/time")

@z.message(Form.fTime)
async def cd_time(message: Message, state: FSMContext):
    tx = message.text
    await state.clear()
    try:
        repo = g.get_repo("UPL-ANIME/bazemath")
        content = repo.get_contents("time", ref="main")
        repo.update_file(content.path, "ss", tx, content.sha, branch="main")
        await message.answer("Vaqt kiritildi")
    except Exception as e:
        await message.answer(f"GitHub'ga yozishda xatolik: {e}")

@z.message(Command("end"))  # /end komandasi berilganda ishlaydi
async def vv(message: Message):
    try:
        bb = db.reference("/").get()
        # Firebase lug'atini (dict) JSON matn ko'rinishiga o'tkazamiz
        bb_str = json.dumps(bb, indent=2, ensure_ascii=False) if bb else "{}"
        repo = g.get_repo("UPL-ANIME/bazemath")
        rsh = repo.get_contents("date", ref="main")
        repo.update_file(
            rsh.path,
            "ss",
            bb_str,  # GitHub'ga matn ko'rinishida yuboramiz
            rsh.sha,
            branch="main",
        )
        await message.answer("Baza ko'chirildi")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot ishga tushdi...")
    try:
        await z.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
