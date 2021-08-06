
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'f6b11596869c2c7caf7420af7a456e7f52e82faf56a6d5fe17964666c48dea82f1beefa2f7ed9b05e67f0'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': 1388348, 'message': "Хули блядь?",  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")