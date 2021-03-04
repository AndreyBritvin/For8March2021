# import telegram
from questions import questions
import copy
# import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, ParseMode
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# logging.basicConfig(
#   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
# keyboard = []
X = 5
Y = 4
TOKEN = "TOKEN"
# usernames = {451269878: ['Andrey', 0, -1, 'Nothing'], 588317655: ['Слава', 0, -1,
#                                                                  'Nothing']}  # id:[name, num of correct answers, num of question, question], ---keyboard---
usernames = {}
teams = {"Большой брат":["",[],0,-10000,-10000]}  # name: [[],[id], total num of correct, total num of uncorrect, cor-uncor]

isTask = False
penaltyCount = 0.5

def getNameById(id, d, place=1, isUsers = False):
    for i in list(d.keys()):
        if place == 1 and not isUsers:
            for idToFind in d[i][place]:
                if idToFind == id:
                    return str(i)
        elif place != 1:
            if d[i][place] == id:
                return str(i)
        elif place == 1 and isUsers:
            if d[i][place] == id:
                return str(i)
    return None


def generateKeyboard(sizeX, sizeY, isAsmin = False):
    keyboard = []
    for i in range(sizeX):
        keyboard.append([])
        for j in range(sizeY):
            keyboard[i].append(0)

    for i in range(sizeX):
        for j in range(sizeY):
            keyboard[i][j] = InlineKeyboardButton(str(sizeY * (i) + j + 1),  # + "❌",
                                                  callback_data=list(questions.keys())[sizeY * i + j])
    keyboard.append([InlineKeyboardButton("Посмотреть статистику", callback_data="stat")])
    if isAsmin:
        keyboard.append([InlineKeyboardButton("Статистика по игрокам", callback_data="stat2"),
                         InlineKeyboardButton("Статистика по командам", callback_data="stat3")])
    return keyboard

teamskb = {"Большой брат":[generateKeyboard(X,Y, isAsmin=True)]} #name:[keyboard]

def start(update: Update, context: CallbackContext) -> None:
    # global keyboard
    print("/start " + update.message.from_user.first_name)
    if update.message.chat_id not in list(usernames.keys()):
        # usernames[update.message.chat_id][3] = "Nothing"
        usernames[update.message.chat_id] = [str(update.message.from_user.first_name),
                                             0, -1,
                                             "Nothing"]  # , generateKeyboard(X, Y)]  # username, num of solved questions, num of question

    """keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]"""
    #    print(keyboard)
    # reply_markup = InlineKeyboardMarkup(teams[getNameById(update.message.chat_id)][0])

    update.message.reply_text('Привет!\n'
                              'Сначала вступи или создай команду:\n'
                              'Создать команду: /createTeam _Название команды_ (на одной строчке)\n'
                              'Вступить в уже созданную: /joinTeam _Название команды_ (также на одной строчке)'
                              )  # , reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    # global keyboard
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    print(query.data)
    if isTask:
        if query.data == "MainMenu123":
            query.edit_message_text(text="Выберите задание и дайте на него ответ",
                                    reply_markup=InlineKeyboardMarkup(
                                        teamskb[getNameById(query.message.chat.id, teams)][0]))
            usernames[query.message.chat.id][3] = "Nothing"

        elif query.data in list(questions.keys()):
            # print(questions[query.data])
            isSolved = questions[query.data][2]
            toAppend = ""
            print(getNameById(query.message.chat.id, isSolved))
            print(isSolved)
            if getNameById(query.message.chat.id, teams) in list(isSolved.keys()):
                toAppend = "\n\nЭто задание было решено " + \
                           usernames[isSolved[getNameById(query.message.chat.id, teams)][1][0]][0]

            query.edit_message_text(text=str(questions[query.data][0]) + toAppend,
                                    reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("Вернуться к выбору заданий",
                                                               callback_data="MainMenu123")]]), parse_mode=ParseMode.HTML)
            usernames[query.message.chat.id][3] = query.data
            usernames[query.message.chat.id][2] = list(questions.keys()).index(query.data) + 1
            print(query.message.chat.id, " ", usernames[query.message.chat.id][2])
    else:
        query.edit_message_text(text="Выполнение заданий приостановлено/ещё не началось. Чтобы показать задания,"
                                     " напишите /showTask")
    if query.data == "stat":
        statistic = "Статистика решенных задач по командам:\n"

        """
        num_team = {}
        for i in list(teams.keys()):
            # name = teams[i][1]
            #summa = teams[i][2]
            num_team[teams[i][2]] = str(i)

            #statistic += str(i) + ": " + str(summa) + "\n"
        print(num_team)
        sortSum = list(num_team.keys())
        sortSum.sort(reverse=True)
        print(sortSum)
        for i in range(len(sortSum)):
            statistic += str(i+1)+". "+num_team[sortSum[i]] + ": " + str(sortSum[i]) + "\n" #1. Name:res \n
        """
        teamsc = copy.deepcopy(teams)
        num_team = []
        pl = 4
        for i in list(teams.keys()):
            num_team.append(teams[i][pl])

        num_team.sort(reverse=True)
        print(num_team)

        for i in range(len(num_team)-1):
            name = getNameById(num_team[i], teamsc, place=pl)
            print(num_team[i], teamsc)

            if name == getNameById(query.message.chat.id, teams):
                name2 = "<u>" + name + "</u>"
            else:
                name2 = name
            statistic += str(i + 1) + ". " + name2 + ": " + str(num_team[i]) + " (✅:"+str(teamsc[name][2])+", ❌:"+str(teamsc[name][3])+")\n"  # 1. Name:res \n
            del teamsc[name]

        statistic += "\nВыберите задание и дайте на него ответ:"
        query.edit_message_text(text=statistic,
                                reply_markup=InlineKeyboardMarkup(
                                    teamskb[getNameById(query.message.chat.id, teams)][0]), parse_mode=ParseMode.HTML)
    if query.data == "stat2":
        nums = []
        users = copy.deepcopy(usernames)
        for i in list(usernames.keys()):
            nums.append(usernames[i][1])
        nums.sort(reverse=True)
        statistic = "Статистика решенных задач по игрокам:\n"
        for i in range(len(nums)):
            #print(usernames)
            #print(getNameById(nums[i], users, 1, True))
            name = usernames[int(getNameById(nums[i], users, 1, True))][0]
            statistic+=str(i+1)+". "+name+": "+str(nums[i])+"\n"
            del users[int(getNameById(nums[i], users, 1, True))]

        query.edit_message_text(text=statistic,
                                reply_markup=InlineKeyboardMarkup(
                                    teamskb[getNameById(query.message.chat.id, teams)][0]), parse_mode=ParseMode.HTML)

    if query.data == "stat3":
        num_team = {}
        statistic = "Статистика решенных задач по командам (без штрафов):\n"
        for i in list(teams.keys()):
            # name = teams[i][1]
            # summa = teams[i][2]
            num_team[teams[i][2]] = str(i)

            # statistic += str(i) + ": " + str(summa) + "\n"
        #print(num_team)
        sortSum = list(num_team.keys())
        sortSum.sort(reverse=True)
        #print(sortSum)
        for i in range(len(sortSum)):
            statistic += str(i + 1) + ". " + num_team[sortSum[i]] + ": " + str(sortSum[i]) + "\n"  # 1. Name:res \n

        query.edit_message_text(text=statistic,
                                reply_markup=InlineKeyboardMarkup(
                                    teamskb[getNameById(query.message.chat.id, teams)][0]), parse_mode=ParseMode.HTML)
    print(usernames)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Хай! Тут проходит квест для 8'В'. Чтобы начать напиши /start\n затем создай команду"
                              " или присоединись к уже готовой и решай задания. Удачи!"
                              "(подробности при написании /start)")


def answers(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    #  global keyboard
    print(update.message.text)
    # update.message.reply_text(update.message.text)

    if usernames[update.message.chat_id][3] == "Nothing":  # answer without question
        update.message.reply_text("Чтобы показать задания, напишите /showTask")

    elif update.message.text in questions[usernames[update.message.chat_id][3]][1] and \
            getNameById(update.message.chat_id, teams) not in list(
        questions[usernames[update.message.chat_id][3]][2].keys()):
        #   getNameById(update.message.chat_id, teams) != getNameById(update.message.chat_id,
        #                                                             questions[usernames[update.message.chat_id][3]][
        #                                                                2]):

        # str(update.message.chat_id) not in questions[usernames[update.message.chat_id][3]][1]:  # answer correct

        questionNum = usernames[update.message.chat_id][2]
        i = (questionNum - 1) // Y
        j = questionNum % Y - 1
        print(i, j)
        questions[usernames[update.message.chat_id][3]][2][getNameById(update.message.chat_id, teams)] = ["", [
            update.message.chat_id]]
        """
        questions[usernames[update.message.chat_id][3] + "\n\nРешено " + str(update.message.from_user.first_name)] = questions[
            usernames[update.message.chat_id][3]]
        del questions[usernames[update.message.chat_id][3]]
        """
        teamskb[getNameById(update.message.chat_id, teams)][0][i][j] = InlineKeyboardButton("✅",
                                                                                          callback_data=
                                                                                          usernames[
                                                                                              update.message.chat_id][
                                                                                              3])

        usernames[update.message.chat_id][1] = usernames[update.message.chat_id][
                                                   1] + 1  # num of correct answers for user
        teams[getNameById(update.message.chat_id, teams)][2] += 1  # for team
        teams[getNameById(update.message.chat_id, teams)][4] += 1  # for team

        usernames[update.message.chat_id][2] = -1  # current ques
        usernames[update.message.chat_id][3] = "Nothing"

        update.message.reply_text("Правильный ответ ✅ \n\nВыбирайте следующее задание:",
                                  reply_markup=InlineKeyboardMarkup(
                                      teamskb[getNameById(update.message.chat_id, teams)][0]))

    # elif getNameById(update.message.chat_id, teams) == getNameById(update.message.chat_id,
    #                                                               questions[usernames[update.message.chat_id][3]][2]):
    elif getNameById(update.message.chat_id, teams) in list(questions[usernames[update.message.chat_id][3]][2].keys()):
        update.message.reply_text("На этот вопрос уже ответили. Возвращайтесь к выбору заданий "
                                  "и решайте другое :)",
                                  reply_markup=InlineKeyboardMarkup(
                                      teamskb[getNameById(update.message.chat_id, teams)][0]))
    else:  # answer incorrect
        teams[getNameById(update.message.chat_id, teams)][3] += penaltyCount  # for team
        teams[getNameById(update.message.chat_id, teams)][4] -= penaltyCount  # for team
        update.message.reply_text("Ответ неверный ❌ \nПопробуйте ещё")


def restartTotal(update: Update, context: CallbackContext) -> None:
    pass
    """
    generateKeyboard(X, Y)
    for i in list(questions.keys()):
        questions[i][1] = ""
    for i in list(usernames.keys()):
        usernames[i][3] = "Nothing"
    """


def createTeam(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
    name = {}
    try:
        name = str(update.message.text).split("/createTeam ")[1]
    except IndexError:
        update.message.reply_text("Для создания команды напишите /createTeam _Название команды_ (на одной строчке!)")
    else:
        print(name)
        if getNameById(update.message.chat_id, teams) == None:
            teams[name] = [[], [update.message.chat_id], 0,0,0]
            teamskb[name] = [generateKeyboard(X,Y)]
            # update.message.reply_text("Команда " + name + " создана. Вы автоматически стали ее членом."
            #                                             " \nВыберите задание и дайте на него ответ:",
            #                         reply_markup=InlineKeyboardMarkup(teams[name][0]))
            update.message.reply_text("Команда '" + name + "' создана\nЧтобы показать задания, отправьте /showTask")

        else:
            if (name not in list(teams.keys())):
                teams[name] = [[], [], 0,0,0]
                teamskb[name] = [generateKeyboard(X, Y)]
                update.message.reply_text("Команда '" + name + "' создана. Вы не стали ее членом автоматически, "
                                                               "потому что уже состоите в другой команде."
                                                               " Для вступления в эту команду, напишите /joinTeam "
                                          + name + " (на одной строчке!). Чтобы показать задания,"
                                                   " напишите /showTask")
            else:
                update.message.reply_text("Команда '" + name + "' уже существует."
                                                               " Для вступления в эту команду, напишите /joinTeam "
                                          + name + " (на одной строчке!) Чтобы показать задания, напишите /showTask")


def joinTeam(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
    name = {}
    try:
        name = update.message.text.split("/joinTeam ")[1]
    except IndexError:
        update.message.reply_text("Для вступления в команду напишите /joinTeam _Название команды_ (на одной строчке!)")

    else:
        print(name)
        for i in list(teams.keys()):
            try:
                teams[i][1].remove(update.message.chat_id)
            except ValueError:
                continue
        try:
            teams[name][1].append(update.message.chat_id)
        except KeyError:
            update.message.reply_text("Такой команды не существует. Для вступления в уже существующую команду"
                                      " напишите /joinTeam _Название команды_ (на одной строчке!)")
        else:
            #   update.message.reply_text("Вы вступили в команду " + name + "\nВыберите задание и дайте на него ответ:",
            #                        reply_markup=InlineKeyboardMarkup(teams[name][0]))
            update.message.reply_text(
                "Вы вступили в команду '" + name + "'\nЧтобы показать задания, отправьте /showTask")


def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(str(usernames))
    update.message.reply_text(str(teams))
    # update.message.reply_text(str(getNameById(451269878)))


def showTask(update: Update, context: CallbackContext) -> None:
    if isTask:
        try:
            update.message.reply_text(text="Выберите задание и дайте на него ответ",
                                      reply_markup=InlineKeyboardMarkup(
                                          teamskb[getNameById(update.message.chat_id, teams)][0]))
        except KeyError:
            update.message.reply_text(text="Вы не состоите ни в одной команде. Напишите /start для подробностей")
    else:
        update.message.reply_text(text="Дождитесь разрешения показа")


def enableTask(update: Update, context: CallbackContext) -> None:
    global isTask
    isTask = True
    update.message.reply_text(text="Задания разрешены")


def disableTask(update: Update, context: CallbackContext) -> None:
    global isTask
    isTask = False
    update.message.reply_text(text="Задания запрещены")


def mailing(update: Update, context: CallbackContext) -> None:
    bot = Bot(token=TOKEN)
    for i in list(usernames.keys()):
        bot.send_message(chat_id=int(i), text=str(update.message.text).split("/mailing1 ")[1])
     #   bot.send_sticker(chat_id=int(i),
     #                   sticker='CAACAgIAAxkBAAIBZ2A0nt7nzJMJnbzdEbBEVqw6aWk-AAIQAAPdzt44vqSCOa4N-EAeBA')


def mailingReady(update: Update, context: CallbackContext) -> None:
    bot = Bot(token=TOKEN)
    for i in list(usernames.keys()):
        bot.send_message(chat_id=int(i), text="За то, что вы такие умные, отправляетесь в")
        bot.send_sticker(chat_id=int(i),
                         sticker='CAACAgIAAxkBAAIBZ2A0nt7nzJMJnbzdEbBEVqw6aWk-AAIQAAPdzt44vqSCOa4N-EAeBA')

def penalty(update: Update, context: CallbackContext) -> None:
    num = int(update.message.text.split("/penalty ")[1].split(" ")[0])
    name =  update.message.text.split("/penalty "+str(num)+" ")[1]
    teams[name][3]+=num
    teams[name][4] -= num

def thanks (update: Update, context: CallbackContext) -> None:
    bot = Bot(token=TOKEN)
    for i in list(usernames.keys()):
        bot.send_message(chat_id=int(i), text="Над ботом работал: Андрей\n"
                                              "Вопросы придумали: Артём, Кирилл П., Слава\n"
                                              "Стикеры рисовал: Миша С.\n"
                                              "Бота тестировали: Андрей, Слава, Миша С., Артём, Кирилл Н., Саша Р., Максим С., Кирилл П., Саша Н., Влад, Рома\n"
                                              "\n"
                                              "Огромное спасибо им! С наступающим праздником!🥳🎉\n\n\n"
                                              "P.S. Код на бота: https://github.com/AndreyBritvin/For8March2021\n"
                                              "Ссылка на стикеры: https://t.me/addstickers/B_853_class")

def main():
    # generateKeyboard(X, Y)
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # restarts
    # updater.dispatcher.add_handler(CommandHandler('help', help_command))
    # updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # teams
    updater.dispatcher.add_handler(CommandHandler('createTeam', createTeam))
    updater.dispatcher.add_handler(CommandHandler('joinTeam', joinTeam))

    # tasks
    updater.dispatcher.add_handler(CommandHandler('showTask', showTask))
    updater.dispatcher.add_handler(CommandHandler('enableTask', enableTask))
    updater.dispatcher.add_handler(CommandHandler('disableTask', disableTask))

    # for admin
    updater.dispatcher.add_handler(CommandHandler('mailing1', mailing))
    updater.dispatcher.add_handler(CommandHandler('mailingReady', mailingReady))
    updater.dispatcher.add_handler(CommandHandler('status', status))
    updater.dispatcher.add_handler(CommandHandler('restartTotal', restartTotal))
    updater.dispatcher.add_handler(CommandHandler('penalty', penalty))
    updater.dispatcher.add_handler(CommandHandler('thanks', thanks))

    updater.dispatcher.add_handler(MessageHandler(Filters.all, answers))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
