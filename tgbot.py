import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def notify__progress(secs_left, seconds, answer):
    pbar = render_progressbar(seconds, seconds - secs_left)
    text = "Осталось секунд: {}\n{}".format(secs_left, pbar)
    bot.update_message(TG_CHAT_ID, answer, text)


def time(TG_CHAT_ID, text):
    seconds = 0
    seconds = parse(text)
    answer = bot.send_message(TG_CHAT_ID, "Таймер запущен...")
    bot.create_countdown(seconds, notify__progress, seconds=seconds, answer=answer)
    bot.create_timer(seconds, choose)


def choose():
    message = "Время вышло!"
    bot.send_message(TG_CHAT_ID, message)


def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == '__main__':
    load_dotenv()
    TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    bot = ptbot.Bot(TG_TOKEN)

    bot.reply_on_message(time)
    bot.run_bot()
