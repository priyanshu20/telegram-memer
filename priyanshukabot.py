import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import textwrap
from betterGenerator import memeMaker
import os

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

# UTILITIES
knownUsers = []
userStep = {}
userMemes = {}
keyConverter = {"shaq-crying": "crying.png", "bhagwaan-hai": "bhagwan_hai.jpg"}
defaultText = {"crying.png": [], "bhagwan_hai.jpg": [
    "Kabhi kabhi lagta hai ki", "apun hi Bhagwan hai"]}


commands = {  # command description used in the "help" command
    'start': 'Do this before creating every meme to avoid any glitches',
    'help': 'Gives you information about the available commands',
    'memes': 'Shows all the meme templates and starts the meme creation process',
    'todo': 'Displays features yet to be implemented'
}


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
imageSelect.add('shaq-crying', "bhagwaan-hai")
# baap ko mat sikha , avoid
hideBoard = types.ReplyKeyboardRemove()
lineSelect = types.ForceReply(selective=False)
#


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        # save user id, so you could brodcast messages to all users of this bot later
        knownUsers.append(cid)
        # save user id and his current "command level", so he can use the "/getImage" command
        userStep[cid] = 0
        bot.send_message(
            cid, "Hi,some useful commands for you,try not to spam the bot with random commands it tends to slow things down")
        # bot.send_message(cid, "chalo ab /memes likho")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(
            cid, "You are now ready to create memes /memes")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# @bot.message_handler(commands=['meme'])
# def meme(message):
#     # print(type(message))
#     # print(chat_id=message['content_type']['from_user']['id'])
#     # print(message.from_user.id)
#     photo = open("./templates/avoid.jpg", "rb")
#     bot.send_photo(chat_id=message.from_user.id, photo=photo)

# -----------STEP1---------------------


@bot.message_handler(commands=['memes'])
def template_selector(message):
    cid = message.chat.id
    bot.send_message(cid, "Please choose your image now",
                     reply_markup=imageSelect)
    userStep[cid] = 1


# -------------STEP2------------------------
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(message):
    cid = message.chat.id
    text = message.text
    try:
        userMemes[cid] = keyConverter[text]
        print(userMemes)
        bot.send_photo(cid, open(f'./templates/{keyConverter[text]}', 'rb'),
                       reply_markup=hideBoard)
        bot.send_message(
            cid, "This is your chosen template if this was not what u wanted do /start to choose again")
        bot.send_message(
            cid, "The text on bottom will appear automatically")
        # bot.send_message(
        # cid, "if this was what you want,enter text seperating lines by |")
        # bot.send_message(cid, "Bottom text will appear on its own")
        bot.send_message(cid, "Enter text seperating lines with |",
                         reply_markup=lineSelect)
        userStep[cid] = 2
    except:
        bot.send_message(
            cid, "Some error occured try again type /start", reply_markup=hideBoard)
        userStep[cid] = 0


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def meme_line_no(message):
    cid = message.chat.id
    text = message.text
    lines = list(text.split('|'))
    memeMaker(template=userMemes[cid], top_lines=lines,
              bottom_lines=defaultText[userMemes[cid]], cid=cid)
    bot.send_message(cid, "Creating meme", reply_markup=hideBoard)
    bot.send_photo(
        cid, open(f"./{cid}.png", "rb"), reply_markup=hideBoard)
    userStep[cid] = 0
    print(userStep)


@bot.message_handler(commands=['todo'])
def todo(message):
    cid = message.chat.id
    bot.send_message(
        cid, "1-Ability to change the bottom text of every meme,\n 2- Ability for users to add their own meme templates")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message, "This is not a recognized command")


bot.polling()
