import logging
import os
import random
from typing import Optional

from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.api import API



token = ''



api = API(token)
bot = Bot(token)

keyboard = Keyboard(one_time=True, inline=False)  # О параметрах one_time и inline вы можете прочитать в документации к апи вконтакте
keyboard.add(Text("Кнопка 1"), color=KeyboardButtonColor.POSITIVE)  # Первая строка (ряд) добавляется автоматически
keyboard.row()  # Переходим на следующую строку 
keyboard.add(Text("Кнопка 2"))
keyboard.add(Text("Кнопка 3", payload={"command": 3}))

# Logging level can be set through .basicConfig(level=LOGGING_LEVEL)
# but if you use loguru the instruction is different.
# ---
# If you use loguru you need to remove default logger and add new with
# level specified logging level, visit https://github.com/Delgan/loguru/issues/138
logging.basicConfig(level=logging.DEBUG)

# Documentation for keyboard builder > tools/keyboard
KEYBOARD = Keyboard(one_time=True).add(Text("Съесть еще", {"cmd": "eat"})).get_json()
EATABLE = ["мороженое", "макароны", "суп"]


# If you need to make handler respond for 2 different rule set you can
# use double decorator like here it is or use filters (OrFilter here)
@bot.on.message(text=["/съесть <item>", "/съесть"])
@bot.on.message(payload={"cmd": "eat"})
async def eat_handler(message: Message, item: Optional[str] = None):
    print('hand')
    if item is None:
        item = random.choice(EATABLE)
    await message.answer(f"Ты съел <<{item}>>!", keyboard=KEYBOARD)

@bot.on.message(lev="/инфо")  # lev > custom_rule from LevensteinRule
async def info(message: Message):
    current_group = (await message.ctx_api.groups.get_by_id())[0]
    await message.answer(f"Название моей группы: {current_group.name}", keyboard=keyboard.get_json())
    usr_id = message.from_id
    print(await api.request("users.get", {'user_id': usr_id,
                                          'fields': 'verified,photo_50,bdate,about'
                                          })) 
   


# You can use raw_event to handle any event type, the advantage is
# free dataclass, for example it can be dict if you have some problems
# with module types quality
@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:

        # Basic API call, please notice that bot.api (or blueprint.api) is
        # not accessible in case multibot is used, API can be accessed from
        # event.ctx_api
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Спасибо за подписку!", random_id=0
        )

    # Read more about exception handling in documentation
    # low-level/exception_factory/exception_factory
    except VKAPIError(901):
        pass


# Runs loop > loop.run_forever() > with tasks created in loop_wrapper before,
# read the loop wrapper documentation to comprehend this > tools/loop-wrapper.
# The main polling task for bot is bot.run_polling()
bot.run_forever()



# from vkbottle.bot import Bot, Message

# bot = Bot(token=token)

# @bot.on.message()
# async def hi_handler(message: Message):
#     # users_info = await bot.api.users.get(message.from_id)
#     await message.answer("Хуй пиздец")

# bot.run_forever()