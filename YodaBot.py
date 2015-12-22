from telegram import Updater
import random
import re
from bs4 import BeautifulSoup
import requests
import urllib2
import os


def main():
    updater = Updater(token='158296194:AAETUoB_u4YGPSfj-4VCS749p9GgxFp8CLo')
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('biography', biography)
    dispatcher.addTelegramCommandHandler('photo', get_image)
    dispatcher.addTelegramMessageHandler(echo)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    updater.start_polling()


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Hello, please, talk to me! And it will be rephrased by me. "
                         "\n *And also, can you read biography my by using \"/biography\" command."
                         "\n *And also, can you see random my photo by using \"/photo\" command."
                         "\n (last feature doesn't work properly)")


def transform(text):
    text = text.lower()
    answer = ""
    sentenceEnders = re.compile('[.?!;:]')
    sentences = sentenceEnders.split(text)
    for sentence in sentences:
        answer_sentence = ""
        words = sentence.split()
        for i in range(len(words) - 1):
            if len(words[i]) < 3 and len(words[i]) > 0:
                words[i] += " " + words[i + 1]
                words[i + 1] = ""
        for i in range(len(words) - 1):
            if random.randint(0, 2) > 0:
                words[i], words[i + 1] = words[i + 1], words[i]
            answer_sentence += words[i] + " "
        answer_sentence += words[len(words) - 1] + ". "
        answer += answer_sentence.capitalize()
    return answer


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=transform(update.message.text))


def biography(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="http://starwars.wikia.com/wiki/Yoda")


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, this command seems to be unknown to me.")
    start(bot, update)


def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)))


def get_image(bot, update):
    image_type = "Action"
    # you can change the query for the image  here
    query = "Yoda"
    url = url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    soup = get_soup(url, header)
    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
    # print images
    img = images[random.randint(0, len(images))]
    raw_img = urllib2.urlopen(img).read()
    f = open('photo.jpg', 'wb')
    f.write(raw_img)
    f.close()
    f = open('photo.jpg', 'rb')
    response = requests.post(img, files=f)
    bot.sendChatAction(chat_id=update.message.chat_id, action='upload_photo')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=response, reply_to_message_id=update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text="Done.")
    f.close()


if __name__ == '__main__':
    main()
