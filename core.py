import logging, re
from decouple import config

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN', default='')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def loadWords():
    wordlist = open('wordlist.txt' ,'r').readlines()
    return wordlist

def start(update, context):
    response_message = "Olá, eu sou a Dona Guiomar, um bot que modera o uso de palavras racistas, homofóbicas e que atrapalhem o bom andamento das conversas!"
    update.message.reply_text(response_message)

def listWords(update, context):
    response_message = "Oi! Estou filtrando as seguintes palavras: " + ", ".join(WORDLIST)
    context.bot.send_message(update.message.from_user.id, response_message)

def badwords(update, context):
    response_message = "Essa mensagem não acrescenta em nada e por isso foi removida." 
    context.bot.send_message(update.message.from_user.id, response_message)
    update.message.delete()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('listWords', listWords))
    
    regex_words = r"\b(?:" + "|".join(WORDLIST) + r")\b"
    dispatcher.add_handler(MessageHandler(Filters.regex(regex_words), badwords))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    WORDLIST = [re.escape(word.strip()) for word in loadWords()]
    main()