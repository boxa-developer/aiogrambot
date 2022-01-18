import os
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

ACCESS_TOKEN = '5056272926:AAG5qfWMQr1C6EC3kp7NxIVv9nlTaz32oXs'
bot = Bot(token=ACCESS_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("""
        b-111111-abcd \n
        kabit kiriting
    """)


@dispatcher.message_handler()
async def accept_answers(message: types.Message):
    if re.match("^[k, b]-[1-9][0-9][0-9][0-9][0-9][0-9]-*", message.text):
        ktype, key_name, keys = message.text.split('-')
        if ktype == 'k':
            create_key_file(key_name, keys)
            await message.reply('Kalitlar Tizimda Saqlandi')
        elif ktype == 'b':
            user_name = message["from"]["username"] or \
                        f'{message["from"]["first_name"]} {message["from"]["last_name"]}'
            res = check_keys(key_name, keys, user_name)
            await message.reply(res or 'Test Topilmadi!')
    else:
        await message.reply('Kiritish Shakli Xato!')


def create_key_file(key_name, answers):
    if not os.path.exists('keys'):
        os.makedirs('keys')
    with open(f"keys/test-{key_name}.txt", 'w', encoding='utf-8') as f:
        f.write(f"{answers}")


def check_keys(key_name, keys, username):
    if os.path.exists(f'keys/test-{key_name}.txt'):
        with open(f'keys/test-{key_name}.txt', 'r') as f:
            answers = f.readline()
            count = 0
            incorrect_answers = []
            if len(keys) == len(answers):
                for i in range(len(keys)):
                    if keys[i] == answers[i]:
                        count += 1
                    else:
                        incorrect_answers.append(i+1)
                return f'Username: @{username}\n'\
                       f'Natija: {count}/{len(answers)} \n' \
                       f'Kalit: {answers} \n'\
                       f'Xato Javoblar: {incorrect_answers}'
            else:
                return f'Kalitlar Soni To`gri Kelmadi!'


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
