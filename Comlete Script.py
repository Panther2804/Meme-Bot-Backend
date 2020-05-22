#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:49:10 2020

@author: ppasch
"""
#Importing all the Libs
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Updater
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

updater = Updater(token='Token', use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from PIL import Image, ImageDraw, ImageFont
import textwrap
#######################

#Add memes to programm
drakememe = ["Drake-Comparison.jpg", {'Drake Name': (0,300,11,(0,0,0)), 'Drake No':(600,0,11,(0,0,0)),'Drake Yes':(600,600,11,(0,0,0))}, 100]
expandingbrain = ["Expanding-Brain.jpg", {"Small Brain": (0,0,22,(0,0,0)), "Medium Brain": (0,300,22,(0,0,0)), "Big Brain": (0,600,22,(0,0,0)), "Biggest Brain":(0,900,22,(0,0,0))}, 40]
distractedbf = ["Distracted-Boyfriend.jpg", {'Boyfriend': (580,370,9,(0,0,0)), 'Girlfriend': (920,420,7,(0,0,0)), "Girl in Red Dress": (100,500,12,(0,0,0))},80]
buttonmeme = ["Blank-Button.jpg", {"Button": (30,240,15,(255,255,255)), "Hand": (300,100,15,(255,255,255))}, 40]
handshakememe = ["handshake.jpg", {"Boss": (0,350,15,(255,255,255)), "Hand": (360,350,15,(255,255,255))}, 40]
spongebobws = ["spongebob strong.png", {"Spongebob name": (35,130,20,(0,0,0)), "Spongebob Weak": (400,0,20,(0,0,0)), "Spongebob Strong": (400,270,15,(0,0,0)), }, 40]



memes = {"Drake":drakememe, "Expanding Brain": expandingbrain, 
                 "Distracted Boyfriend": distractedbf, "Hand and Button": buttonmeme, 
                 "Handshake" : handshakememe, "Spongebob Weak / Spongebob Strong": spongebobws}
####################

#everything to do with the conversation handler




  
CONTENT, INFGAT, FIN = range(3)

def start(update, context):
        
    context.user_data.clear()
    context.user_data.update({'Mid': []})

    context.user_data["Mid"].append(update.message.message_id)

        
    message = "Is this message " + listcategories(" or ", memes) + " ?"

    reply_markup = telegram.ReplyKeyboardMarkup(memeselect())

    mid = context.bot.send_message(chat_id=update.effective_chat.id, 
             text=message, 
             reply_markup=reply_markup, one_time_keyboard=True)

    context.user_data["Mid"].append(mid.message_id)
    
    
    

        
                              
    print("start done")
    return CONTENT
    
def content(update, context):
    
    context.user_data["Mid"].append(update.message.message_id)
    
    print("content")
    message = "Ok. This message has " + str(len(memes[str(update.message.text)][1])) + " different text fields: \n"
    for i in memes[str(update.message.text)][1]:
        message += i + " \n"
    
    
    mid = context.bot.send_message(chat_id=update.effective_chat.id, 
             text=message, 
             reply_markup= telegram.ReplyKeyboardRemove())
    context.user_data["Mid"].append(mid.message_id)
    
    context.user_data.update({'Meme': update.message.text})
    context.user_data.update({'Textfield': 0})
    
    currentmeme = context.user_data["Meme"]
    textfieldnumber = context.user_data["Textfield"]
    message = "We will start with " + list(memes[currentmeme][1].keys())[textfieldnumber]
    message += ". Please enter the text for this field now."
    
    mid = context.bot.send_message(chat_id=update.effective_chat.id, 
             text=message)
    context.user_data["Mid"].append(mid.message_id)
    """
    if context.bot.delete_message(chat_id=update.message.chat_id,
                   message_id=update.message.message_id):
        context.bot.send_message(chat_id=update.effective_chat.id, 
             text="Message was deleted")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
             text="error")
        
    """
    

    return INFGAT

def textgatherer(update, context) :
    
    context.user_data["Mid"].append(update.message.message_id)
    
    currentmeme = context.user_data["Meme"]
    textfieldnumber = context.user_data["Textfield"]
    fieldname = list(memes[currentmeme][1].keys())[textfieldnumber]
    
    context.user_data.update({fieldname : update.message.text}) #save the input
    
    context.user_data.update({'Textfield': context.user_data["Textfield"] + 1})
    textfieldnumber = context.user_data["Textfield"]
    
    print("The Current Meme: " + currentmeme)
    print("Textfieldnumber " + str(textfieldnumber))
    print("fieldname " + fieldname)
    print(str(context.user_data))
    
    if context.user_data["Textfield"] < len(memes[currentmeme][1]):
        message = "Ok. Now: " + list(memes[currentmeme][1].keys())[textfieldnumber]
        message += ". Please enter the text for this field now."

        mid = context.bot.send_message(chat_id=update.effective_chat.id, 
                 text=message)
        context.user_data["Mid"].append(mid.message_id)
        
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                 text="your coder boy fucked up. this message should never appear")
    
    if context.user_data["Textfield"] < len(memes[currentmeme][1]) - 1:
        return INFGAT
    else:
        return FIN
    
    
def fin(update, context):
    
    context.user_data["Mid"].append(update.message.message_id)
    
    print("FIN---FIN---FIN---FIN---FIN---FIN---FIN---FIN---FIN")
    
    
    currentmeme = context.user_data["Meme"]
    textfieldnumber = context.user_data["Textfield"]
    fieldname = list(memes[currentmeme][1].keys())[textfieldnumber]
    
    context.user_data.update({fieldname : update.message.text})
    
    context.user_data.update({'Textfield': context.user_data["Textfield"] + 1})
    textfieldnumber = context.user_data["Textfield"]
    
    print("The Current Meme: " + currentmeme)
    print("Textfieldnumber " + str(textfieldnumber))
    print("fieldname " + fieldname)
    print(str(context.user_data))
    
    #context.user_data.update({'pri': update.message.text})
    message = "Ok. Your message is done. You entered the following parameters: \n"
    for i in context.user_data:
        message += (i + " : " +   str(context.user_data[i])) + "\n"
        
    mid = context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup = telegram.ReplyKeyboardRemove())
    context.user_data["Mid"].append(mid.message_id)
    
    print(type(context.user_data))
    
    makememe(context.user_data)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('test.png', 'rb'))
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Meme by @CtrlLinkBot. /start to make the next meme.")

    for i in context.user_data["Mid"]:
        context.bot.delete_message(chat_id=update.message.chat_id,
                   message_id=i)
    
    return ConversationHandler.END
    
    
def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        pass
    except BadRequest:
        # handle malformed requests - read more below!
        context.bot.send_message(chat_id=update.effective_chat.id, text=
                                 'WARNING: "Bad Request"-Error occured. This is most likely caused by the bot trying to delete messages in group chats without permission. Make sure that the Bot is an Admin with the propper permissions to delete messages. If this does not work, contact @Panther2804  ')

    except TimedOut:
        # handle slow connection problems
        pass
    except NetworkError:
        # handle other connection problems
        pass
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        pass
    except TelegramError:
        # handle all other telegram related errors
        pass

dispatcher.add_error_handler(error_callback)
    
    
conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CONTENT: [MessageHandler(Filters.text, content)],
            INFGAT: [MessageHandler(Filters.text, textgatherer)],
            FIN: [MessageHandler(Filters.text, fin)]
        },

        fallbacks=[CommandHandler('cancel', start)]
    )

    
        
dispatcher.add_handler(conv_handler)

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

############################

##additional functions
def listcategories(divider, divlist):
    s = ""
    for i in divlist:
        s += i
        s += divider
            
    s = s[:-len(divider)]
    return s



def makememe(user_data):
    memeinfo = memes[user_data["Meme"]]
    im = Image.open(memeinfo[0])
    im = im.convert("RGB")
    draw = ImageDraw.Draw(im)
    
    smallfont = ImageFont.truetype("sfont.otf", memeinfo[2])
    for i in memeinfo[1]:
        #memeinfo[1][i] cords
        print(i)
        wrap(user_data[i], memeinfo[1][i][0], memeinfo[1][i][1], draw, smallfont, memeinfo[1][i][2], memeinfo[1][i][3])

    im.save("test.png")
    
    


def rmaxwidth(text, width, font):
    print("Text: " + text + " Width: " + str(width))
    for i in range(0, len(text)):
        if font.getsize(text[:i])[0] > width:
            print("returning: " + text[:i-1])
            print("because " + str(font.getsize(text[:i])[0]))
            
            return text[:i-1]
    print("returning whole text")
    return text


def wrap(text, x, y, draw, font, margin, color):
    for line in textwrap.wrap(text, width=margin):
        draw.text((x, y), line, font=font, fill=color)
        y += font.getsize(line)[1]


def memeselect():
    r = []
    if len(memes) % 2 != 1:
        for i in range(0, len(memes), 2):
            r.append([list(memes.keys())[i], list(memes.keys())[i + 1] ])
    else:
        for i in range(0, len(memes) - 1, 2):
            r.append([list(memes.keys())[i], list(memes.keys())[i + 1] ])
        r.append([list(memes.keys())[-1]])
    return r
##############
    
#start bot
updater.start_polling()