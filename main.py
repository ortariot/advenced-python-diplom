import logging
from vkbottle.bot import Bot, Message
from vkbottle import BaseStateGroup, GroupEventType,\
                     GroupTypes, Keyboard, VKAPIError
from vk_simple_api import VkSimpleApi
from kinderboad import keyboard_init

logging.basicConfig(level=logging.INFO)

KEYBOARD_BANK = {'start_keyboard': Keyboard(one_time=True, inline=False),
                 'gender_choise': Keyboard(one_time=True, inline=False),
                 'status_choise-1': Keyboard(one_time=True, inline=False),
                 'status_choise-2': Keyboard(one_time=True, inline=False),
                 'end_keyboard': Keyboard(one_time=True, inline=False)
                 }


class MenuState(BaseStateGroup):
    GENDER = 1
    STATUS = 2
    ID = 3
    AGE = 4
    CITY = 5
    END = 6
    TYPE = 7


class VKinderInterface():
    search_parameter = {'gender': None,
                        'age_from': None,
                        'age_to': None,
                        'city': None,
                        'status': None,
                        'user_id': None
                        }

    def __init__(self, api, bot):
        self.api = api
        self.bot = bot

    async def push_search(self, message):
        await message.answer('Я начинаю поиск, это займёт некоторое время:',)
        users = await self.api.user_search(self.search_parameter['gender'],
                                           self.search_parameter['age_from'],
                                           self.search_parameter['age_to'],
                                           self.search_parameter['city'],
                                           self.search_parameter['status'],
                                           self.search_parameter['user_id']
                                           )
        await message.answer(f'По твоему запросу найдено {len(users)} анкет:')

        for profile in users:
            await message.answer(f"{profile['name']} - {profile['link']}")
            for p_id in profile['photo_id']:
                await message.answer(attachment=f"photo{profile['id']}_{p_id}")

        self.search_parameter.clear()
        await message.answer('Это все кого я нашёл, чем займёмся теперь?',
                             keyboard=KEYBOARD_BANK['end_keyboard']
                             )
        await self.bot.state_dispenser.set(message.peer_id, MenuState.END)

    async def auto_parameters(self, message, id=None):
        if id:
            params = await self.api.user_get(id)
        else:
            params = await self.api.user_get(message.from_id)

        self.search_parameter = params[0]
        await message.answer((f"Будем искать для {params[1]['first_name']}"
                              f" {params[1]['last_name']} {params[1]['url']}"
                              ))
        if None in self.search_parameter.values():
            await message.answer(("Мне не хватает информации для поиска"
                                 " Давай разбеёмся с этим"
                                  )
                                 )
        await self.gender_chose(message)

    async def group_invite(self, event):
        try:
            await self.bot.api.messages.send(peer_id=event.object.user_id,
                           message=("Привет! Спасибо за подписку!"
                                    " Я бот способный подбирать интересных"
                                    " собеседников по твоим предпочтениям"
                                    ", если ты понимаешь о чём я говорю :-)"
                                    " Могу найти кого-то для тебя, для "
                                    "сына мамкиной подруги или давай поищем "
                                    "по заданным параметрам. Выбирать тебе."
                                    ),
                           random_id=0,
                           keyboard=KEYBOARD_BANK['start_keyboard'].get_json()
                           )
            await self.bot.state_dispenser.set(event.object.user_id, MenuState.TYPE)
        except VKAPIError(901):
            pass

    async def hello(self, message):
        await message.answer(("Привет! Рад встрече!"
                              " Я бот способный подбирать интересных"
                              " собеседников по твоим предпочтениям"
                              ", если ты понимаешь о чём я говорю :-)"
                              " Могу найти кого-то для тебя, для "
                              "сына мамкиной подруги или давай поищем "
                              "по заданным параметрам. Выбирать тебе."
                              ),
                             keyboard=KEYBOARD_BANK['start_keyboard']
                             .get_json())
        await self.bot.state_dispenser.set(message.peer_id, MenuState.TYPE)

    async def gender_chose(self, message):
        if self.search_parameter.get('gender', None) is None:
            await message.answer('Отлично! Выбрем нужный пол',
                                 keyboard=KEYBOARD_BANK['gender_choise']
                                 .get_json())
            await self.bot.state_dispenser.set(message.peer_id,
                                               MenuState.GENDER)
        else:
            await self.age_chose(message)

    async def age_chose(self, message):
        if self.search_parameter.get('age_from', None) is None:
            await message.answer(('Давай определимся с возрастом '
                                  'просто пришли мне два числа разделённые'
                                  ' пробелом, и я буду искать в диапазоне'
                                  ' между ними'),
                                 )
            await self.bot.state_dispenser.set(message.peer_id, MenuState.AGE)
        else:
            await self.city_chose(message)

    async def city_chose(self, message):
        if self.search_parameter.get('city', None) is None:
            await message.answer(('Отлично! В каком городе будем искать?'
                                  ' Пришли мне в сообщение название города'
                                  )
                                 )
            await self.bot.state_dispenser.set(message.peer_id, MenuState.CITY)
        else:
            await self.status_chose(message)

    async def status_chose(self, message):
        if self.search_parameter.get('status', None) is None:
            await message.answer(('И теперь самое сложное.'
                                 'Выберете статус искомых анкет'
                                  ),
                                 keyboard=KEYBOARD_BANK[f"status_choise-{self.search_parameter.get('gender', 'femail')}"
                                                        ].get_json()
                                 )
            await self.bot.state_dispenser.set(message.peer_id,
                                               MenuState.STATUS
                                               )
        else:
            await self.push_search(message)

    async def again(self, message):
        await message.answer(("Уважаю твой выбор, как ищем на сей раз?"),
                             keyboard=KEYBOARD_BANK['start_keyboard'
                                                    ].get_json()
                             )

    async def goodby(self, message):
        await message.answer(("Хорошо, не трать себя впустую "
                              "если понадоблюсь, я здесь, просто дай знать"
                              " как мне искать"),
                             keyboard=KEYBOARD_BANK['start_keyboard'
                                                    ].get_json()
                             )

    async def search_for_any_id(self, message):
        await message.answer("Напомни мне id.")
        await self.bot.state_dispenser.set(message.peer_id, MenuState.ID)


if __name__ == '__main__':
    token = 'f6b11596869c2c7caf7420af7a456e7f52e82faf56a6d5fe17964666c48dea82f1beefa2f7ed9b05e67f0'
    app_token = 'b96ddcc35240f5643e49604ca80cee4209a5be8741c7087034418a43aefe1f3a4ea9efdc2c7960277a3ff'

    bot = Bot(token)
    api = VkSimpleApi(app_token)
    interface = VKinderInterface(api, bot)
    keyboard_init(KEYBOARD_BANK)

    @bot.on.raw_event(GroupEventType.GROUP_JOIN,
                      dataclass=GroupTypes.GroupJoin)
    async def group_join_handler(event: GroupTypes.GroupJoin):
        await interface.group_invite(event)

    @bot.on.message(text=['Найди какого-то для меня'])
    @bot.on.message(state=MenuState.TYPE, payload={"command": 'smart'})
    async def info(message: Message):
        await interface.auto_parameters(message)

    @bot.on.message(text=['Поиск по параметрам'])
    @bot.on.message(state=MenuState.TYPE, payload={"command": 'manual'})
    async def gender_choise_in(message: Message):
        interface.search_parameter['user_id'] = message.from_id
        await interface.gender_chose(message)

    @bot.on.message(text=['Для сына мамкиной подруги'])
    @bot.on.message(state=MenuState.TYPE, payload={"command": 'son'})
    async def search_by_id(message: Message):
        await interface.search_for_any_id(message)

    @bot.on.message(state=MenuState.GENDER, payload_map=[("command", str)])
    @bot.on.message(payload={"command": '/mail', "cmd": '/femail'})
    async def gender_choise_acc(message: Message):
        interface.search_parameter['gender'] \
            = int(message.get_payload_json()['command'])
        await interface.age_chose(message)

    @bot.on.message(state=MenuState.STATUS, payload_map=[("command", str)])
    async def chose_status(message: Message):
        interface.search_parameter['status'] = message.get_payload_json()['command']
        await bot.state_dispenser.delete(message.peer_id)
        await interface.push_search(message)

    @bot.on.message(text=["Снова искать"])
    @bot.on.message(state=MenuState.END, payload={"command": 'again'})
    async def searching_again(message: Message):
        await interface.again(message)

    @bot.on.message(text=['Я всех уже нашёл'])
    @bot.on.message(state=MenuState.END, payload={"command": 'end'})
    async def goobay(message: Message):
        await interface.goodby(message)

    @bot.on.message(state=MenuState.ID)
    async def set_user_id(message: Message):
        user_id = message.text
        await interface.auto_parameters(message, user_id)

    @bot.on.message(state=MenuState.AGE)
    async def set_age(message: Message):
        age = message.text.split(' ')
        interface.search_parameter['age_from'] = age[0] if len(age) >= 1 else 0
        interface.search_parameter['age_to'] = age[1] if len(age) >= 2 else 99
        await interface.city_chose(message)

    @bot.on.message(state=MenuState.CITY)
    async def set_city(message: Message):
        interface.search_parameter['city'] = message.text.strip()
        await interface.status_chose(message)

    @bot.on.message()
    async def other(message: Message):
        await interface.hello(message)

    bot.run_forever()
