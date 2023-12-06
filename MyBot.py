import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)

group_chat_id = -1001846121545

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Hello {message.from_user.first_name}")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Rus"), KeyboardButton("Eng"), KeyboardButton("Uzb")
    )
    await bot.send_message(chat_id=message.chat.id, text="Choose language:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ['Rus', 'Eng', 'Uzb'])
async def handle_language_choice(message: types.Message):
    user_name = message.from_user.first_name
    language = message.text.lower()
    phone_number = message.text.lower()

    greetings = {
        'rus': f"Привет {user_name}\nНапишите ваше сообщение, и я отвечу вам в ближайшее время.",
        'eng': f"Hello {user_name}\nWrite your message, and I'll contact you.",
        'uzb': f"Salom {user_name}\nXabaringizni yozing, men siz bilan bog'lanaman."
    }
    share_phone = {
        'rus': "Сначала, пожалуйсте поделитесь номером, чтобы я смог связаться с вами",
        'eng': "At first, please share your number so I can contact you",
        'uzb': "Boshida, Iltimos, siz bilan bog'lanishim uchun raqamingizni baham ko'ring"
    }

    welcome = {
        'rus': "Спасибо",
        'eng': "Thank You",
        'uzb': "Raxmat"
    }

    await message.answer(greetings.get(language, "Invalid language choice"), reply_markup=ReplyKeyboardRemove())


    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton(f"share phone number", request_contact=True)
    )

    await message.answer(share_phone.get(phone_number), reply_markup=keyboard)

@dp.message_handler(content_types=[types.ContentType.CONTACT])
async def handle_contact(message: types.Message):
    global contact, phone_number
    contact = message.contact
    phone_number = contact.phone_number
    await message.answer("Thank You", reply_markup=ReplyKeyboardRemove())

@dp.message_handler()
async def handle_user_reply(message: types.Message):
    user_reply = message.text
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    print(f"User replied: {user_reply}\nfirst_name: {user_name}\nuser_ID: {user_id}\n\n\n User PhoneNumber:")
    await bot.send_message(
        chat_id=group_chat_id,
        text=f"User replied: {user_reply}\n\nfirst_name: {user_name}\n\nId: {user_id}\n\nuser phone_number: +{phone_number}  \n\n\nMessage from @techKhasanov_bot"
    )

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=False)
