import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


load_dotenv()
tg_token = os.getenv("TELEGRAM_TOKEN")
tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")


def main():
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, text: time(chat_id, text, bot))
    bot.run_bot()


def notify__progress(secs_left, seconds, answer, bot):
    pbar = render_progressbar(seconds, seconds - secs_left)
    text = "Осталось секунд: {}\n{}".format(secs_left, pbar)
    bot.update_message(tg_chat_id, answer, text)


def time(tg_chat_id, text, bot):
    seconds = 0
    seconds = parse(text)
    answer = bot.send_message(tg_chat_id, "Таймер запущен...")
    bot.create_countdown(
        seconds,
        notify__progress,
        seconds=seconds,
        answer=answer,
        bot=bot,
    )
    bot.create_timer(seconds, choose, bot=bot)


def choose(bot):
    message = "Время вышло!"
    bot.send_message(tg_chat_id, message)


def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == '__main__':
    main()
