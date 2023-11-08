from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
start_message = """Привет 👋 
На связи бот БайкалАренды, выбери подразделение:"""
no_start_message = """Привет 👋 
К сожалению бот тебе не доступен"""
start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет\nПиши /start"

add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""


car_message = "Выбери автомобиль:"
no_car_message = "В этом подразделение у вас нет авто!"

period_message = "Выбери период:"
no_period_message = "Такой машины нет"

no_send_message = "Такого периода нет"

error_send_message = "Машина была не найдена\n\n"
send_file_message = "Отправка файлов началась!"

MESSAGES = {
    "start": start_message,
    "no_start": no_start_message,
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,


    "car": car_message,
    "no_car": no_car_message,

    "period": period_message,
    "no_period": no_period_message,
    "no_send": no_send_message,

    "error_send": error_send_message,
    "send_file": send_file_message,
}
