# import telegram
from questions import questions

# import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# logging.basicConfig(
#   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
keyboard = []
X = 4
Y = 3
users = {}
usernames = {}


def generateKeyboard(sizeX, sizeY):
    for i in range(sizeX):
        keyboard.append([])
        for j in range(sizeY):
            keyboard[i].append(0)

    for i in range(sizeX):
        for j in range(sizeY):
            keyboard[i][j] = InlineKeyboardButton(str(sizeY * (i) + j + 1),
                                                  callback_data=list(questions.keys())[sizeY * (i) + j])
    keyboard.append([InlineKeyboardButton("Посмотреть статистику", callback_data="stat")])


def start(update: Update, context: CallbackContext) -> None:
    global keyboard
    if update.message.chat_id not in users:
        users[update.message.chat_id] = "Nothing"
        usernames[update.message.chat_id] = [str(update.message.from_user.first_name),
                                             0, -1]  # username, num of solved questions, num of question

    """keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]"""
    #    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите задание', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    global keyboard
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    print(query.data)

    if query.data == "MainMenu123":
        query.edit_message_text(text="Выберите задание",
                                reply_markup=InlineKeyboardMarkup(keyboard))
        users[query.message.chat.id] = "Nothing"

    elif query.data in list(questions.keys()):
        isSolved = questions[query.data][1]
        toAppend = ""
        if isSolved!="":
            toAppend = "\n\nРешено "+isSolved
        query.edit_message_text(text=str(query.data)+toAppend,
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Вернуться к выбору заданий",
                                                                                         callback_data="MainMenu123")]]))
        users[query.message.chat.id] = query.data
        usernames[query.message.chat.id][2] = list(questions.keys()).index(query.data)+1
        print(query.message.chat.id," ", usernames[query.message.chat.id][2])

    elif query.data == "stat":
        statistic = "Вот кто сколько решил:\n"
        for i in list(usernames.keys()):
            name = usernames[i][0]
            num = usernames[i][1]
            statistic += name + ": " + str(num) + "\n"
        statistic += "\nВыберите задание:"
        query.edit_message_text(text=statistic, reply_markup=InlineKeyboardMarkup(keyboard))
    print(users)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Хай! Тут проходит квест для 8'В'. Чтобы начать напиши /start")


def answers(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global keyboard
    print(update.message.text)
    # update.message.reply_text(update.message.text)

    if users[update.message.chat_id] == "Nothing":  # answer without question
        update.message.reply_text("Выберите вопрос и дайте на него ответ")

    # elif
    elif update.message.text in questions[users[update.message.chat_id]][0] and \
            questions[users[update.message.chat_id]][1] == "":  # answer correct

        questionNum = usernames[update.message.chat_id][2]
        i = (questionNum-1) // Y
        j = questionNum % Y -1
        print(i,j)
        questions[users[update.message.chat_id]][1] = str(update.message.from_user.first_name)
        """
        questions[users[update.message.chat_id] + "\n\nРешено " + str(update.message.from_user.first_name)] = questions[
            users[update.message.chat_id]]
        del questions[users[update.message.chat_id]]
"""
        keyboard[i][j] = InlineKeyboardButton("✅",
                                              callback_data=users[update.message.chat_id])

        usernames[update.message.chat_id][1] = usernames[update.message.chat_id][1] + 1  # num of correct answers
        usernames[update.message.chat_id][2] = -1  # current ques
        users[update.message.chat_id] = "Nothing"

        update.message.reply_text("Правильный ответ. Выбирайте следующее задание:",
                                  reply_markup=InlineKeyboardMarkup(keyboard))
    elif questions[users[update.message.chat_id]][1] != "":
        update.message.reply_text("На этот вопрос уже ответили. Решайте другие", reply_markup=InlineKeyboardMarkup(keyboard))
    else:  # answer incorrect
        update.message.reply_text("Ответ неверный, попробуйте ещё")

def restartTotal():
    generateKeyboard(X, Y)
    for i in list(questions.keys()):
        questions[i][1] = ""
    for i in list(users.keys()):
        users[i] = "Nothing"
    

def main():
    generateKeyboard(X, Y)
    # Create the Updater and pass it your bot's token.
    updater = Updater("1680109532:AAEVxsAfCEwlkPtRPUwn2SCJyW8pIdvLjcs")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    updater.dispatcher.add_handler(CommandHandler('restartTotal', restartTotal))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))


    updater.dispatcher.add_handler(MessageHandler(Filters.text, answers))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
