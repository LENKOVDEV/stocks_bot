import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

import json, re
from GUI import dependence, make_currency

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5256106421:AAFK-LIYbl_LvKMrmkXwTCo0CoVCCwvMuTY'


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

lang = 'ru'

regularExpression = re.compile('[A-Z]{3}')
curMass = [
    'ð²BTCð²',
    'ðETHð',
    'ðºð¸USDðºð¸',
    'ðªðºEURðªðº',
    'ðºð¦UAHðºð¦',
    'ð·ðºRUBð·ðº',
    'ð¬ð§GBPð¬ð§',
    'ðµð±PLNðµð±',
    'ð§ð¾BYNð§ð¾',
    'ð²ð©MDLð²ð©',
    'ð¦ðºAUDð¦ðº',
    'ð§ð¬BGNð§ð¬',
    'ð°ð·KRWð°ð·',
    'ð­ð°HKDð­ð°',
    'ð©ð°DKKð©ð°',
    'ðªð¬EGPðªð¬',
    'ð¯ðµJPYð¯ðµ',
    'ð®ð³INRð®ð³',
    'ð¨ð¦CADð¨ð¦',
    'ð­ð·HRKð­ð·',
    'ð²ð½MXNð²ð½',
    'ð®ð±ILSð®ð±',
    'ð³ð¿NZDð³ð¿',
    'ð³ð´NOKð³ð´',
    'ð¿ð¦ZARð¿ð¦',
    'ð·ð´RONð·ð´',
    'ð®ð©IDRð®ð©',
    'ð¸ð¦SARð¸ð¦',
    'ð¸ð¬SGDð¸ð¬',
    'XDR',
    'ð°ð¿KZTð°ð¿',
    'ð¹ð·TRYð¹ð·',
    'ð­ðºHUFð­ðº',
    'ð¨ð¿CZKð¨ð¿',
    'ð¸ðªSEKð¸ðª',
    'ð¨ð­CHFð¨ð­',
    'ð¨ð³CNYð¨ð³',
    'ð©ð¿DZDð©ð¿',
    'ð§ð©BDTð§ð©',
    'ð¦ð²AMDð¦ð²',
    'ð®ð·IRRð®ð·',
    'ð®ð¶IQDð®ð¶',
    'ð°ð¬KGSð°ð¬',
    'ð±ð§LBPð±ð§',
    'ð±ð¾LYDð±ð¾',
    'ð²ð¾MYRð²ð¾',
    'ð²ð¦MADð²ð¦',
    'ðµð°PKRðµð°',
    'ð»ð³VNDð»ð³',
    'ð¹ð­THBð¹ð­',
    'ð¦ðªAEDð¦ðª',
    'ð¹ð³TNDð¹ð³',
    'ðºð¿UZSðºð¿',
    'ð¹ð²TMTð¹ð²',
    'ð·ð¸RSDð·ð¸',
    'ð¦ð¿AZNð¦ð¿',
    'ð¹ð¯TJSð¹ð¯',
    'ð¬ðªGELð¬ðª',
    'ð§ð·BRLð§ð·',
]

# navigation buttons
navBtns = [
    ['Ð¯Ð·ÑÐº', 'Language', 'ÐÐ¾Ð²Ð°'],
    ['ÐÐ¾Ð½Ð²ÐµÑÑÑÑ', 'Convert', 'ÐÐ¾Ð½Ð²ÐµÑÑÐµÑ'],
    ['ÐÑÑÑ', 'Currency', 'ÐÑÑÑ'],
    ['ÐÐ±Ð½Ð¾Ð²Ð¸ÑÑ', 'Update', 'ÐÐ½Ð¾Ð²Ð¸ÑÐ¸']
]

curMassDict = {}
for i in curMass:
    if len(i) == 7:
        curMassDict[re.findall(regularExpression, i)[0]] = i[0:2]
    elif len(i) == 5:
        curMassDict[re.findall(regularExpression, i)[0]] = i[0:1]
    else:
        curMassDict[re.findall(regularExpression, i)[0]] = ''

curShortMas = [i[0:4] if len(i) != 7 else i[0:5] for i in curMass]


# States
class Convert(StatesGroup):
    currency1 = State()  # Will be represented in storage as 'Form:name'
    currency2 = State()  # Will be represented in storage as 'Form:age'
    value = State()  # Will be represented in storage as 'Form:gender'


class Starting(StatesGroup):
    langSet = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Starting.langSet.set()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Englishð¬ð§", callback_data="en"))
    markup.add(types.InlineKeyboardButton(text="Ð ÑÑÑÐºÐ¸Ð¹ð·ðº", callback_data="ru"))
    markup.add(types.InlineKeyboardButton(text="Ð£ÐºÑÐ°ÑÐ½ÑÑÐºÐ°ðºð¦", callback_data="ua"))

    await message.answer(f'<b>Choose the language</b>\n\n'
                         f'<b>ÐÑÐ±ÐµÑÐ¸ÑÐµ ÑÐ·ÑÐº</b>\n\n'
                         f'<b>ÐÐ±ÐµÑÑÑÑ Ð¼Ð¾Ð²Ñ</b>',
                         parse_mode='html',
                         reply_markup=markup)


@dp.message_handler(Text(equals=navBtns[0]))
@dp.message_handler(commands='lang')
async def change_language(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Englishð¬ð§", callback_data="EN"))
    markup.add(types.InlineKeyboardButton(text="Ð ÑÑÑÐºÐ¸Ð¹ð·ðº", callback_data="RU"))
    markup.add(types.InlineKeyboardButton(text="Ð£ÐºÑÐ°ÑÐ½ÑÑÐºÐ°ðºð¦", callback_data="UA"))

    await message.answer(f'<b>Choose the language</b>\n\n'
                         f'<b>ÐÑÐ±ÐµÑÐ¸ÑÐµ ÑÐ·ÑÐº</b>\n\n'
                         f'<b>ÐÐ±ÐµÑÑÑÑ Ð¼Ð¾Ð²Ñ</b>',
                         parse_mode='html',
                         reply_markup=markup)


@dp.callback_query_handler(text=['EN', 'RU', 'UA'])
async def change_lang(call: types.CallbackQuery):
    global lang
    lang = call.data.lower()
    if lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await call.message.answer('<b>Ð¯Ð·ÑÐº ÑÑÐ¿ÐµÑÐ½Ð¾ Ð¸Ð·Ð¼ÐµÐ½ÑÐ½!</b>', parse_mode='html', reply_markup=markup)
    elif lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer('<b>Language successfully changed!</b>', parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer('<b>ÐÐ¾Ð²Ð° ÑÑÐ¿ÑÑÐ½Ð¾ Ð·Ð¼ÑÐ½ÐµÐ½Ð°!</b>', parse_mode='html', reply_markup=markup)


@dp.callback_query_handler(text=['en', 'ru', 'ua'], state=Starting.langSet)
async def send_random_value(call: types.CallbackQuery, state: FSMContext):
    global lang
    lang = call.data
    if lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer(
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>Ð¡Ð»Ð°Ð²Ð° Ð£ÐºÑÐ°ÑÐ½Ñ!!!</b>\n'
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>Hi, I\'m Stocks Bot!ð¤</b>\n'
            f'My commands:\n'
            f'/convert - convert any currency into another.\n'
            f'/currency - get actual exchange rate.\n'
            f'/lang - to change the language.\n'
            f'/update - to make update all currency by now.'
            f'Currency automatically updating every day.',
            parse_mode='html',
            reply_markup=markup
        )
    elif lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await call.message.answer(
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>Ð¡Ð»Ð°Ð²Ð° Ð£ÐºÑÐ°ÑÐ½Ñ!!!</b>\n'
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>ÐÑÐ¸Ð²ÐµÑ, Ñ ÐÐ¾Ñ ÐÐ¾Ð½Ð²ÐµÑÑÑÑ ÐÐ°Ð»ÑÑ!ð¤</b>\n'
            f'ÐÐ¾Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ:\n'
            f'/convert - ÐºÐ¾Ð½Ð²ÐµÑÑÐ¸ÑÐ¾Ð²Ð°ÑÑ Ð²Ð°Ð»ÑÑÑ Ð² Ð´ÑÑÐ³ÑÑ.\n'
            f'/currency - Ð¿Ð¾Ð»ÑÑÐ¸ÑÑ Ð°ÐºÑÑÐ°Ð»ÑÐ½ÑÐ¹ ÐºÑÑÑ Ð²Ð°Ð»ÑÑÑ.\n'
            f'/lang - ÑÑÐ¾Ð±Ñ Ð¸Ð·Ð¼ÐµÐ½Ð¸ÑÑ ÑÐ·ÑÐº.\n'
            f'/update - Ð¾Ð±Ð½Ð¾Ð²Ð¸ÑÑ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ Ð²Ð°Ð»ÑÑ Ðº Ð°ÐºÑÑÐ°Ð»ÑÐ½ÑÐ¼, ÐµÑÐ»Ð¸ Ð¿ÑÐ¾Ð¸ÑÑÐ¾Ð´Ð¸Ð»Ð¸ Ð¸Ð·Ð¼ÐµÐ½ÐµÐ½Ð¸Ñ Ð½Ð° ÑÑÐ½ÐºÐµ.'
            f'ÐÐ½Ð°ÑÐµÐ½Ð¸Ñ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸ÑÐµÑÐºÐ¸ Ð¾Ð±Ð½Ð¾Ð²Ð»ÑÑÑÑÑ ÐµÐ¶ÐµÐ´Ð½ÐµÐ²Ð½Ð¾.',
            parse_mode='html',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await call.message.answer(
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>Ð¡Ð»Ð°Ð²Ð° Ð£ÐºÑÐ°ÑÐ½Ñ!!!</b>\n'
            f'ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦ðºð¦\n'
            f'<b>ÐÑÐ¸Ð²ÑÑ, Ð¯ ÐÐ¾Ñ ÐÐ¾Ð½Ð²ÐµÑÑÐµÑ ÐÐ°Ð»ÑÑ!ð¤</b>\n'
            f'ÐÐ¾Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ð¸:\n'
            f'/convert - ÐºÐ¾Ð½Ð²ÐµÑÑÑÐ²Ð°ÑÐ¸ Ð²Ð°Ð»ÑÑÑ Ð² ÑÐ½ÑÑ.\n'
            f'/currency - Ð¾ÑÑÐ¸Ð¼Ð°ÑÐ¸ Ð°ÐºÑÑÐ°Ð»ÑÐ½Ð¸Ð¹ ÐºÑÑÑ Ð²Ð°Ð»ÑÑÐ¸.\n'
            f'/lang - ÑÐ¾Ð± Ð·Ð¼ÑÐ½Ð¸ Ð¼Ð¾Ð²Ñ.\n'
            f'/update - Ð¾Ð±Ð½Ð¾Ð²Ð¸ÑÐ¸ Ð·Ð½Ð°ÑÐµÐ½Ð½Ñ Ð²Ð°Ð»ÑÑÐ¸ Ð´Ð¾ Ð°ÐºÑÑÐ°Ð»ÑÐ½Ð¸Ñ, ÑÐºÑÐ¾ Ð±ÑÐ»Ð¸ Ð·Ð¼ÑÐ½Ð¸ Ð½Ð° ÑÐ¸Ð½ÐºÑ.'
            f'ÐÐ½Ð°ÑÐµÐ½Ð½Ñ Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸ÑÐ½Ð¾ Ð¾Ð½Ð¾Ð²Ð»ÑÑÑÑÑÑ ÐºÐ¾Ð¶ÐµÐ½ Ð´ÐµÐ½Ñ.',
            parse_mode='html',
            reply_markup=markup
        )

    await state.finish()


@dp.message_handler(Text(equals=navBtns[2]))
@dp.message_handler(commands='currency')
async def currency(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add('âï¸ALLâï¸')
    massive = curShortMas
    markup.add(*massive)
    if lang == 'en':
        await message.reply('Choose currency you wanna to get', reply_markup=markup)
    elif lang == 'ru':
        await message.reply('ÐÑÐ±ÐµÑÐµÑÐµ Ð²Ð°Ð»ÑÑÑ, ÐºÐ¾ÑÐ¾ÑÑÑ ÑÐ¾ÑÐ¸ÑÐµ Ð¿ÐµÑÐµÐ²ÐµÑÑÐ¸', reply_markup=markup)
    else:
        await message.reply('ÐÐ¸Ð±ÐµÑÑÑÑ Ð²Ð°Ð»ÑÑÑ, ÑÐºÑ ÑÐ¾ÑÐµÑÐµ Ð¿ÐµÑÐµÐ²ÐµÑÑÐ¸', reply_markup=markup)

@dp.message_handler(Text(equals=navBtns[3]))
@dp.message_handler(commands='update')
async def update(message: types.Message):
    make_currency()
    if lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await message.answer('ð¢<b>Data was successfully updated</b>ð¢', parse_mode='html', reply_markup=markup)
    elif lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await message.answer('ð¢<b>ÐÐ°Ð½Ð½ÑÐµ ÑÑÐ¿ÐµÑÐ½Ð¾ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ñ</b>ð¢', parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer('ð¢<b>ÐÐ°Ð½Ñ ÑÑÐ¿ÑÑÐ½Ð¾ Ð¾Ð½Ð¾Ð²Ð»ÐµÐ½Ñ</b>ð¢', parse_mode='html', reply_markup=markup)


@dp.message_handler(Text(equals=curShortMas))
async def one_currency(message: types.Message):
    file = json.load(open('currency.json'))
    text = re.findall(regularExpression, message.text)[0]
    if lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await message.answer(f'Exchange of {text}\n'
                             f'<b>{round(file[text], 4)}</b>\n\n'
                             f'Last update was\n'
                             f'at <i>{file["update"]}</i>\n\n'
                             f'Use /update\n'
                             f'if you want to update data',
                             parse_mode='html',
                             reply_markup=markup
                             )
    elif lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await message.answer(f'ÐÑÑÑ {text}\n'
                             f'<b>{round(file[text], 4)}</b>\n\n'
                             f'ÐÐ¾ÑÐ»ÐµÐ´Ð½ÐµÐµ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ\n'
                             f'Ð² <i>{file["update"]}</i>\n\n'
                             f'ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ÑÐµ /update\n'
                             f'ÐµÑÐ»Ð¸ ÑÐ¾ÑÐ¸ÑÐµ Ð¾Ð±Ð½Ð¾Ð²Ð¸ÑÑ Ð´Ð°Ð½Ð¸Ðµ',
                             parse_mode='html',
                             reply_markup=markup
                             )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer(f'ÐÑÑÑ {text}\n'
                             f'<b>{round(file[text], 4)}</b>\n\n'
                             f'ÐÑÑÐ°Ð½Ð½Ñ Ð¾Ð½Ð¾Ð²Ð»ÐµÐ½Ð½Ñ\n'
                             f'Ð¾ <i>{file["update"]}</i>\n\n'
                             f'ÐÐ¸ÐºÐ¾ÑÐ¸ÑÑÐ¾Ð²ÑÐ¹ÑÐµ /update\n'
                             f'ÑÐºÑÐ¾ Ð²Ð¸ ÑÐ¾ÑÐµÑÐµ Ð¾Ð½Ð¾Ð²Ð¸ÑÐ¸ Ð´Ð°Ð½Ñ',
                             parse_mode='html',
                             reply_markup=markup
                             )


@dp.message_handler(Text(equals='âï¸ALLâï¸'))
async def all_currency(message: types.Message):
    file = json.load(open('currency.json'))
    result = ''
    for k, v in file.items():
        if len(k) == 3:
            flag = curMassDict[k]
            result += f'{flag}{k}{flag} - {round(v, 4)}\n'

    if lang == 'eu':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await message.answer(
            f'<b>{result}</b>\n\n'
            f'Last update was\n'
            f'at <i>{file["update"]}</i>\n\n'
            f'Use /update\n'
            f'if you want to update data',
            parse_mode='html',
            reply_markup=markup
        )
    elif lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await message.answer(
            f'<b>{result}</b>\n\n'
            f'ÐÐ¾ÑÐ»ÐµÐ´Ð½ÐµÐµ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ\n'
            f'Ð² <i>{file["update"]}</i>\n\n'
            f'ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ÑÐµ /update\n'
            f'ÐµÑÐ»Ð¸ Ð²Ñ ÑÐ¾ÑÐ¸ÑÐµ Ð¾Ð±Ð½Ð¾Ð²Ð¸ÑÑ Ð´Ð°Ð½Ð½ÑÐµ',
            parse_mode='html',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer(
            f'<b>{result}</b>\n\n'
            f'ÐÑÑÐ°Ð½Ð½Ñ Ð¾Ð½Ð¾Ð²Ð»ÐµÐ½Ð½Ñ\n'
            f'Ð¾ <i>{file["update"]}</i>\n\n'
            f'ÐÐ¸ÐºÐ¾ÑÐ¸ÑÑÐ¾Ð²ÑÐ¹ÑÐµ /update\n'
            f'ÑÐºÑÐ¾ Ð²Ð¸ ÑÐ¾ÑÐµÑÐµ Ð¾Ð½Ð¾Ð²Ð¸ÑÐ¸ Ð´Ð°Ð½Ñ',
            parse_mode='html',
            reply_markup=markup
        )


@dp.message_handler(Text(navBtns[1]))
@dp.message_handler(commands='convert')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Convert.currency1.set()

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add(*curMass)

    if lang == 'en':
        await message.reply("Choose your currency", reply_markup=markup)
    elif lang == 'ru':
        await message.reply("ÐÑÐ±ÐµÑÐ¸ÑÐµ Ð²Ð°Ð»ÑÑÑ", reply_markup=markup)
    else:
        await message.reply("ÐÐ±ÐµÑÑÑÑ Ð²Ð°Ð»ÑÑÑ", reply_markup=markup)


@dp.message_handler(lambda message: message.text.lower() not in [cur.lower() for cur in json.load(open('currency.json'))] and message.text not in curMass, state=Convert.currency1)
async def process_cur1_invalid(message: types.Message):
    """
    If cur1 is invalid
    """
    if lang == 'en':
        return await message.reply('Currency gotta be in format "usd"\n\nOr choose with buttons')
    elif lang == 'ru':
        return await message.reply('ÐÐ°Ð»ÑÑÐ° Ð´Ð¾Ð»Ð¶Ð½Ð° Ð±ÑÑÑ Ð² ÑÐ¾ÑÐ¼Ð°ÑÐµ "usd"\n\nÐÐ»Ð¸ Ð²ÑÐ±ÐµÑÐ¸ÑÐµ Ñ Ð¿Ð¾Ð¼Ð¾ÑÑÑ ÐºÐ½Ð¾Ð¿Ð¾Ðº')
    else:
        return await message.reply('ÐÐ°Ð»ÑÑÐ° Ð¿Ð¾Ð²Ð¸Ð½Ð½Ð° Ð±ÑÑÐ¸ Ð² ÑÐ¾ÑÐ¼Ð°ÑÑ "usd"\n\nÐÐ±Ð¾ Ð²Ð¸Ð±ÐµÑÑÑÑ Ð·Ð° Ð´Ð¾Ð¿Ð¾Ð¼Ð¾Ð³Ð¾Ñ')


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Convert.currency1)
async def process_cur1(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        if len(message.text) > 3:
            data['cur1'] = re.findall(regularExpression, message.text)[0].lower()
        else:
            data['cur1'] = message.text.lower()

    await Convert.next()
    if lang == 'en':
        await message.reply("<b>Choose currency convert toð:</b>", parse_mode='html')
    elif lang == 'ru':
        await message.reply("<b>ÐÑÐ±ÐµÑÐµÑÐµ Ð²Ð°Ð»ÑÑÑ Ð² ÐºÐ¾ÑÐ¾ÑÑÑ ÐºÐ¾Ð½Ð²ÐµÑÑÐ¸ÑÐ¾Ð²Ð°ÑÑð:</b>", parse_mode='html')
    else:
        await message.reply("<b>ÐÐ±ÐµÑÑÑÑ Ð²Ð°Ð»ÑÑÑ Ð² ÑÐºÑ ÐºÐ¾Ð½Ð²ÐµÑÑÑÐ²Ð°ÑÐ¸ð:</b>", parse_mode='html')


# Check age. Age gotta be digit
@dp.message_handler(lambda message: message.text.lower() not in [cur.lower() for cur in json.load(open('currency.json'))] and message.text not in curMass, state=Convert.currency2)
async def process_cur2_invalid(message: types.Message):
    """
    If cur2 is invalid
    """
    if lang == 'en':
        return await message.reply('Currency gotta be inf format "usd"\n\nOr choose with buttons')
    elif lang == 'ru':
        return await message.reply('ÐÐ°Ð»ÑÑÐ° Ð´Ð¾Ð»Ð¶Ð½Ð° Ð±ÑÑÑ Ð² ÑÐ¾ÑÐ¼Ð°ÑÐµ "usd"\n\nÐÐ»Ð¸ Ð²ÑÐ±ÐµÑÐ¸ÑÐµ Ñ Ð¿Ð¾Ð¼Ð¾ÑÑÑ ÐºÐ½Ð¾Ð¿Ð¾Ðº')
    else:
        return await message.reply('ÐÐ°Ð»ÑÑÐ° Ð¿Ð¾Ð²Ð¸Ð½Ð½Ð° Ð±ÑÑÐ¸ Ð² ÑÐ¾ÑÐ¼Ð°ÑÑ "usd"\n\nÐÐ±Ð¾ Ð²Ð¸Ð±ÐµÑÑÑÑ Ð·Ð° Ð´Ð¾Ð¿Ð¾Ð¼Ð¾Ð³Ð¾Ñ')


@dp.message_handler(lambda message: message.text.lower() in [cur.lower() for cur in json.load(open('currency.json'))] or message.text in curMass, state=Convert.currency2)
async def process_cur2(message: types.Message, state: FSMContext):
    # Update state and data
    await Convert.next()
    if len(message.text) > 3:
        await state.update_data(cur2=re.findall(regularExpression, message.text)[0].lower())
    else:
        await state.update_data(cur2=message.text.lower())

    if lang == 'en':
        await message.reply("What is value?", reply_markup=types.ReplyKeyboardRemove())
    elif lang == 'ru':
        await message.reply("ÐÐ°ÐºÐ°Ñ ÑÑÐ¼Ð°?", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply("Ð¯ÐºÐ° ÑÑÐ¼Ð°?", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isdigit(), state=Convert.value)
async def process_value_invalid(message: types.Message):
    """
    In this example value has to be digit one.
    """
    if lang == 'en':
        return await message.reply("Value must be a number.")
    elif lang == 'ru':
        return await message.reply("ÐÐ½Ð°ÑÐµÐ½Ð¸Ðµ Ð´Ð¾Ð»Ð¶Ð½Ð¾ Ð±ÑÑÑ ÑÐ¸ÑÐ»Ð¾Ð¼.")
    else:
        return await message.reply("ÐÐ½Ð°ÑÐµÐ½Ð½Ñ Ð¿Ð¾Ð²Ð¸Ð½Ð½Ð¾ Ð±ÑÑÐ¸ ÑÐ¸ÑÐ»Ð¾Ð¼.")


@dp.message_handler(lambda message: message.text.isdigit(), state=Convert.value)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = int(message.text)

        updated = json.load(open('currency.json'))['update']

        result = dependence(data['cur1'], data['cur2'], data['value'])

        # And send message
        if lang == 'en':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add(*[i[1] for i in navBtns])
            await bot.send_message(
                message.chat.id,
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'to\n'
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'EQUALS\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'ðµðµðµðµðµ\n\n'
                f'Last update was\n'
                f'at <i>{updated}</i>\n\n'
                f'Use /update\n'
                f'if you want to update data',
                parse_mode='html',
                reply_markup=markup
            )
        elif lang == 'ru':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add(*[i[0] for i in navBtns])
            await bot.send_message(
                message.chat.id,
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'Ð²\n'
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'Ð ÐÐÐÐ\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'ðµðµðµðµðµ\n\n'
                f'ÐÐ¾ÑÐ»ÐµÐ´Ð½ÐµÐµ Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ\n'
                f'Ð² <i>{updated}</i>\n\n'
                f'ÐÑÐ¿Ð¾Ð»ÑÐ·ÑÐ¹ÑÐµ /update\n'
                f'ÐµÑÐ»Ð¸ Ð²Ñ ÑÐ¾ÑÐ¸ÑÐµ Ð¾Ð±Ð½Ð¾Ð²Ð¸ÑÑ Ð´Ð°Ð½Ð½ÑÐµ Ðº Ð°ÐºÑÑÐ°Ð²Ð»ÑÐ½ÑÐ¼',
                parse_mode='html',
                reply_markup=markup
            )
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add(*[i[2] for i in navBtns])
            await bot.send_message(
                message.chat.id,
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'Ñ\n'
                f'ðµðµðµðµðµ\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'ðµðµðµðµðµ\n'
                f'ÐÐÐ ÐÐÐÐ®Ð\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'ðµðµðµðµðµ\n\n'
                f'ÐÑÑÐ°Ð½Ð½Ñ Ð¾Ð½Ð¾Ð²Ð»ÐµÐ½Ð½Ñ\n'
                f'Ð¾ <i>{updated}</i>\n\n'
                f'ÐÐ¸ÐºÐ¾ÑÐ¸ÑÑÐ¾Ð²ÑÐ¹ÑÐµ /update\n'
                f'ÑÐºÑÐ¾ Ð²Ð¸ ÑÐ¾ÑÐµÑÐµ Ð¾Ð½Ð¾Ð²Ð¸ÑÐ¸ Ð´Ð°Ð½Ñ Ð´Ð¾ Ð°ÐºÑÑÐ°Ð»ÑÐ½Ð¸Ñ',
                parse_mode='html',
                reply_markup=markup
            )

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)