from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesAdmin, StatesAddUser
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID
from cfg.database import Database
from create_bot import dp, bot

db = Database('cfg/database')


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================
# ================= ДОБАВИТЬ АДМИНА =================
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID АДМИНА ===============
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# ===================================================
# ================= УДАЛИТЬ АДМИНА ==================
# ===================================================
async def del_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[2])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# ========== ВВОД ID АДМИНА ДЛЯ УДАЛЕНИЯ ==========
async def del_id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        try:
            ADMIN_ID.remove(new_users_id)
            await message.answer("Удалил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Такого пользователя нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[2])


# ===================================================
# ================ НОВЫЙ ПОЛЬЗОВАТЕЛЬ ===============
# ===================================================
async def add_new_user(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="Введи username нового пользователя", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAddUser.all()[0])

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД ID ПОЛЬЗОВАТЕЛЯ ===============
async def add_id_user_new(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer("Введи id нового пользователя", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.update_data(username=message.text)
        await state.set_state(StatesAddUser.all()[1])


# =============== ВВОД USERNAME ПОЛЬЗОВАТЕЛЯ  ===============
async def add_new_user_finish(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        try:
            bal = await state.get_data()
            db.add_user(int(message.text), bal["username"])
            await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Ошибка!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    else:
        await message.answer("Это не число!", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAddUser.all()[1])


# ===================================================
# ============== УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ ===============
# ===================================================
async def del_user(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="Введи id для удаления пользователя", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[8])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID ПОЛЬЗОВАТЕЛЯ ===============
async def id_del_user(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        try:
            db.del_user(message.text)
            await message.answer("Удалил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Ошибка!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[8])


# ===================================================
# =================== ДОБАВИТЬ АВТО =================
# ===================================================
async def add_new_car(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="Выбери подразделение:", reply_markup=BUTTON_TYPES["BTN_ADD_CAR"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[3])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД ПОДРАЗДЕЛЕНИЯ ===============
async def add_car_division(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text == "БайкалАренда Иркутск" or message.text == "БайкалАренда Улан-Удэ" or message.text == "БайкалАренда Ангарск":
        if message.text == "БайкалАренда Иркутск":
            await state.update_data(division="car_d1")
        elif message.text == "БайкалАренда Улан-Удэ":
            await state.update_data(division="car_d2")
        else:
            await state.update_data(division="car_d3")
        await bot.send_message(chat_id=message.from_user.id, text="Введи id пользователя для добавления авто:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[4])

    else:
        await message.answer("Такого подразделения нет\nПопробуй снова:", reply_markup=BUTTON_TYPES["BTN_ADD_CAR"])
        await state.set_state(StatesAdmin.all()[3])


# =============== ВВОД ID ПОЛЬЗОВАТЕЛЯ ===============
async def id_user_for_car(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        if db.there_is_user(message.text):
            await state.update_data(user_id_car=message.text)
            await bot.send_message(chat_id=message.from_user.id, text="Введи полное название авто(без запятых и точек):", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[5])
        else:
            await message.answer("Такого пользователя нет\nПопробуй снова ввести id пользователя которому добавить авто", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[4])
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[4])


# =============== ВВОД НАЗВАНИЕ АВТО ===============
async def add_name_car(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await state.update_data(name_car=message.text)
        await bot.send_message(chat_id=message.from_user.id, text="Отправь Excel файл с информацией об авто за МЕСЯЦ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
        await state.set_state(StatesAdmin.all()[7])


# =============== СКАЧИВАНИЕ ФАЙЛА №1 ===============
# async def file_1_for_car(message: Message, state: FSMContext):
#     name_car = await state.get_data()
#     await message.document.download(destination_file=f"all_file_excel/{name_car['name_car']} Неделя.xlsx")
#     await bot.send_message(chat_id=message.from_user.id, text="Отправь Excel файл с информацией об авто за МЕСЯЦ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
#     await state.set_state(StatesAdmin.all()[7])


# =============== ПРОВЕРКА ФАЙЛ ЭТО ИЛИ НЕТ №1 ===============
# async def no_file_1_for_car(message: Message, state: FSMContext):
#     if message.text.lower() == "отмена":
#         await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
#         await state.finish()
#     elif message.text == "Пропустить":
#         await bot.send_message(chat_id=message.from_user.id, text="Отправь Excel файл с информацией об авто за МЕСЯЦ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
#         await state.set_state(StatesAdmin.all()[7])
#     else:
#         await bot.send_message(chat_id=message.from_user.id, text="Это не Excel файл!!!\nОтправь Excel файл с информацией об авто за НЕДЕЛЮ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
#         await state.set_state(StatesAdmin.all()[6])


# =============== СКАЧИВАНИЕ ФАЙЛА №2 ===============
async def file_2_for_car(message: Message, state: FSMContext):
    name_car = await state.get_data()
    db.add_car_user(name_car["user_id_car"], name_car["division"], f'{name_car["name_car"]},')
    await message.document.download(destination_file=f"all_file_excel/{name_car['name_car']} Месяц.xlsx")
    await bot.send_message(chat_id=message.from_user.id, text="Всё добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    await state.finish()


# =============== ПРОВЕРКА ФАЙЛ ЭТО ИЛИ НЕТ №2 ===============
async def no_file_2_for_car(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    # elif message.text == "Пропустить":
    #     name_car = await state.get_data()
    #     db.add_car_user(name_car["user_id_car"], name_car["division"], f'{name_car["name_car"]},')
    #     await bot.send_message(chat_id=message.from_user.id, text="Всё добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    #     await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Это не Excel файл!!!\nОтправь Excel файл с информацией об авто за МЕСЯЦ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
        await state.set_state(StatesAdmin.all()[7])


# ===================================================
# ================== УДАЛИТЬ АВТО ===================
# ===================================================
async def del_car(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="Введи id пользователя для удаления у него авто", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAddUser.all()[2])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID ПОЛЬЗОВАТЕЛЯ ===============
async def id_del_car(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        try:
            all_car_name = []
            if db.select_all_car("car_d1", message.text)[0]:
                all_car_name += db.select_all_car("car_d1", message.text)[0].split(",")
            if db.select_all_car("car_d2", message.text)[0]:
                all_car_name += db.select_all_car("car_d2", message.text)[0].split(",")
            if db.select_all_car("car_d3", message.text)[0]:
                all_car_name += db.select_all_car("car_d3", message.text)[0].split(",")
            await state.update_data(id_user=message.text)
            await state.update_data(all_car=all_car_name)
            if all_car_name:
                text = "Все машины пользователя:\n\n"
                idx = 0
                for car in all_car_name:
                    if car:
                        text += f"{idx+1}. <code>{car}</code>\n"
                        idx += 1

                await message.answer(text + "\n\nОтправь название машины", reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode='HTML')
                await state.set_state(StatesAddUser.all()[3])
            else:
                await message.answer("У пользователя нет авто!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
                await state.finish()
        except:
            await message.answer("Такого пользователя нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAddUser.all()[2])


# =============== УДАЛЕНИЕ АВТО ===============
async def del_car_user(message: Message, state: FSMContext):
    all_data = await state.get_data()
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text in all_data["all_car"]:
        try:
            db.del_car_user(all_data["id_user"], message.text)
            await message.answer("Удалил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Ошибка!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()
    else:
        await message.answer("Такого авто нет!\nПопробуй снова:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAddUser.all()[3])


# ===================================================
# ============= ВЫВОД ВСЕХ ПОЛЬЗОВАТЕЛЕЙ ============
# ===================================================
async def views_users(message: Message):
    if message.from_user.id in ADMIN_ID:
        all_info_users = db.select_all()
        for idx, info_user in enumerate(all_info_users):
            text = f"""<b>{idx+1}. Информация о пользоватле:</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>user_id:</b> <code>{info_user[1]}</code>
<b>username:</b> <code>{info_user[2]}</code>\n
<b>Машины в Иркутске:</b>
{info_user[3]}\n
<b>Машины в Улан-Удэ:</b>
{info_user[4]}\n
<b>Машины в Ангарске:</b>
{info_user[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖"""

            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML')

    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"])


# =======================================================
# ================== ИЗМЕНЕНИЕ ТЕКСТА ===================
# =======================================================
async def edit_text(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="Выбери какой текст надо изменить:", reply_markup=BUTTON_TYPES["BTN_EDIT_TEXT"])

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


async def edit_text_call(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Выбери какой текст надо изменить:", reply_markup=BUTTON_TYPES["BTN_EDIT_TEXT"])
    await state.finish()


# ================== ВЫБРАЛИ ТЕКСТ ===================
async def edit_opr(callback: CallbackQuery):
    await callback.message.edit_text(text="Сейчас стоит такой текст:\n\n" + f'<code>{MESSAGES[f"{callback.data}"]}</code>', parse_mode="HTML")
    await callback.message.edit_reply_markup(BUTTON_TYPES["BTN_EDIT"])
    state = dp.current_state(user=callback.from_user.id)
    await state.update_data(ed_text=callback.data)
    await state.set_state(StatesAddUser.all()[4])


# ================== ВВОД НОВОГО ТЕКСТ ===================
async def input_new_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Вводи новый текст:", reply_markup=BUTTON_TYPES["BTN_MENU"])
    await state.set_state(StatesAddUser.all()[5])


# ================== СОХРАНЕНИЕ НОВОГО ТЕКСТ ===================
async def save_new_text(message: Message, state: FSMContext):
    all_data = await state.get_data()
    MESSAGES[f"{all_data['ed_text']}"] = message.text
    await message.answer(text="Новый текст добавлен!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    await state.finish()


# ===================================================
# ============ ОБНОВЛЕНИЕ ДАННЫХ О МАШИНЕ ===========
# ===================================================
async def update_car(message: Message):
    if message.from_user.id in ADMIN_ID:
        all_info_users = db.select_all()
        for idx, info_user in enumerate(all_info_users):
            text = f"""<b>{idx+1}. Информация о пользоватле:</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>user_id:</b> <code>{info_user[1]}</code>
<b>username:</b> <code>{info_user[2]}</code>\n
<b>Машины в Иркутске:</b>
"""
            try:
                a = info_user[3].split(",")
                for i in a:
                    text += f"<code>{i}</code>, "
            except:
                ...
            try:
                text += "\n\n<b>Машины в Улан-Удэ</b>\n"
                a = info_user[4].split(",")
                for i in a:
                    text += f"<code>{i}</code>, "
            except:
                ...

            try:
                text += "\n\n<b>Машины в Ангарске:</b>\n"
                a = info_user[5].split(",")
                for i in a:
                    text += f"<code>{i}</code>, "
            except:
                ...
            text += "\n➖➖➖➖➖➖➖➖➖➖➖➖➖"

            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML')

        await bot.send_message(chat_id=message.from_user.id, text="Введи полное название машины для обновления данных", parse_mode='HTML', reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAddUser.all()[6])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"])


# ============ ОБНОВЛЕНИЕ ДАННЫХ О МАШИНЕ ===========
async def update_file(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(f"Отправьте новый файл Excel для {message.text}", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.update_data(name_car=message.text)
        await state.set_state(StatesAddUser.all()[7])


# =============== СКАЧИВАНИЕ ФАЙЛА №2 ===============
async def file_2_update(message: Message, state: FSMContext):
    name_car = await state.get_data()
    await message.document.download(destination_file=f"all_file_excel/{name_car['name_car']} Месяц.xlsx")
    await bot.send_message(chat_id=message.from_user.id, text="Всё добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    await state.finish()


# =============== ПРОВЕРКА ФАЙЛ ЭТО ИЛИ НЕТ №2 ===============
async def no_file_2_update(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Это не Excel файл!!!\nОтправь Excel файл с информацией об авто за МЕСЯЦ", reply_markup=BUTTON_TYPES["BTN_SKIP"])
        await state.set_state(StatesAddUser.all()[7])


def register_handler_admin(dp: Dispatcher):
    # ДОБАВЛЕНИЕ АДМИНА
    dp.register_message_handler(add_admin, lambda message: message.text.lower() == 'добавить админа')
    dp.register_message_handler(id_admin, state=StatesAdmin.STATES_1)

    # УДАЛЕНИЕ АДМИНА
    dp.register_message_handler(del_admin, lambda message: message.text.lower() == 'удалить админа')
    dp.register_message_handler(del_id_admin, state=StatesAdmin.STATES_2)

    # ДОБАВЛЕНИЕ АВТО
    dp.register_message_handler(add_new_car, lambda message: message.text.lower() == 'добавить авто')
    dp.register_message_handler(add_car_division, state=StatesAdmin.STATES_3)
    dp.register_message_handler(id_user_for_car, state=StatesAdmin.STATES_4)
    dp.register_message_handler(add_name_car, state=StatesAdmin.STATES_5)

    # dp.register_message_handler(file_1_for_car, state=StatesAdmin.STATES_6, content_types=["document"])
    # dp.register_message_handler(no_file_1_for_car, state=StatesAdmin.STATES_6)

    dp.register_message_handler(file_2_for_car, state=StatesAdmin.STATES_7, content_types=["document"])
    dp.register_message_handler(no_file_2_for_car, state=StatesAdmin.STATES_7)

    # УДАЛЕНИЕ АВТО
    dp.register_message_handler(del_car, lambda message: message.text.lower() == 'удалить авто')
    dp.register_message_handler(id_del_car, state=StatesAddUser.STAT_2)
    dp.register_message_handler(del_car_user, state=StatesAddUser.STAT_3)

    # ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    dp.register_message_handler(add_new_user, lambda message: message.text.lower() == 'добавить пользователя')
    dp.register_message_handler(add_id_user_new, state=StatesAddUser.STAT_0)
    dp.register_message_handler(add_new_user_finish, state=StatesAddUser.STAT_1)

    # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    dp.register_message_handler(del_user, lambda message: message.text.lower() == 'удалить пользователя')
    dp.register_message_handler(id_del_user, state=StatesAdmin.STATES_8)

    # ВЫВОД ВСЕХ ПОЛЬЗОВАТЕЛЯ
    dp.register_message_handler(views_users, lambda message: message.text.lower() == 'все пользователи')

    # ИЗМЕНЕНИЕ ТЕКСТА
    dp.register_message_handler(edit_text, lambda message: message.text.lower() == 'изменить текст')
    dp.register_callback_query_handler(edit_text_call, lambda callback: callback.data == "menu", state=StatesAddUser.STAT_4)
    dp.register_callback_query_handler(edit_text_call, lambda callback: callback.data == "menu", state=StatesAddUser.STAT_5)

    dp.register_callback_query_handler(edit_opr, lambda callback: callback.data == "start" or callback.data == "car" or callback.data == "no_car" or callback.data == "period"
                                       or callback.data == "no_period" or callback.data == "send_file" or callback.data == "not_command")
    dp.register_callback_query_handler(input_new_text, lambda callback: callback.data == "red", state=StatesAddUser.STAT_4)
    dp.register_message_handler(save_new_text, state=StatesAddUser.STAT_5)

    # ОБНОВИТЬ ДАННЫЕ
    dp.register_message_handler(update_car, lambda message: message.text.lower() == 'обновить авто')
    dp.register_message_handler(update_file, state=StatesAddUser.STAT_6)
    dp.register_message_handler(file_2_update, state=StatesAddUser.STAT_7, content_types=["document"])
    dp.register_message_handler(no_file_2_update, state=StatesAddUser.STAT_7)

