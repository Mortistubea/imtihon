import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp,bot
from states.ms import Example
from data.config import ADMINS
from database.base import create_connection,create_table,add_user_to_db
from keyboards.reply.menu import user_menu,baholash,filiallar
import sqlite3

# 2. Botda xabarlarni qayta ishlash
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    global ADMIN_CHAT_ID
    ADMIN_CHAT_ID = message.from_user.id  # Adminning chat_id sini olish
    await message.answer(f"Salom, {message.from_user.full_name}!",reply_markup=user_menu)
    create_table()  # Dastur ishga tushganda jadval yaratib qo'yamiz


# @dp.message_handler(text="Kursga yozilish")
# async def s_handler(message: types.Message):
#     await Example.name.set()
#     await message.answer("Iltimos, ismingizni kiriting")


@dp.message_handler(text="Kursga yozilish")
async def s_handler(message: types.Message):
    phone_number = message.from_user

    await Example.name.set()
    await message.answer("Iltimos, ismingizni kiriting")




@dp.message_handler(state=Example.name)
async def name_handler(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)  # Foydalanuvchi ismini saqlash
    await Example.familya.set()
    await message.answer("Iltimos, familiyangizni kiriting")


@dp.message_handler(state=Example.familya)
async def familya_handler(message: types.Message, state: FSMContext):
    familya = message.text
    await state.update_data(familya=familya)  # Foydalanuvchi familiyasini saqlash
    await Example.age.set()
    await message.answer("Iltimos, yoshingizni kiriting")


@dp.message_handler(state=Example.age)
async def age_handler(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)  # Foydalanuvchi yoshini saqlash
    await Example.phone_number.set()
    await message.answer("Iltimos, telefon raqamingizni kiriting")

@dp.message_handler(state=Example.phone_number)
async def phone_number_handler(message: types.Message, state: FSMContext):
    phone_number = message.text

    # Foydalanuvchi ismi, familiyasi, yoshi va telefon raqamini olish
    user_data = await state.get_data()
    name = user_data.get("name")
    familya = user_data.get("familya")
    age = user_data.get("age")

    # Foydalanuvchini bazaga qo'shish
    add_user_to_db(name, familya, age, phone_number)
    text = f"Yozilgan ism: {name}, Familiya: {familya}, Yosh: {age}, Telefon: {phone_number}. Baza saqlandi."

    # Adminlarga xabar yuborish
    for admin_id in ADMINS:
        await bot.send_message(chat_id=admin_id, text=text)

    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
    await state.finish()



@dp.message_handler(text="Baholash")
async def baholash_handler(message: types.Message):
    # Baholash klaviaturasini yuborish
    await message.answer("Iltimos, bahoni tanlang:", reply_markup=baholash)

@dp.message_handler(lambda message: message.text in ["⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"])
async def baholash_star_handler(message: types.Message, state: FSMContext):
    # Bahoni olish
    stars = message.text.strip()

    if stars in ["⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"]:
        # 4 yoki 5 yulduz uchun
        await message.answer("FIKRINGIZ UCHUN RAXMAT!")

        # Adminlarga xabar yuborish
        admin_message = (
            f"   Yangi baho:\n     "
            f"Baholash: {stars}\n"  # Bahoni ham yuboramiz
            f"Foydalanuvchi: {message.from_user.full_name} ({message.from_user.id}) ({message.from_user.username})"
        )
        for admin_id in ADMINS:
            await bot.send_message(chat_id=admin_id, text=admin_message)

        # Foydalanuvchini bosh menuga qaytarish
        await message.answer("Bosh menuga qaytish", reply_markup=user_menu)
    else:
        # 1, 2 yoki 3 yulduz uchun izoh qoldirishni so'rash
        await message.answer("Iltimos, izoh qoldiring:")
        await Example.baho_izoh.set()  # Holatni `baho_izoh` ga o'zgartiramiz
        await state.update_data(stars=stars)  # Bahoni holatda saqlash




@dp.message_handler(state=Example.baho_izoh)
async def baho_izoh_handler(message: types.Message, state: FSMContext):
    izoh = message.text  # Foydalanuvchi qoldirgan izoh
    user_data = await state.get_data()
    stars = user_data.get("stars")  # Oldin kiritilgan baho

    # Adminlarga xabar yuborish
    admin_message = (
        f"Baholash: {stars}\n"  # Baholashni ham qo'shamiz
        f"Izoh: {izoh}\n"
        f"Foydalanuvchi: {message.from_user.full_name} ({message.from_user.id}) ({message.from_user.username})"
    )
    for admin_id in ADMINS:
        await bot.send_message(chat_id=admin_id, text=admin_message)

    # Foydalanuvchiga javob berish va bosh menuga qaytarish
    await message.answer("Fikringiz uchun raxmat!", reply_markup=user_menu)
    
    # State-ni tugatish
    await state.finish()






# Filiallar tugmasini bosganda klaviatura chiqsin
@dp.message_handler(text="Filiallar")
async def filiallar_handler(message: types.Message):
    await message.answer("Filialni tanlang:", reply_markup=filiallar)

# Har bir filial uchun manzilni yuborish
@dp.message_handler(text="💻Tinchlik")
async def tinchlik_handler(message: types.Message):
    await message.answer("Tinchlik filial manzili: https://www.google.com/maps/place/MARS+IT+School/...")

@dp.message_handler(text="💻Yunusobod")
async def yunusobod_handler(message: types.Message):
    await message.answer("Yunusobod filial manzili: https://www.google.com/maps/place/MARS+IT+School+yunusobod/...")

@dp.message_handler(text="💻Buyuk ipak yoli")
async def buyuk_ipak_yoli_handler(message: types.Message):
    await message.answer("Buyuk Ipak Yo'li filial manzili: https://www.google.com/maps/place/MARS+IT+School/...")

@dp.message_handler(text="💻Sergeli")
async def sergeli_handler(message: types.Message):
    await message.answer("Sergeli filial manzili: https://www.google.com/maps/place/MARS+IT+School/...")

@dp.message_handler(text="💻Chilonzor")
async def chilonzor_handler(message: types.Message):
    await message.answer("Chilonzor filial manzili: https://www.google.com/maps/place/MARS+IT+School/...")


# Orqaga tugmasini bosganda bosh menyuga qaytarish
@dp.message_handler(text="🔙 Orqaga")
async def orqaga_handler(message: types.Message):
    await message.answer("Bosh menyu", reply_markup=user_menu)


@dp.message_handler(text="Profil")
async def profile_handler(message: types.Message):
    await message.answer("Buq qismi hali ishlamaydi")



@dp.message_handler(text="Kontakt")
async def profile_handler(message: types.Message):
    text = "    Biz bilan bog'lanish uchun    \n"
    text += "TEL: +9981234567\n"
    text += "Admin: @mortistubea\n"
    await message.answer(text)


@dp.message_handler(text="Sozlamalar")
async def profile_handler(message: types.Message):
    await message.answer("Bu qismi imtohonda yuq")














