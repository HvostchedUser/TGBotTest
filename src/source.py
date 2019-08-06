import peewee
import os
from flask import Flask, request

db=peewee.SqliteDatabase('users.db')

class User(peewee.Model):
    chat_id = peewee.IntegerField(unique=True)
    state = peewee.IntegerField(default=0)
    class Meta:
        database=db

def init():
    db.connect()
    db.create_tables([User],safe=True)
    db.close()
def get_state(chat_id):
    user=User.get_or_none(chat_id=chat_id)
    if user is None:
        return -1
    return user.state
def set_state(chat_id,state):
    user,created=User.get_or_create(chat_id=chat_id)
    user.state=state
    user.save()
init()




import telebot

API_TOKEN=os.getenv('TG_API_TOKEN')
bot=telebot.TeleBot(API_TOKEN,skip_pending=True)
server=Flask(__name__)
q=['Ты человек или automata de merde?','Тебе нужны красивые желтые перчатки для работы?','?','Как выглядят те самые люди, которые ботов пишут?','Ты победил. Начнем снова.']
a=['человек','да','!','как люди, которые ботов пишут']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,text="Здравздвуйде. Чтобы ответить на вопросы, отвечайте на вопросы.")
    set_state(message.chat.id,0)
    quest(message.chat.id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text != a[get_state(message.chat.id)]:
        bot.reply_to(message,"\""+message.text+"\" - это не правильный ответ. Надо было написать \""+a[get_state(message.chat.id)]+"\"")
        bot.send_message(message.chat.id,"И вообще, начинай заново")
        set_state(message.chat.id,0)
    else:
        if q[get_state(message.chat.id)+1]=="Ты победил. Начнем снова.":
            bot.send_message(message.chat.id,q[get_state(chat_id)+1])
            set_state(message.chat.id,0)
        else:
            bot.reply_to(message,"Окай, некст")
            set_state(message.chat.id,get_state(message.chat.id)+1)

    quest(message.chat.id)
def quest(chat_id):
    bot.send_message(chat_id,q[get_state(chat_id)])
while True:
    try:
        bot.polling()
    except:
        print("Except")
