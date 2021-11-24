import os
from exelpars import databut, datasort, dicsort

class Frame:

    def __init__(self, name) -> None:
        self.name = name
        self.sum = 0
        #self.id = msg.message_id
        #self.chat = msg.chat.id

        self.dicprice = {
            "экстра":dicsort[name][0],
            "1й разбор":dicsort[name][1],
            "2й разбор":dicsort[name][2],
            "3й разбор":dicsort[name][3],
            "детки": dicsort[name][4]}

        #self.dicvals = {"экстра":0, "1й разбор":0, "2й разбор":0, "3й разбор":0, "детки":0}

        self.pricestr = [
            f'экстра:{self.dicprice["экстра"]}грн.',
            f'1й разбор:{self.dicprice["1й разбор"]}грн',
            f'2й разбор:{self.dicprice["2й разбор"]}грн',
            f'3й разбор:{self.dicprice["2й разбор"]}грн',
            f'детки:{self.dicprice["детки"]}грн./дес.']

        self.menu = ["галерея", "информация", "стоимость"]
        self.info = 'informpacket'
        self.prev = self.photoset(self.name, 'prev')[0]
        self.galery = self.photoset(self.name, 'photo')


        #'PHOTOSET'
    def photoset(self, s, dir):
        path = os.path.join(os.getcwd(), dir)
        flist = []
        for f in os.scandir(path):
            if f.is_dir(): continue
            if s in f.path.split('\\')[-1]:
                flist.append(f.path)
        return flist



""" def photoset2():
    path = os.path.join(os.getcwd(), 'photo')
    for root, fold, files in os.walk(path):
        print(files) """



fsort = {f : Frame(f)for f in dicsort}

#for f in fsort:print(fsort[f].prev)
#photoset2()
