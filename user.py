import os
from datetime import datetime


class User:
    def __init__(self, msg, bot, ds) -> None:
        self.usid = msg.chat.id
        try:
            self.bot = f'{bot.full_name}({bot.username})'
        except:
            self.bot = 'bot'
        self.name = msg.from_user.full_name
        self.contact = ''
        self.vals = {k:{"экстра":0, "1й разбор":0, "2й разбор":0, "3й разбор":0, "детки":0} for k in ds} # values
        self.shop = {} # {name:{quality:value....}...}
        self.history = ''







    def userlog(self, msg, ans):
        path = os.path.join(os.getcwd(), 'users', str(self.usid))
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}//log.txt', 'a', encoding='utf-8')as op:
            if msg:
                op.write(f'{datetime.today().strftime("%d:%m:%Y-%H:%M:%S")} - {msg.from_user.full_name} - {msg.text}\n')
            if ans:
                op.write(f'{datetime.today().strftime("%d:%m:%Y-%H:%M:%S")} - {self.bot} - {ans}\n')
