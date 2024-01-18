from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# ================= КНОПКИ ПОЛЬЗОВАТЕЛЯ =================

# ПОДРАЗДЕЛЕНИЯ
btn_divisions_1 = KeyboardButton("БайкалАренда Иркутск")
btn_divisions_2 = KeyboardButton("БайкалАренда Улан-Удэ")
btn_divisions_3 = KeyboardButton("БайкалАренда Ангарск")
btn_divisions_all = KeyboardButton("Все подразделения")

# АВТОМОБИЛИ
btn_car_all = KeyboardButton("Все автомобили")

# ПЕРИОД
btn_all = KeyboardButton("Всё время")
btn_week = KeyboardButton("Неделя")
btn_month = KeyboardButton("Месяц")


# ================= КНОПКИ АДМИНА =================
btn_add_user = KeyboardButton("Добавить пользователя")
btn_del_user = KeyboardButton("Удалить пользователя")

btn_add_car = KeyboardButton("Добавить авто")
btn_del_car = KeyboardButton("Удалить авто")
btn_update_car = KeyboardButton("Обновить авто")

btn_add_admin = KeyboardButton("Добавить админа")
btn_del_admin = KeyboardButton("Удалить админа")

btn_view_users = KeyboardButton("Все пользователи")

btn_edit_text = KeyboardButton("Изменить текст")

btn_edit_start = InlineKeyboardButton(text="Приветствие", callback_data="start")
btn_edit_car = InlineKeyboardButton(text="Выбор Авто", callback_data="car")
btn_edit_no_car = InlineKeyboardButton(text="Если нет авто", callback_data="no_car")
btn_edit_period = InlineKeyboardButton(text="Период", callback_data="period")
btn_edit_no_period = InlineKeyboardButton(text="Нет такого Периода", callback_data="no_period")
btn_edit_send_file = InlineKeyboardButton(text="Отправка файлов", callback_data="send_file")
btn_edit_not_command = InlineKeyboardButton(text="Такой команды нет", callback_data="not_command")

btn_edit_opr_text = InlineKeyboardButton(text="Редактировать 📝", callback_data="red")
btn_edit_menu = InlineKeyboardButton(text="Меню", callback_data="menu")

# ================= ОБЩИЕ =================
btn_skip = KeyboardButton("Пропустить")
btn_cancel = KeyboardButton("Отмена")
btn_back = KeyboardButton("Меню")


BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_divisions_1, btn_divisions_2, btn_divisions_3).add(btn_divisions_all),
    "BTN_CAR": ReplyKeyboardMarkup(resize_keyboard=True),
    "BTN_PERIOD": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_week, btn_month, btn_all).add(btn_back),

    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_user, btn_del_user).add(btn_add_car, btn_del_car, btn_update_car).add(btn_add_admin, btn_del_admin).add(btn_view_users).add(btn_edit_text),
    "BTN_ADD_CAR": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_divisions_1, btn_divisions_2, btn_divisions_3).add(btn_cancel),
    "BTN_EDIT_TEXT": InlineKeyboardMarkup().add(btn_edit_start).add(btn_edit_car, btn_edit_no_car).add(btn_edit_period, btn_edit_no_period).add(btn_edit_send_file).add(btn_edit_not_command),
    "BTN_EDIT": InlineKeyboardMarkup().add(btn_edit_opr_text).add(btn_edit_menu),
    "BTN_MENU": InlineKeyboardMarkup().add(btn_edit_menu),

    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
    "BTN_SKIP": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
}
