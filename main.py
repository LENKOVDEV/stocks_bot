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
    '💲BTC💲',
    '💎ETH💎',
    '🇺🇸USD🇺🇸',
    '🇪🇺EUR🇪🇺',
    '🇺🇦UAH🇺🇦',
    '🇷🇺RUB🇷🇺',
    '🇬🇧GBP🇬🇧',
    '🇵🇱PLN🇵🇱',
    '🇧🇾BYN🇧🇾',
    '🇲🇩MDL🇲🇩',
    '🇦🇺AUD🇦🇺',
    '🇧🇬BGN🇧🇬',
    '🇰🇷KRW🇰🇷',
    '🇭🇰HKD🇭🇰',
    '🇩🇰DKK🇩🇰',
    '🇪🇬EGP🇪🇬',
    '🇯🇵JPY🇯🇵',
    '🇮🇳INR🇮🇳',
    '🇨🇦CAD🇨🇦',
    '🇭🇷HRK🇭🇷',
    '🇲🇽MXN🇲🇽',
    '🇮🇱ILS🇮🇱',
    '🇳🇿NZD🇳🇿',
    '🇳🇴NOK🇳🇴',
    '🇿🇦ZAR🇿🇦',
    '🇷🇴RON🇷🇴',
    '🇮🇩IDR🇮🇩',
    '🇸🇦SAR🇸🇦',
    '🇸🇬SGD🇸🇬',
    'XDR',
    '🇰🇿KZT🇰🇿',
    '🇹🇷TRY🇹🇷',
    '🇭🇺HUF🇭🇺',
    '🇨🇿CZK🇨🇿',
    '🇸🇪SEK🇸🇪',
    '🇨🇭CHF🇨🇭',
    '🇨🇳CNY🇨🇳',
    '🇩🇿DZD🇩🇿',
    '🇧🇩BDT🇧🇩',
    '🇦🇲AMD🇦🇲',
    '🇮🇷IRR🇮🇷',
    '🇮🇶IQD🇮🇶',
    '🇰🇬KGS🇰🇬',
    '🇱🇧LBP🇱🇧',
    '🇱🇾LYD🇱🇾',
    '🇲🇾MYR🇲🇾',
    '🇲🇦MAD🇲🇦',
    '🇵🇰PKR🇵🇰',
    '🇻🇳VND🇻🇳',
    '🇹🇭THB🇹🇭',
    '🇦🇪AED🇦🇪',
    '🇹🇳TND🇹🇳',
    '🇺🇿UZS🇺🇿',
    '🇹🇲TMT🇹🇲',
    '🇷🇸RSD🇷🇸',
    '🇦🇿AZN🇦🇿',
    '🇹🇯TJS🇹🇯',
    '🇬🇪GEL🇬🇪',
    '🇧🇷BRL🇧🇷',
]

# navigation buttons
navBtns = [
    ['Язык', 'Language', 'Мова'],
    ['Конвертёр', 'Convert', 'Конвертер'],
    ['Курс', 'Currency', 'Курс'],
    ['Обновить', 'Update', 'Оновити']
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
    markup.add(types.InlineKeyboardButton(text="English🇬🇧", callback_data="en"))
    markup.add(types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"))
    markup.add(types.InlineKeyboardButton(text="Українська🇺🇦", callback_data="ua"))

    await message.answer(f'<b>Choose the language</b>\n\n'
                         f'<b>Выберите язык</b>\n\n'
                         f'<b>Оберіть мову</b>',
                         parse_mode='html',
                         reply_markup=markup)


@dp.message_handler(Text(equals=navBtns[0]))
@dp.message_handler(commands='lang')
async def change_language(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="English🇬🇧", callback_data="EN"))
    markup.add(types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="RU"))
    markup.add(types.InlineKeyboardButton(text="Українська🇺🇦", callback_data="UA"))

    await message.answer(f'<b>Choose the language</b>\n\n'
                         f'<b>Выберите язык</b>\n\n'
                         f'<b>Оберіть мову</b>',
                         parse_mode='html',
                         reply_markup=markup)


@dp.callback_query_handler(text=['EN', 'RU', 'UA'])
async def change_lang(call: types.CallbackQuery):
    global lang
    lang = call.data.lower()
    if lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await call.message.answer('<b>Язык успешно изменён!</b>', parse_mode='html', reply_markup=markup)
    elif lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer('<b>Language successfully changed!</b>', parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer('<b>Мова успішно змінена!</b>', parse_mode='html', reply_markup=markup)


@dp.callback_query_handler(text=['en', 'ru', 'ua'], state=Starting.langSet)
async def send_random_value(call: types.CallbackQuery, state: FSMContext):
    global lang
    lang = call.data
    if lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await call.message.answer(
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Слава Україні!!!</b>\n'
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Hi, I\'m Stocks Bot!🤖</b>\n'
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
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Слава Україні!!!</b>\n'
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Привет, я Бот Конвертёр Валют!🤖</b>\n'
            f'Мои команды:\n'
            f'/convert - конвертировать валюту в другую.\n'
            f'/currency - получить актуальный курс валюты.\n'
            f'/lang - чтобы изменить язык.\n'
            f'/update - обновить значение валют к актуальным, если происходили изменения на рынке.'
            f'Значения автоматически обновляются ежедневно.',
            parse_mode='html',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await call.message.answer(
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Слава Україні!!!</b>\n'
            f'🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦🇺🇦\n'
            f'<b>Привіт, Я Бот Конвертер Валют!🤖</b>\n'
            f'Мої команди:\n'
            f'/convert - конвертувати валюту в іншу.\n'
            f'/currency - отримати актуальний курс валюти.\n'
            f'/lang - щоб зміни мову.\n'
            f'/update - обновити значення валюти до актуальних, якщо були зміни на ринку.'
            f'Значення автоматично оновлюється кожен день.',
            parse_mode='html',
            reply_markup=markup
        )

    await state.finish()


@dp.message_handler(Text(equals=navBtns[2]))
@dp.message_handler(commands='currency')
async def currency(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add('❗️ALL❗️')
    massive = curShortMas
    markup.add(*massive)
    if lang == 'en':
        await message.reply('Choose currency you wanna to get', reply_markup=markup)
    elif lang == 'ru':
        await message.reply('Выберете валюту, которую хотите перевести', reply_markup=markup)
    else:
        await message.reply('Виберіть валюту, яку хочете перевести', reply_markup=markup)

@dp.message_handler(Text(equals=navBtns[3]))
@dp.message_handler(commands='update')
async def update(message: types.Message):
    make_currency()
    if lang == 'en':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[1] for i in navBtns])
        await message.answer('🟢<b>Data was successfully updated</b>🟢', parse_mode='html', reply_markup=markup)
    elif lang == 'ru':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[0] for i in navBtns])
        await message.answer('🟢<b>Данные успешно обновлены</b>🟢', parse_mode='html', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer('🟢<b>Дані успішно оновлені</b>🟢', parse_mode='html', reply_markup=markup)


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
        await message.answer(f'Курс {text}\n'
                             f'<b>{round(file[text], 4)}</b>\n\n'
                             f'Последнее обновление\n'
                             f'в <i>{file["update"]}</i>\n\n'
                             f'Используйте /update\n'
                             f'если хотите обновить дание',
                             parse_mode='html',
                             reply_markup=markup
                             )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer(f'Курс {text}\n'
                             f'<b>{round(file[text], 4)}</b>\n\n'
                             f'Останнє оновлення\n'
                             f'о <i>{file["update"]}</i>\n\n'
                             f'Використовуйте /update\n'
                             f'якщо ви хочете оновити дані',
                             parse_mode='html',
                             reply_markup=markup
                             )


@dp.message_handler(Text(equals='❗️ALL❗️'))
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
            f'Последнее обновление\n'
            f'в <i>{file["update"]}</i>\n\n'
            f'Используйте /update\n'
            f'если вы хотите обновить данные',
            parse_mode='html',
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add(*[i[2] for i in navBtns])
        await message.answer(
            f'<b>{result}</b>\n\n'
            f'Останнє оновлення\n'
            f'о <i>{file["update"]}</i>\n\n'
            f'Використовуйте /update\n'
            f'якщо ви хочете оновити дані',
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
        await message.reply("Выберите валюту", reply_markup=markup)
    else:
        await message.reply("Оберіть валюту", reply_markup=markup)


@dp.message_handler(lambda message: message.text.lower() not in [cur.lower() for cur in json.load(open('currency.json'))] and message.text not in curMass, state=Convert.currency1)
async def process_cur1_invalid(message: types.Message):
    """
    If cur1 is invalid
    """
    if lang == 'en':
        return await message.reply('Currency gotta be in format "usd"\n\nOr choose with buttons')
    elif lang == 'ru':
        return await message.reply('Валюта должна быть в формате "usd"\n\nИли выберите с помощью кнопок')
    else:
        return await message.reply('Валюта повинна бути в форматі "usd"\n\nАбо виберіть за допомогою')


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
        await message.reply("<b>Choose currency convert to🔄:</b>", parse_mode='html')
    elif lang == 'ru':
        await message.reply("<b>Выберете валюту в которую конвертировать🔄:</b>", parse_mode='html')
    else:
        await message.reply("<b>Оберіть валюту в яку конвертувати🔄:</b>", parse_mode='html')


# Check age. Age gotta be digit
@dp.message_handler(lambda message: message.text.lower() not in [cur.lower() for cur in json.load(open('currency.json'))] and message.text not in curMass, state=Convert.currency2)
async def process_cur2_invalid(message: types.Message):
    """
    If cur2 is invalid
    """
    if lang == 'en':
        return await message.reply('Currency gotta be inf format "usd"\n\nOr choose with buttons')
    elif lang == 'ru':
        return await message.reply('Валюта должна быть в формате "usd"\n\nИли выберите с помощью кнопок')
    else:
        return await message.reply('Валюта повинна бути в форматі "usd"\n\nАбо виберіть за допомогою')


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
        await message.reply("Какая сума?", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply("Яка сума?", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isdigit(), state=Convert.value)
async def process_value_invalid(message: types.Message):
    """
    In this example value has to be digit one.
    """
    if lang == 'en':
        return await message.reply("Value must be a number.")
    elif lang == 'ru':
        return await message.reply("Значение должно быть числом.")
    else:
        return await message.reply("Значення повинно бути числом.")


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
                f'💵💵💵💵💵\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'to\n'
                f'💵💵💵💵💵\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'EQUALS\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'💵💵💵💵💵\n\n'
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
                f'💵💵💵💵💵\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'в\n'
                f'💵💵💵💵💵\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'РАВНО\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'💵💵💵💵💵\n\n'
                f'Последнее обновление\n'
                f'в <i>{updated}</i>\n\n'
                f'Используйте /update\n'
                f'если вы хотите обновить данные к актуавльным',
                parse_mode='html',
                reply_markup=markup
            )
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add(*[i[2] for i in navBtns])
            await bot.send_message(
                message.chat.id,
                f'💵💵💵💵💵\n'
                f'<b>{data["cur1"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'у\n'
                f'💵💵💵💵💵\n'
                f'<b>{data["cur2"].upper()}</b>\n'
                f'💵💵💵💵💵\n'
                f'ДОРІВНЮЄ\n'
                f'<b>{result}</b>{curMassDict[data["cur2"].upper()]}\n'
                f'💵💵💵💵💵\n\n'
                f'Останнє оновлення\n'
                f'о <i>{updated}</i>\n\n'
                f'Використовуйте /update\n'
                f'якщо ви хочете оновити дані до актуальних',
                parse_mode='html',
                reply_markup=markup
            )

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)