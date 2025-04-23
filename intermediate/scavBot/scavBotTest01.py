####################################################################################################
#Nicholas Dubs
#Scavenger Bot
#Induction 2025
#Test 01
#04/01/2025
####################################################################################################
import telebot
import time
bot = telebot.TeleBot("7293156317:AAE7miyzvDsANHYkQqSBiUisRj_G2PnCD90", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello goog mornging")
    print("User: " + message.text)
    
@bot.message_handler(commands=['search'])
def search(message):
    words = message.text.split()
    if len(words) > 1:
        bot.reply_to(message, "searching for " + words[1])
        if words[1] == "jon":
            bot.reply_to(message, "jon is a cool guy")
        elif words[1] == "nicholas":
            bot.reply_to(message, "nicholas is a cooler guy")
        else:
            bot.reply_to(message, "I don't know what " + words[1] + " is")
    else:
        bot.reply_to(message, "use search followed by a word")

@bot.message_handler(func=lambda message: message.text == "🫡")
def clue1(message):
    bot.reply_to(message, "ask me to play a sound")
    print("User: " + message.text)
@bot.message_handler(func=lambda message: "sound" in message.text.lower() or "audio" in message.text.lower() or "play" in message.text.lower())
def play_sound(message):
    with open("sound.mp3", "rb") as audio:
        bot.send_audio(message.chat.id, audio,"Birbs")
    print("User: " + message.text)

@bot.message_handler(func=lambda message: message.text == "block")
def sendimage(message):
    with open("clue1.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    print("User: " + message.text)

@bot.message_handler(func=lambda message: message.text == "exercise")
def sendvideo(message):
    with open("clue2.mp4", "rb") as video:
        bot.send_video(message.chat.id, video)
    print("User: " + message.text)

bot.infinity_polling()