from collections import UserDict
import os
import pandas as pd
import tabulate
from user import User
from frame import fsort
from aiogram.utils.markdown import hide_link, text
from aiogram.types import InlineKeyboardMarkup as km, InlineKeyboardButton as kb, ReplyKeyboardMarkup as rm, KeyboardButton as btn, ReplyKeyboardRemove as rem, MediaGroup, InputFile, ChatActions, InputMediaPhoto


users = {}
startboard = ["каталог", "акции", "корзина", "история"]
sortboard = ["экстра", "1й разбор", "2й разбор", "3й разбор", "детки", "назад"]
chengboard = ['+1', '+2', '+5', '+10', '-1', '-2', '-5', '-10', 'вернуться', 'сбросить', 'в корзину']

# Генерация клавиатуры.
def get_keyboard(board, n=2):
    but = [kb(text=str(w).title(), callback_data=w) for w in board]
    return km(resize_keyboard=True, row_width=n).add(*but)
# Генерация кнопок
def get_btn(blist, n):
    return rm(resize_keyboard=True, row_width=n).row(*[btn(i) for i in blist])

# START #
async def startans(dp, msg):
    #await msg.answer(f'ваш номер : {msg.chat.id}', reply_markup=get_keyboard(startboard, 2))
    await msg.reply(f'ваш номер : {msg.chat.id}', reply_markup=get_btn(startboard, 2))

async def catalog(bot, msg, ds):
    for f in fsort:
        with open(fsort[f].prev, 'rb')as op:
            photo = op   #InputMediaPhoto(op)
            await bot.send_photo(
                    chat_id=msg.chat.id,
                    photo=photo,
                    caption=f,
                    reply_markup=get_keyboard(fsort[f].menu, len(fsort[f].menu))
                    )
        #await msg.answer(fsort[f].name, reply_markup=get_keyboard(fsort[f].menu, len(fsort[f].menu)))

# MES_EDIT #
async def calledit(bot, query):
    #print(query)
    f, *m = query.message.caption.split('\n')
    #i = query.message.photo[0].file_id
    img = open(fsort[f].prev, 'rb')
    if query.data == 'стоимость':
        txt = '\n'.join([f, *fsort[f].pricestr])
        board = [sortboard, 3]
    elif query.data == 'информация':
        txt = '\n'.join([f, fsort[f].info])
        board = [["галерея", "назад", "стоимость"], 3]
    elif query.data == 'галерея':
        #with open(fsort[f].galery[0], 'rb')as op:
        img = open(fsort[f].galery[0], 'rb')
        txt = '\n'.join([f, "галерея"])
        board = [["назад", "информация", "стоимость"], 3]

        """ media = MediaGroup()
        for p in fsort[f].galery:
            media.attach_photo(InputFile(p), '') """
        """ await ChatActions.upload_photo()
            await bot.edit_message_media(
                chat_id=query.message.chat.id,
                media=media, 
                caption=f,
                message_id=query.message.message_id,
                reply_markup=get_keyboard(*board)
                ) """
    elif query.data == 'назад':
        txt = f
        board = [["галерея", "информация", "стоимость"], 3]
    if txt == query.message.text:
        txt = f
        board = [["галерея", "информация", "стоимость"], 3]
    await bot.edit_message_media(
                chat_id=query.message.chat.id,
                media=InputMediaPhoto(img, txt),
                message_id=query.message.message_id,
                reply_markup=get_keyboard(*board)
                )
    img.close()

async def calledit2(bot, query):
    msg, q = query.message, query.data
    img = query.message.photo[0].file_id
    users[msg.chat.id] = users.get(msg.chat.id, User(msg, bot, fsort))
    f, *m = query.message.caption.split('\n')
    txt = '\n'.join([f, f'{q} = {fsort[f].dicprice[q]}грн/шт.'])
    if users[msg.chat.id].vals[f][q]:
        txt += f'\nколичество = {users[msg.chat.id].vals[f][q]}шт'
        txt += f'\nстоимость = {users[msg.chat.id].vals[f][q] * fsort[f].dicprice[q]}грн.'
    board = [chengboard, 4]
    await bot.edit_message_media(
                chat_id=query.message.chat.id,
                media=InputMediaPhoto(img, txt),
                message_id=query.message.message_id,
                reply_markup=get_keyboard(*board)
                )

async def calledit3(bot, query):
    msg = query.message
    i = msg.chat.id
    u = users[i] = users.get(i, User(msg, bot, fsort))
    img = msg.photo[0].file_id
    f, q, *m = msg.caption.split('\n')
    q = q.split(' = ')[0]
    if query.data == 'вернуться':
        txt = '\n'.join([f, *fsort[f].pricestr])
        board = [sortboard, 3]
    elif query.data == 'сбросить':
        try:u.vals[f][q] = 0
        except:pass
        txt = '\n'.join([f, f'{q} = {fsort[f].dicprice[q]}грн/шт.'])
        board = [chengboard, 4]
    elif query.data == 'в корзину':
        try:
            u.shop[f] = u.shop.get(f, {})
            u.shop[f][q] = u.shop[f].get(q, 0) + u.vals[f][q]
            u.vals[f][q] = 0
        except:pass
        print(u.shop[f])
        txt = '\n'.join([f, f'{q} = {fsort[f].dicprice[q]}грн/шт.'])
        board = [chengboard, 4]
        
    else:
        u.vals[f][q] += eval(query.data)
        if u.vals[f][q] < 0:u.vals[f][q] = 0
        txt = '\n'.join([
            f,
            f'{q} = {fsort[f].dicprice[q]}грн/шт.',
            f'количество = {u.vals[f][q]}шт.',
            f'стоимость = {fsort[f].dicprice[q] * u.vals[f][q]}грн.'])
        board = [chengboard, 4]
    if txt == msg.caption:return
    await bot.edit_message_media(
                chat_id=msg.chat.id,
                media=InputMediaPhoto(img, txt),
                message_id=msg.message_id,
                reply_markup=get_keyboard(*board)
                )

# Action #
async def action(bot, msg, ds=None):
    await msg.answer('passed!')

# SHOPPING #
async def shopping(bot, msg, ds=None):
    usid = msg.chat.id
    f, q, *m = msg.caption.split('\n')
    q = q.split(' = ')[0]
    u = users[usid] = users.get(usid, User(msg, bot, fsort))
    #u.shop[f] = u.shop.get(f, {})
    if u.vals[f].get(q):
        #users[usid].shop[f][q] = users[usid].shop[f].get(q, 0) + users[usid].vals[f][q]  # с добавлением
        u.shop[f][q] = u.vals[f][q] # без добавления
        u.vals[f][q] = 0

# КОРЗИНА #
async def shoppack(bot, msg, ds=None):
    u = users[msg.chat.id] = users.get(msg.chat.id, User(msg, bot, fsort))
    for k, v in u.shop.items():
        item = [f'{ki} = {vi}' for ki, vi in v.items()if vi>0]
        if not item:continue
        txt = '\n'.join([k, *item])
        board = [['удалить', 'добавить'], 2]
        await msg.answer(text=txt, reply_markup=get_keyboard(*board))
    txt = 'корзина'
    if not u.shop:
        txt += '\nздесь ничего нет...'
    await msg.answer(text=txt, reply_markup=get_keyboard(['заказать', 'удалить'], 2))

# УДАЛЕНИЕ #
async def delpack(bot, msg, ds=None):
    u = users[msg.chat.id] = users.get(msg.chat.id, User(msg, bot, fsort))

    f, *m = msg.text.split('\n')
    if f.lower() == 'корзина':
        u.shop = {}
    else:
        u.shop.pop(f, None)
    await bot.edit_message_text(chat_id=msg.chat.id,
                            text='DELETED',
                            message_id=msg.message_id)

# ЗАКАЗ #
async def ordpack(bot, msg, ds=None):
    path = os.path.join(os.getcwd(), 'orders')
    if not os.path.exists(path):
        os.makedirs(path)

    u = users[msg.chat.id] = users.get(msg.chat.id, User(msg, bot, fsort))

    conv = {}
    for k, v in u.shop.items():
        for x, y in v.items():
            conv[x] = {**conv.get(x, {}), **{k:y}}

    df = pd.DataFrame.from_dict(conv)

    """ with open(os.path.join(path, f'{msg.chat.id}.txt'), 'w', encoding='utf=8')as op:
        op.write(df.to_string(justify='center', index=True))
    with open(os.path.join(path, f'{msg.chat.id}.mark'), 'w', encoding='utf=8')as op:
        op.write(df.to_markdown()) """

    with open(os.path.join(path, f'{msg.chat.id}.tab'), 'w', encoding='utf=8')as op:
        op.write(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

    # ОТПРАВЛЕНИЕ ЗАКАЗА
    with open(os.path.join(path, f'{msg.chat.id}.tab'), 'rb')as op:
        #print(op)
        try:
            await bot.send_document(1450362049, op)
            txt = 'принято...'
        except:
            txt = 'корзина пустая!'
        await bot.edit_message_text(chat_id=msg.chat.id,
                        text=txt,
                        message_id=msg.message_id)



    # обнулить корзину
    u.shop = {}
    for k in u.vals:
        for i in u.vals[k]:
            u.vals[k][i] = 0