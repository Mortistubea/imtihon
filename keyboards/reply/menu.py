from aiogram.types import ReplyKeyboardMarkup,KeyboardButton



user_menu = ReplyKeyboardMarkup(

    keyboard=[

        [
            KeyboardButton("Kursga yozilish"),
        ],
        [
            KeyboardButton("Filiallar"),
            KeyboardButton("Profil"),
        ],
        [
            KeyboardButton("Kontakt"),
            KeyboardButton("Baholash"),
        ],
        [
            KeyboardButton("Sozlamalar"),
        ],
        
    ],
    resize_keyboard=True,
    one_time_keyboard=True

)


baholash = ReplyKeyboardMarkup(

    keyboard=[

        [
            KeyboardButton("      ⭐️       "),
        ],
        [
            KeyboardButton("      ⭐️⭐️       "),
        ],
        [
            KeyboardButton("      ⭐️⭐️⭐️       "),
        ],
        [
            KeyboardButton("      ⭐️⭐️⭐️⭐️       "),
        ],
        [
            KeyboardButton("      ⭐️⭐️⭐️⭐️⭐️       "),
        ],
    ]

)



filiallar = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("💻Tinchlik"),
            KeyboardButton("💻Yunusobod"),
        ],
        [
            KeyboardButton("💻Buyuk ipak yoli"),
            KeyboardButton("💻Sergeli"),
        ],
        [
            KeyboardButton("💻Chilonzor"),
        ],
        [
            KeyboardButton("🔙 Orqaga")  # Orqaga tugmasi qo'shildi
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
