import telebot

bot = telebot.TeleBot('8259666751:AAGEpx4tGxAZ4OzkWM7vUKmy7FXHGLMepEU')

#decorator message_handler
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Привіт!")

#bot.polling(non_stop=False)