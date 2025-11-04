import telebot
import webbrowser
import threading
import time
import random
from datetime import datetime, time as dt_time
from telebot import types

a=[103,104,105,106,107,108]
b=[101,102]
c=[109,110,111,113,115,116]
d=[217,218,201,202]
e=[203,204,205,206,207,208]
f=[209,210,211,212,213,214,215,216]
j=[301,302,311]
k=[303,304,305,306,307]
g=[403,404,405]
h=[406,407]

# Список для хранения ID чатов для рассылки
subscribed_chats = set()

bot = telebot.TeleBot('8356625468:AAE11_QhXsQ2rwwzGbnSUdwToPJ8W-hUTpo')

# Обновленные сообщения о запрете курения
smoking_messages = [
    "🚭 ЖЕСТКИЙ ЗАПРЕТ КУРЕНИЯ!\n\n"
    "📍 Курение ЗАПРЕЩЕНО:\n"
    "• На всей территории колледжа\n"
    "• Возле здания колледжа\n"
    "• Рядом с прокуратурой\n"
    "• В радиусе 50 метров от входа\n\n"
    "⚖️ Нарушители привлекаются к ответственности!",
    
    "🚭 ВНИМАНИЕ: Абсолютный запрет курения!\n\n"
    "❌ Запрещено везде:\n"
    "• В помещениях и на территории ФЭК\n"
    "• У входа и вокруг колледжа\n"
    "• Возле здания прокуратуры\n"
    "• На прилегающих тротуарах\n\n"
    "💚 ФЭК - территория без табачного дыма!",
    
    "🚭 ЗАПРЕТ КУРЕНИЯ 100%\n\n"
    "📍 НЕТ разрешённых мест для курения!\n"
    "• Не на территории колледжа\n"
    "• Не рядом с колледжем\n"
    "• Не возле прокуратуры\n"
    "• Не на окружающих улицах\n\n"
    "🌿 Дышите чистым воздухом!",
    
    "🚭 АДМИНИСТРАТИВНОЕ ПРЕДУПРЕЖДЕНИЕ\n\n"
    "Курение ЗАПРЕЩЕНО на всей территории:\n"
    "• ФЭК РГЭУ(РИНХ) и прилегающая зона\n"
    "• Подходы к колледжу\n"
    "• Зона возле прокуратуры\n\n"
    "📞 Сообщите о нарушителях администрации",
    
    "💨 ПОЛНЫЙ ЗАПРЕТ КУРЕНИЯ!\n\n"
    "🚭 НЕТ курению:\n"
    "• В колледже ❌\n"
    "• Рядом с колледжем ❌\n"
    "• У прокуратуры ❌\n"
    "• На окружающей территории ❌\n\n"
    "💪 Выбираем здоровье без компромиссов!",
    
    "🚭 ТЕРРИТОРИЯ БЕЗ ТАБАКА!\n\n"
    "📍 Абсолютный запрет курения:\n"
    "• Весь кампус ФЭК\n"
    "• Прилегающие территории\n"
    "• Зона прокуратуры\n"
    "• Все подходы к зданию\n\n"
    "⚖️ Нарушение = дисциплинарная ответственность",
    
    "🌱 ФЭК - ЗОНА СВОБОДНАЯ ОТ КУРЕНИЯ!\n\n"
    "🚭 Запрещено полностью:\n"
    "• На территории колледжа\n"
    "• В радиусе 50м от входа\n"
    "• Возле прокуратуры\n"
    "• На всех прилегающих площадях\n\n"
    "💚 Создаём здоровую среду для всех!"
]

# Функция для автоматической рассылки в случайное время
def smoking_ban_broadcast():
    """Рассылка 2-3 раза в день в случайное время"""
    sent_times_today = []
    
    while True:
        try:
            now = datetime.now()
            current_date = now.date()
            
            # Очищаем список отправок если наступил новый день
            if not sent_times_today or sent_times_today[0].date() != current_date:
                sent_times_today = []
                # Генерируем 2-3 случайных времени на сегодня
                today_times = []
                num_messages = random.randint(2, 3)  # 2 или 3 сообщения в день
                
                for _ in range(num_messages):
                    hour = random.randint(8, 20)  # с 8 утра до 20 вечера
                    minute = random.randint(0, 59)
                    today_times.append((hour, minute))
                
                # Сортируем по времени
                today_times.sort()
            
            # Проверяем, настало ли одно из случайных времен
            current_time = (now.hour, now.minute)
            if current_time in today_times and current_time not in sent_times_today:
                # Выбираем случайное сообщение
                message = random.choice(smoking_messages)
                message += f"\n\n📅 Напоминание от: {now.strftime('%H:%M')}"
                
                # Отправляем сообщение
                sent_count = 0
                for chat_id in list(subscribed_chats):
                    try:
                        bot.send_message(chat_id, message)
                        sent_count += 1
                    except Exception as e:
                        print(f"Ошибка отправки в чат {chat_id}: {e}")
                        subscribed_chats.discard(chat_id)
                
                print(f"✅ Рассылка отправлена в {sent_count} чатов в {now.strftime('%H:%M')}")
                sent_times_today.append(current_time)
                
                # Ждем чтобы не отправить повторно в ту же минуту
                time.sleep(61)
            else:
                # Проверяем каждую минуту
                time.sleep(60)
                
        except Exception as e:
            print(f"Ошибка в рассылке: {e}")
            time.sleep(60)

# Запускаем рассылку в отдельном потоке
broadcast_thread = threading.Thread(target=smoking_ban_broadcast, daemon=True)
broadcast_thread.start()

@bot.message_handler(commands=['start'])
def start(message):
    # Добавляем чат в список рассылки
    subscribed_chats.add(message.chat.id)
    
    markup = types.ReplyKeyboardMarkup()
    
    btn1 = types.KeyboardButton('Найти кабинет')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn2)
    btn3 = types.KeyboardButton('что рядом?')
    btn4 = types.KeyboardButton('🚽')
    markup.row(btn3,btn4)
    btn5 = types.KeyboardButton('Приёмная и каб. зам. директоров')
    markup.row(btn5)
    
    welcome_msg = "Добро пожаловать в навигатор по ФЭК РГЭУ(РИНХ)!!!\n\n"
    welcome_msg += "🚭 Курение ЗАПРЕЩЕНО везде: в колледже, рядом с колледжем и возле прокуратуры\n"
    
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

@bot.message_handler(commands=['smoking_info'])
def smoking_info_command(message):
    show_smoking_info(message)

def show_smoking_info(message):
    smoking_text = """
🚭 ПОЛНЫЙ ЗАПРЕТ КУРЕНИЯ НА ВСЕЙ ТЕРРИТОРИИ!

📍 Где ЗАПРЕЩЕНО курение (100% запрет):
• Все помещения ФЭК (аудитории, коридоры, санузлы)
• Вся территория колледжа (двор, входы, площадки)
• Возле здания колледжа (радиус 50 метров)
• Рядом с прокуратурой и прилегающие территории
• Все тротуары и подходы к зданию

⚖️ Ответственность за нарушение:
• Немедленное замечание от дежурного преподавателя
• Дисциплинарное взыскание от администрации
• Вызов к заместителю директора
• Уведомление в деканат и учебную часть

💡 Важно:
• НЕТ специально отведённых мест для курения
• Запрет действует 24/7 на всей территории
• Относится к студентам, преподавателям и посетителям

💚 ФЭК - территория здоровья без табачного дыма!

📅 Напоминания приходят 2-3 раза в день в случайное время
    """
    bot.send_message(message.chat.id, smoking_text)



@bot.message_handler(content_types=['text'])
def on_click(message):
    if message.text == '🚽':
        toilet_info = """
🚽 ТУАЛЕТЫ ФЭК

📍 1 ЭТАЖ:
• Левое крыло: 3 дверь - женский, 4 дверь - мужской

📍 2 ЭТАЖ:
• Левое крыло: 3 дверь - женский, 4 дверь - мужской  

📍 3 ЭТАЖ:
• Левое крыло: 3 дверь - женский, 4 дверь - мужской

🚭 Курение в туалетах ЗАПРЕЩЕНО!
        """
        bot.send_message(message.chat.id, toilet_info)
    
    elif message.text == 'Найти кабинет':
        msg = bot.send_message(message.chat.id, 'Введите номер кабинета: ')
        bot.register_next_step_handler(msg, process_cabinet_number)
    
    elif message.text == 'Перейти на сайт':
        website_url = "https://rsue.ru/rfec/"
        markup = types.InlineKeyboardMarkup()
        btn_website = types.InlineKeyboardButton("🌐 Открыть сайт ФЭК", url=website_url)
        markup.add(btn_website)

        bot.send_message(
            message.chat.id, 
            "Нажмите на кнопку ниже чтобы открыть сайт ФЭК:", 
            reply_markup=markup
        )
        
    elif message.text == 'что рядом?':
        show_nearby_places(message)
    
    elif message.text == 'Приёмная и каб. зам. директоров':
        bot.send_message(message.chat.id, 'Приёмная: 1 этаж, правое крыло, справа 6 дверь\nКабинеты заместителей директоров: 1 этаж, правое крыло, справа с 1 по 5')
    

def show_nearby_places(message):
    """Показывает места рядом с колледжем"""
    nearby_text = """
🏫 ЧТО РЯДОМ С ФЭК:

📍 Справа от колледжа (~100м):
🛒 Продуктовый магазин "Пятерочка"
- Хлеб, молоко, продукты
- Бутерброды, напитки
- Канцелярия

📍 Слева от колледжа (~100м):
🛒 Продуктовый магазин "Магнит" 
- Полуфабрикаты, выпечка
- Кофе, снеки
- Хозтовары

📍 В 200м от колледжа:
💊 Аптека "АптекаПлюс"
- Лекарства по рецепту
- Медицинские изделия
- Витамины, БАДы
    """
    
    # Создаем инлайн-кнопки для навигации
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_food = types.InlineKeyboardButton("🛒 Продукты", callback_data="nearby_food")
    btn_pharmacy = types.InlineKeyboardButton("💊 Аптека", callback_data="nearby_pharmacy") 
    
    markup.add(btn_food, btn_pharmacy)
    
    bot.send_message(message.chat.id, nearby_text, reply_markup=markup)

# Обработчик для инлайн-кнопок "что рядом?"
@bot.callback_query_handler(func=lambda call: call.data.startswith('nearby_'))
def handle_nearby_buttons(call):
    if call.data == 'nearby_food':
        response = """
🛒 ПРОДУКТОВЫЕ МАГАЗИНЫ:

📍 Справа (~100м):
• "Пятерочка" - ул. Примерная, 15
⏰ 6:00-22:00

📍 Слева (~100м):  
• "Магнит" -Гвардейский переулок, 2/1
⏰ 8:00-21:00
        """
        
    elif call.data == 'nearby_pharmacy':
        response = """
💊 АПТЕКА "АптекаПлюс":

📍 200м от колледжа
🏠 Гвардейский переулок, 2/1

💊 Что есть:
• Лекарства по рецепту и без
• Медицинские изделия
• Витамины и БАДы
• Косметика для ухода
        """
        
    
    # Редактируем сообщение вместо отправки нового
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id, 
        text=response,
        reply_markup=call.message.reply_markup  # Сохраняем кнопки
    )
    
    # Подтверждаем обработку callback
    bot.answer_callback_query(call.id)


def process_cabinet_number(message):
    try:
        namber = int(message.text)
        
           # Определяем этаж по номеру кабинета
        floor = namber // 100  # 101 -> 1, 201 -> 2, etc.
        
        # Словарь с file_id для каждого этажа (ЗАМЕНИТЕ НА ВАШИ РЕАЛЬНЫЕ file_id)
        floor_photos = {
            1: 'AgACAgIAAxkBAAIBlmkKPlMoHiMrAwi-60HagqkVkrV4AAK2Emsbj0xQSIkAARjZS1t3wAEAAwIAA3kAAzYE',  # Замените на реальный file_id
            2: 'AgACAgIAAxkBAAIBmWkKPot_aFhI39mu2YvrCJVpdbXLAAK6Emsbj0xQSIRFBR2LQPj9AQADAgADeQADNgQ',  # Замените на реальный file_id
            3: 'AgACAgIAAxkBAAIBnGkKPshOn6Pc6lRVjfbmAAFtzA9BpAACvBJrG49MUEh5Jiv1954_7wEAAwIAA3kAAzYE',  # Замените на реальный file_id
            4: 'AgACAgIAAxkBAAIBn2kKPupGKAgsaOYBqik_jK3dJP6NAAK9Emsbj0xQSE5OF3LHhbMZAQADAgADeQADNgQ',  # Замените на реальный file_id
        }
        
        # Отправляем фото этажа
        if floor in floor_photos:
            try:
                bot.send_photo(message.chat.id, floor_photos[floor])
                print(f"✅ Отправлено фото {floor} этажа")
            except Exception as e:
                print(f"❌ Ошибка отправки фото: {e}")
                bot.send_message(message.chat.id, f"🏢 {floor} этаж - схема временно недоступна")
        else:
            bot.send_message(message.chat.id, f"🏢 {floor} этаж - схема не найдена")
            
            
        if namber == 101:
            bot.send_message(message.chat.id, '1 этаж, в центре, слева 1 дверь!!!')
        elif namber == 102:
            bot.send_message(message.chat.id, '1 этаж, в центре, слева 2 дверь!!!')
        elif namber == 103:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, слева 1 дверь!!!')
        elif namber == 104:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, слева 2 дверь!!!')
        elif namber == 105:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, слева 3 дверь!!!')
        elif namber == 106:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, слева 4 дверь!!!')
        elif namber == 107:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, справа 2 дверь!!!')
        elif namber == 108:
            bot.send_message(message.chat.id, '1 этаж, левое крыло, справа 1 дверь!!!')
        elif namber == 109:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, слева зайдите в 1 дверь, дверь слева!!!')
        elif namber == 110:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, слева зайдите в 1 дверь, дверь прямо!!!')
        elif namber == 111:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, слева зайдите в 1 дверь, дверь справа!!!')
        elif namber == 113:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, справа 6 дверь!!!')
        elif namber == 115:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, справа 5 дверь!!!')
        elif namber == 116:
            bot.send_message(message.chat.id, '1 этаж, правое крыло, справа 4 дверь!!!')
        elif namber == 201:
            bot.send_message(message.chat.id, '2 этаж, в центре,слева 1 дверь !!!')
        elif namber == 202:
            bot.send_message(message.chat.id, '2 этаж, в центре, слева 2 дверь!!!')
        elif namber == 203:
            bot.send_message(message.chat.id, '2 этаж, левое крыло, слева 1 дверь!!!')
        elif namber == 204:
            bot.send_message(message.chat.id, '2 этаж, левое крыло,слева 2 дверь!!!')
        elif namber == 205:
            bot.send_message(message.chat.id, '2 этаж, левое крыло, слева 3 дверь!!!')
        elif namber == 206:
            bot.send_message(message.chat.id, '2 этаж, левое крыло, слева 4 дверь!!!')
        elif namber == 207:
            bot.send_message(message.chat.id, '2 этаж, левое крыло, справа 2 дверь!!!')
        elif namber == 208:
            bot.send_message(message.chat.id, '2 этаж, левое крыло,справа 1 дверь!!!')
        elif namber == 209:
            bot.send_message(message.chat.id, '2 этаж, правое крыло,слева 1 дверь!!!')
        elif namber == 210:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, слева 2 дверь!!!')
        elif namber == 211:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, слева 3 дверь!!!')
        elif namber == 212:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, слева 4 дверь!!!')
        elif namber == 213:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, справа 4 дверь!!!')
        elif namber == 214:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, справа 3 дверь!!!')
        elif namber == 215:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, справа 2 дверь!!!')
        elif namber == 216:
            bot.send_message(message.chat.id, '2 этаж, правое крыло, справа 1 дверь!!!')
        elif namber == 217:
            bot.send_message(message.chat.id, '2 этаж, в центре, прямо 1 дверь!!!')
        elif namber == 218:
            bot.send_message(message.chat.id, '2 этаж, в центре, прямо 2 лверь!!!')
        elif namber == 301:
            bot.send_message(message.chat.id, '3 этаж, в центре, слева 1 дверь!!!')
        elif namber == 302:
            bot.send_message(message.chat.id, '3 этаж, в центре, слева 2 дверь!!!')
        elif namber == 303:
            bot.send_message(message.chat.id, '3 этаж, левое крыло, слева 1 дверь!!!')
        elif namber == 304:
            bot.send_message(message.chat.id, '3 этаж, левое крыло, слева 2 дверь!!!')
        elif namber == 305:
            bot.send_message(message.chat.id, '3 этаж, левое крыло, слева 3 дверь!!!')
        elif namber == 306:
            bot.send_message(message.chat.id, '3 этаж, левое крыло, слева 4 дверь!!!')
        elif namber == 307:
            bot.send_message(message.chat.id, '3 этаж, левое крыло, справа 1 дверь!!!')
        elif namber == 311:
            bot.send_message(message.chat.id, '3 этаж, в центре, прямо 1 дверь!!!')
        elif namber == 403:
            bot.send_message(message.chat.id, '4 этаж, в центре, прямо 1 дверь!!!')
        elif namber == 404:
            bot.send_message(message.chat.id, '4 этаж, в центре, слева 1 дверь!!!')
        elif namber == 405:
            bot.send_message(message.chat.id, '4 этаж, в центре, слева 2 дверь!!!')
        elif namber == 406:
            bot.send_message(message.chat.id, '4 этаж, левое крыло, слева 1 дверь!!!')
        elif namber == 407:
            bot.send_message(message.chat.id, '4 этаж, левое крыло, справа 1 дверь!!!')
        else:
            bot.send_message(message.chat.id, 'Кабинет не найден! Проверьте номер.')
            
    except ValueError:
        bot.send_message(message.chat.id, 'Введите число')


bot.polling(none_stop=True)