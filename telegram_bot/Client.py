import asyncio
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesUsers
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID
from cfg.database import Database
from create_bot import dp, bot

db = Database('cfg/database')


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
async def start_command(message: Message):
    if message.from_user.id in [i[0] for i in db.select_all_user_id()] or message.from_user.id in ADMIN_ID:
        await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
    else:
        await bot.send_message(text=MESSAGES["no_start"], chat_id=message.from_user.id)


# ===================================================
# =================== АВТОМОБИЛИ ====================
# ===================================================
async def car_in_divisions(message: Message):
    if message.text.lower() == "байкаларенда иркутск":
        table_db = "car_d1"
    elif message.text.lower() == "байкаларенда улан-удэ":
        table_db = "car_d2"
    else:
        table_db = "car_d3"

    if message.from_user.id in [i[0] for i in db.select_all_user_id()] or message.from_user.id in ADMIN_ID:
        all_car_name = db.select_all_car(table_db, message.from_user.id)[0]
        if all_car_name:
            all_car_name = all_car_name.split(",")
            btn_car = ReplyKeyboardMarkup(resize_keyboard=True)
            for car in all_car_name:
                btn_car.add(KeyboardButton(f"{car}"))
            if len(all_car_name) > 2:
                btn_car.add(KeyboardButton("Все автомобили")).add(KeyboardButton("Меню"))
            else:
                btn_car.add(KeyboardButton("Меню"))
            await bot.send_message(text=MESSAGES['car'], reply_markup=btn_car, chat_id=message.from_user.id)

            state = dp.current_state(user=message.from_user.id)
            await state.update_data(all_car_name_save=all_car_name)
            await state.set_state(StatesUsers.all()[1])
        else:
            await bot.send_message(text=MESSAGES['no_car'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
    else:
        await bot.send_message(text=MESSAGES["no_start"], chat_id=message.from_user.id)


# ============== ПЕРИОД В ПОДРАЗДЕЛЕНИИ =============
# async def period_opr_car(message: Message, state: FSMContext):
#     table_db = await state.get_data()
#     if message.text.lower() == "меню":
#         await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
#         await state.finish()
#
#     elif message.text in table_db["all_car_name_save"] or message.text == "Все автомобили":
#         await bot.send_message(text=MESSAGES["period"], reply_markup=BUTTON_TYPES["BTN_PERIOD"], chat_id=message.from_user.id)
#         await state.update_data(car_name=message.text)
#         await state.set_state(StatesUsers.all()[1])
#     else:
#         await bot.send_message(text=MESSAGES["no_period"], chat_id=message.from_user.id)
#         await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
#         await state.finish()


# ================== ОТПРАВКА ФАЙЛОВ ================
async def send_file_excel(message: Message, state: FSMContext):
    await state.update_data(car_name=message.text)
    table_db = await state.get_data()
    if message.text.lower() == "меню":
        await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
        await state.finish()

    elif message.text in table_db["all_car_name_save"] or message.text == "Все автомобили":
        await bot.send_message(text=MESSAGES['send_file'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
        all_data = await state.get_data()
        print(all_data["car_name"])
        if all_data["car_name"] == "Все автомобили":
            for file_name in all_data["all_car_name_save"]:
                if file_name != '':
                    try:
                        file_name += f" Месяц"
                        print(file_name)
                        with open(f"all_file_excel/{file_name}.xlsx", "rb") as file_ex:
                            await bot.send_document(chat_id=message.from_user.id, document=file_ex)
                    except:
                        await bot.send_message(text=MESSAGES["error_send"] + f"{file_name}", chat_id=message.from_user.id)

        else:
            try:
                file_name = all_data["car_name"] + f" Месяц"
                with open(f"all_file_excel/{file_name}.xlsx", "rb") as file_ex:
                    await bot.send_document(chat_id=message.from_user.id, document=file_ex)
            except:
                await bot.send_message(text=MESSAGES["error_send"] + f"{all_data['car_name']}", chat_id=message.from_user.id)
        await state.finish()

    else:
        await bot.send_message(text=MESSAGES["no_send"], chat_id=message.from_user.id)
        await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
        await state.finish()


# ===================================================
# ============ ВСЕ МАШИНЫ ВЫБОР ПЕРИОДА =============
# ===================================================
async def send_all_car_period(message: Message, state: FSMContext):
    if message.from_user.id in [i[0] for i in db.select_all_user_id()] or message.from_user.id in ADMIN_ID:
        all_car_name_d1 = db.select_all_car("car_d1", message.from_user.id)[0]
        all_car_name_d2 = db.select_all_car("car_d2", message.from_user.id)[0]
        all_car_name_d3 = db.select_all_car("car_d3", message.from_user.id)[0]
        if all_car_name_d1 or all_car_name_d2 or all_car_name_d3:
            all_car_name = []
            if db.select_all_car("car_d1", message.from_user.id)[0]:
                all_car_name += db.select_all_car("car_d1", message.from_user.id)[0].split(",")
            if db.select_all_car("car_d2", message.from_user.id)[0]:
                all_car_name += db.select_all_car("car_d2", message.from_user.id)[0].split(",")
            if db.select_all_car("car_d3", message.from_user.id)[0]:
                all_car_name += db.select_all_car("car_d3", message.from_user.id)[0].split(",")

            if all_car_name:
                for file_name in all_car_name:
                    if file_name != '':
                        file_name += f" Месяц"
                        try:
                            with open(f"all_file_excel/{file_name}.xlsx", "rb") as file_ex:
                                await bot.send_document(chat_id=message.from_user.id, document=file_ex)
                        except:
                            await bot.send_message(text=MESSAGES["error_send"] + f"{file_name}",
                                                   chat_id=message.from_user.id)
            else:
                await bot.send_message(text=MESSAGES["error_send"], chat_id=message.from_user.id)
        else:
            await bot.send_message(text=MESSAGES['no_car'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)

    else:
        await bot.send_message(text=MESSAGES["no_start"], chat_id=message.from_user.id)


# ============== ОТПРАВКА ВСЕХ МАШИН ================
# async def send_all_car(message: Message, state: FSMContext):
#     if message.text.lower() == "меню":
#         await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
#         await state.finish()
#
#     elif message.text == "Неделя" or message.text == "Месяц":
#         await bot.send_message(text=MESSAGES['send_file'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
#         all_car_name = []
#         if db.select_all_car("car_d1", message.from_user.id)[0]:
#             all_car_name += db.select_all_car("car_d1", message.from_user.id)[0].split(",")
#         if db.select_all_car("car_d2", message.from_user.id)[0]:
#             all_car_name += db.select_all_car("car_d2", message.from_user.id)[0].split(",")
#         if db.select_all_car("car_d3", message.from_user.id)[0]:
#             all_car_name += db.select_all_car("car_d3", message.from_user.id)[0].split(",")
#
#         if all_car_name:
#             for file_name in all_car_name:
#                 if file_name != '':
#                     file_name += f" {message.text}"
#                     try:
#                         with open(f"all_file_excel/{file_name}.xlsx", "rb") as file_ex:
#                             await bot.send_document(chat_id=message.from_user.id, document=file_ex)
#                     except:
#                         await bot.send_message(text=MESSAGES["error_send"] + f"{file_name}", chat_id=message.from_user.id)
#         else:
#             await bot.send_message(text=MESSAGES["error_send"], chat_id=message.from_user.id)
#         await state.finish()
#
#     else:
#         await bot.send_message(text=MESSAGES["no_send"], chat_id=message.from_user.id)
#         await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)
#         await state.finish()


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
async def unknown_command(message: Message):
    if message.from_user.id in [i[0] for i in db.select_all_user_id()] or message.from_user.id in ADMIN_ID:
        if message.from_user.id in ADMIN_ID:
            await bot.send_message(text=MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"], chat_id=message.from_user.id)
        else:
            await bot.send_message(text=MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)

    else:
        await bot.send_message(text=MESSAGES["no_start"], chat_id=message.from_user.id)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(start_command, lambda message: message.text.lower() == 'меню')

    dp.register_message_handler(car_in_divisions, lambda message: message.text.lower() == 'байкаларенда иркутск' or message.text.lower() == 'байкаларенда улан-удэ' or message.text.lower() == 'байкаларенда ангарск')
    # dp.register_message_handler(period_opr_car, state=StatesUsers.STATE_0)
    dp.register_message_handler(send_file_excel, state=StatesUsers.STATE_1)

    dp.register_message_handler(send_all_car_period, lambda message: message.text.lower() == 'все подразделения')
    # dp.register_message_handler(send_all_car, state=StatesUsers.STATE_2)

    dp.register_message_handler(unknown_command, content_types=["text"])

