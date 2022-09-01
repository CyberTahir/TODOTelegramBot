import telebot

token = "5619126822:AAHl3aCS-SlgEmSNc2OBGeGjdgp21_U55Hc"
bot = telebot.TeleBot(token)

tasks = {}


def add_task(date, task):
    date = date.lower()

    if date not in tasks:
        tasks[date] = []

    tasks[date].append(task)


def get_text(date):
    date = date.lower()

    if date in tasks:
        text = date.upper()

        for task in tasks[date]:
            text += f"\n[ ] {task}"
    else:
        text = f"Задач на {date} нет."

    return text


@bot.message_handler(commands=["help"])
def help_fn(message):
    help_txt = """/help - напечатать справку по программе.
/add - добавить задачу в список.
/show - напечатать все добавленные задачи."""

    bot.send_message(message.chat.id, help_txt)


@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)

    if len(command) != 3:
        print("Неверные данные")
        return

    date = command[1]
    task = command[2]

    add_task(date, task)
    text = f"Задача {task} добавлена на дату {date}."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["show", "print"])
def show(message):
    dates = message.text.split(maxsplit=1)
    if len(dates) == 1:
        dates = ["сегодня"]
    else:
        dates = dates[1].split()

    text_list = [get_text(date) for date in dates]
    text = '\n\n'.join(text_list)

    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)