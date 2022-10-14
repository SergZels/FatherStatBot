from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton("/Внести_виручку")
b2=KeyboardButton("/Місяць")
b3=KeyboardButton("/Рік")

kbcl = ReplyKeyboardMarkup(resize_keyboard=True)
kbcl.add(b1).add(b2,b3)