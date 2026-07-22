from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, ContextTypes


class To_do:
    def __init__(self):
        self.list1=[]
        self.amount=0
    def add(self,exersice):
        self.list1.append(exersice)
        self.amount+=1
        return "Задание успешно добавлено"

    def remove(self, number):
        if 1 <= number <= len(self.list1):
            self.list1.pop(number - 1)
            self.amount -= 1
            return "Задание успешно удалено"
        else:
            return "Ошибка: задачи с таким номером нет!"

    def removeAll(self):
        self.list1.clear()
        self.amount=0
        return "Список полностью очищен"

    def show(self):
        if self.amount == 0:
            return 'Список пуст'
        s=''
        for i in range(self.amount):
            s+=str(i+1)+'. '+self.list1[i]+"\n"
        return s
    #def create(self, exersice):
        #self.list1.append(exersice)

todo=To_do()

async def start(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(  "Привет! Я твой список дел.\n"
        "Команды:\n"
        "/add <задача> - добавить задачу\n"
        "/show - показать все задачи\n"
        "/remove <номер> - удалить задачу по номеру\n"
        "/clear - очистить весь список")

async def add(update: Update , context: ContextTypes.DEFAULT_TYPE):
    text=' '.join(context.args)
    if not text:
        await update.message.reply_text("Напиши задачу после /add. Например: /add Сделать уроки")
        return
    todo.add(text)
    await update.message.reply_text("Добавлено: "+ text)

async def show(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(todo.show())

async def remove(update: Update , context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши номер задачи, например /remove 1")
        return
    try:
        number=int(context.args[0])
        res=todo.remove(number)
        await update.message.reply_text(res)

    except ValueError:
        await update.message.reply_text("Ошибка: Нужно ввести число.")


async def clear(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(todo.removeAll())

if __name__ == "__main__":
    Token='' #вставить ваш токен
    app=ApplicationBuilder().token(Token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler('show', show))
    app.add_handler(CommandHandler('remove', remove))
    app.add_handler(CommandHandler('clear', clear))

    print("Бот удачно запущен")
    app.run_polling()