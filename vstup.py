import telebot
from telebot import types

data = {}

bot = telebot.TeleBot('7453658638:AAHjsWgDuDLUz3lWuhuffxGhillL3Syinlg')

@bot.message_handler(commands=['start'])
def start(message):
    btn = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('ІНСТРУКЦІЯ', callback_data='instr')
    btn2 = types.InlineKeyboardButton('РОЗПОЧАТИ РОЗРАХУНОК', callback_data='start_count')
    btn.add(btn1)
    btn.add(btn2)
    bot.send_message(message.chat.id, f'\U0001F4EC Привіт, {message.from_user.first_name}! Цей бот допоможе тобі розрахувати твій конкурсний бал.', reply_markup=btn)

@bot.callback_query_handler(func=lambda call: call.data == 'instr')
def btn_function(call):
    instr_btn = types.InlineKeyboardMarkup()
    instr_btn1 = types.InlineKeyboardButton('ВАГОВІ КОЕФІЦІЄНТИ', url='https://osvita.ua/consultations/bachelor/10025/')
    instr_btn2 = types.InlineKeyboardButton('РОЗПОЧАТИ РОЗРАХУНОК', callback_data='start_count')
    instr_btn.add(instr_btn1)
    instr_btn.add(instr_btn2)
    bot.send_message(call.message.chat.id, '\U0001F4DA Перед початком роботи натисніть на кнопку "ВАГОВІ КОЕФІЦІЄНТИ" та перегляньте їх у тих предметів, які здавали, відповідно до спеціальності, яку обрали. Після цього натисніть на кнопку "РОЗПОЧАТИ РОЗРАХУНОК"', reply_markup=instr_btn)

@bot.callback_query_handler(func=lambda call: call.data == 'start_count')
def start_count(call):
    math_msg = bot.send_message(call.message.chat.id, '\U0001F587 Через пробіл одним повідомленням надішли мені бал НМТ з математики та його коефіцієнт (коефіцієнт у форматі "0.0", тобто дробове число записати через крапку).')
    bot.register_next_step_handler(math_msg, calculate_math)

def calculate_math(message):
    parts1 = message.text.split(' ')
    data['math_count'] = float(parts1[0])
    data['math_variable'] = float(parts1[1])
    math_btn = types.InlineKeyboardMarkup()
    math_btn.add(types.InlineKeyboardButton('БАЛ З ІСТОРІЇ', callback_data='history'))
    bot.send_message(message.chat.id, '\U0001F4DA Введені дані збережено. Натисніть наступну кнопку для продовження розрахунку.', reply_markup=math_btn)

@bot.callback_query_handler(func=lambda call: call.data == 'history')
def history_cal(call):
    history_msg = bot.send_message(call.message.chat.id, '\U0001F587 Через пробіл одним повідомленням надішли мені бал НМТ з історії та його коефіцієнт (коефіцієнт у форматі "0.0", тобто дробове число записати через крапку).')
    bot.register_next_step_handler(history_msg, calculate_history)

def calculate_history(message):
    parts2 = message.text.split()
    data['history_count'] = float(parts2[0])
    data['history_variable'] = float(parts2[1])
    history_btn = types.InlineKeyboardMarkup()
    history_btn.add(types.InlineKeyboardButton('БАЛ З УКРАЇНСЬКОЇ МОВИ', callback_data='ukrainian'))
    bot.send_message(message.chat.id, '\U0001F4DA Введені дані збережено. Натисніть наступну кнопку для продовження розрахунку.', reply_markup=history_btn)

@bot.callback_query_handler(func=lambda call: call.data == 'ukrainian')
def ukrainian(call):
    ukr_msg = bot.send_message(call.message.chat.id, '\U0001F587 Через пробіл одним повідомленням надішли мені бал НМТ з української та його коефіцієнт (коефіцієнт у форматі "0.0", тобто дробове число записати через крапку).')
    bot.register_next_step_handler(ukr_msg, calculate_ukrainian)

def calculate_ukrainian(message):
    parts3 = message.text.split()
    data['ukrainian_count'] = float(parts3[0])
    data['ukrainian_variable'] = float(parts3[1])
    ukr_btn = types.InlineKeyboardMarkup()
    ukr_btn.add(types.InlineKeyboardButton('БАЛ З 4 ПРЕДМЕТУ', callback_data='four'))
    bot.send_message(message.chat.id, '\U0001F4DA Введені дані збережено. Натисніть наступну кнопку для продовження розрахунку.', reply_markup=ukr_btn)

@bot.callback_query_handler(func=lambda call: call.data == 'four')
def history(call):
    four_msg = bot.send_message(call.message.chat.id, '\U0001F587 Через пробіл одним повідомленням надішли мені бал НМТ з четвертого предмету (на вибір) та його коефіцієнт (коефіцієнт у форматі "0.0", тобто дробове число записати через крапку).')
    bot.register_next_step_handler(four_msg, calculate_four)

def calculate_four(message):
    parts4 = message.text.split()
    data['four_count'] = float(parts4[0])
    data['four_variable'] = float(parts4[1])
    total_btn = types.InlineKeyboardMarkup()
    total_btn.add(types.InlineKeyboardButton('РЕЗУЛЬТАТ', callback_data='total'))
    bot.send_message(message.chat.id, '\U0001F4DA Введені дані збережено. Натисність на кнопку, щоб дізнатися результат.', reply_markup=total_btn)

@bot.callback_query_handler(func=lambda call: True)
def total(call):
    if call.data == 'total':
        count2 = float(data.get('history_count', 0))
        variable2 = float(data.get('history_variable', 1))
        count1 = float(data.get('math_count', 0))
        variable1 = float(data.get('math_variable', 1))
        count3 = float(data.get('ukrainian_count', 0))
        variable3 = float(data.get('ukrainian_variable', 1))
        count4 = float(data.get('four_count', 0))
        variable4 = float(data.get('four_variable', 1))
        sum_amount = variable1 + variable2 + variable3 + variable4
        sum_multi_amount = count1 * variable1 + count2*variable2 + count3 * variable3 + count4 * variable4
        calculate_amount1 = round(sum_multi_amount / sum_amount, 3)
        bot.send_message(call.message.chat.id, f'\U0001F4CD Розрахункове значення: {calculate_amount1}.\n\nЩоб порахувати знову використовуйте команду /start.')
bot.infinity_polling()