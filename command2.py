import aiogram.utils.markdown as mark


async def test(bot, msg):
    await msg.answer('worked!')

async def help(bot, msg):
    text = """
    <b>
    Список команд:                 
    /start       - Начать диалог   
    /catalog(каталог) - каталог    
    /shop(корзина) - корзина       
    /help        - Получить справку
    /form        - Ввод данных     
    /cancel      - Сброс           
    /test        - Тест            
    галерея - фотографии
    </b>"""
    await msg.answer(text, parse_mode="HTML")