#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import conf
import json

import lib.onem2m as onem2m

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

ID = ""


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! Welcome to ESC-bot!')
    update.message.reply_text(
        'This bot allows you to check the status of the school doors and,' + ' if you have permission, to control it.')
    update.message.reply_text("If you want to see a list of commands, type '/help.'")


def sendCI(roomID, opcl):
    global ID

    url = conf.CSE.host + ":" + conf.CSE.port + "/Mobius/database-test/cnt-db"
    print("Try: create CI -", url)

    con = "" + roomID + " " + ID + " " + opcl
    res = onem2m.createCI(conf.AE.name, url, con).send()
    res_text = json.loads(res.text)

    if res.headers['X-M2M-RSC'] in ["2000", "2001"]:
        print(res.headers['X-M2M-RSC'], "Success", res.headers['Content-Location'])

        print("\n<---- created  content ---->")
        for key in res_text['m2m:cin'].keys():
            print('    ' + key + ":", res_text['m2m:cin'][key])

    else:
        print(res.headers['X-M2M-RSC'], "Unknown", res_text['m2m:dbg'])
        print(res_text)


def _help(bot, update):
    """Send a message when the command /help is issued."""
    cmdInfo = "<Command Information>\n"
    cmdInfo += "/list : Show list of classrooms where status can be confirmed\n"
    cmdInfo += "/getinfo + 'building name' + 'room number' : "
    cmdInfo += "You can see if the door of the classroom you want to know is open or closed\n"
    cmdInfo += "/open + 'building name' + 'room number' : "
    cmdInfo += " You can open the door to the classroom\n"
    cmdInfo += "/close + 'building name' + 'room number' : "
    cmdInfo += " You can close the door to the classroom\n"
    cmdInfo += "/login + 'id' : Change the login ID\n"
    cmdInfo += "/id : Check the login ID "
    update.message.reply_text(cmdInfo)


def checkOC(room_num):

    status = {"1": "open", "2": "close"}

    cnt = {}
    cnt['parent'] = conf.CSE.id + "/" + room_num
    cnt['name'] = "cnt-door"

    res = onem2m.retrieveCI(conf=conf, cnt=cnt).send()
    res_text = json.loads(res.text)

    print(res_text)

    res.close()
    # print(res.text)

    return res_text['m2m:cin']['con']


def getroomlist():
    retdata = {}

    res = onem2m.discovery(conf=conf).send()
    res_text = json.loads(res.text)

    print(res_text)

    for data in res_text['m2m:uril']:
        print(data)
        rooms = data.split('/')
        if rooms[1] == 'database-test':
            continue
        retdata[rooms[0]] = []
        retdata[rooms[0]].append(rooms[1])
        print(rooms[1])

    return retdata


def open_door(bot, update, args):
    global ID

    building = args[0]
    room_num = args[1]

    if ID == "":
        update.message.reply_text("Please login first.")

    else:
        sendCI(room_num, "open")


#        flag = checkOC(room_num)
#        flag = flag.split()[2]

#        if flag == '1':
#            update.message.reply_text("Open the " + building + " " + room_num + " door successfully.")
#        else:
#            update.message.reply_text("Failed to open the " + building + " " + room_num + " door.")


def close_door(bot, update, args):

    global ID

    building = args[0]
    room_num = args[1]

    if ID == "":
        update.message.reply_text("Please login first.")
    else:
        sendCI(room_num, "close")


#        flag = checkOC(room_num)
#        flag = flag.split()[2]
#
#        if flag.split()[2] == '2':
#            update.message.reply_text("Close the " + building + " " + room_num + " door successfully")
#        else:
#            update.message.reply_text("Failed to close the " + building + " " + room_num + " door")


def door_list(bot, update):
    """Send a message when the command /list is issued."""

    doorlist = getroomlist()

    doorInfo = "\t[List of Lecturerooms]\n"

    for building in doorlist.keys():
        doorInfo += "<" + building + ">\n"
        for room in doorlist[building]:
            print(room)
            doorInfo += room + " "
        doorInfo += "\n\n"
    update.message.reply_text(doorInfo)


def getinfo(bot, update, args):
    building = args[0]
    room_num = args[1]

    flag = checkOC(room_num)

    print(flag)
    #flag = flag.split()[2]
    #print(flag)

    if flag == '1':  #open
        update.message.reply_text(building + " " + room_num + " is open.")
    if flag == '2':  #close
        update.message.reply_text(building + " " + room_num + " is closed.")


def login(bot, update, args):

    global ID
    ID = args[0]

    update.message.reply_text("Logged in as " + ID + ".")


def _id(bot, update):
    global ID

    if ID == "":
        update.message.reply_text("You are not logged in.")

    else:
        update.message.reply_text("You are logged in as " + ID + ".")


def echo(bot, update):
    """Echo the user message."""

    text = update.message.text
    #update.message.reply_text(text)
    msg = "I don't understand what you say."
    print(text)

    if text == 'hi' or text == 'hello':
        msg = "Oh, hi~ I'm esc bot."
        update.message.reply_text(msg)

    elif text == 'help':
        msg = "Please type '/help.'"
        update.message.reply_text(msg)

    elif text == 'bye':
        msg = "Good bye~."
        update.message.reply_text(msg)

    else:
        update.message.reply_text(msg)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""

    #discovery해서 list, getinfo 출력하기

    #open, close CI 잘보내지는지 확인 --> no

    updater = Updater(YOUR_TELEGRAM_BOT_API_KEY)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("list", door_list))
    dp.add_handler(CommandHandler("open", open_door, pass_args=True))
    dp.add_handler(CommandHandler("close", close_door, pass_args=True))
    dp.add_handler(CommandHandler("login", login, pass_args=True))
    dp.add_handler(CommandHandler("getinfo", getinfo, pass_args=True))
    dp.add_handler(CommandHandler("id", _id))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
