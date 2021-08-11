from vkbottle import KeyboardButtonColor, Text


def keyboard_init(keyboard_bank):
    keyboard_bank['start_keyboard'].add(Text('Поиск по параметрам',
                                             payload={"command": 'manual'}
                                             )
                                        )
    keyboard_bank['start_keyboard'].row()
    keyboard_bank['start_keyboard'].add(Text('Найди какого-то для меня',
                                             payload={"command": 'smart'}
                                             ),
                                        color=KeyboardButtonColor.POSITIVE
                                        )
    keyboard_bank['start_keyboard'].row()
    keyboard_bank['start_keyboard'].add(Text('Для сына мамкиной подруги',
                                             payload={"command": 'son'}
                                             ),
                                        color=KeyboardButtonColor.PRIMARY
                                        )
    keyboard_bank['gender_choise'].add(Text("мужчина",
                                            payload={"command": '2'}
                                            )
                                       )
    keyboard_bank['gender_choise'].add(Text("женщина",
                                            payload={"command": '1'}
                                            )
                                       )
    keyboard_bank['status_choise-1'].add(Text("не замужем",
                                              payload={"command": "single"}
                                              )
                                         )
    keyboard_bank['status_choise-1'].add(Text("встречается",
                                              payload={"command": "meets"}))
    keyboard_bank['status_choise-1'].row()
    keyboard_bank['status_choise-1'].add(Text("помолвлена",
                                              payload={"command": "engaged"}))
    keyboard_bank['status_choise-1'].add(Text("замужем",
                                              payload={"command": "married"}))
    keyboard_bank['status_choise-1'].row()
    keyboard_bank['status_choise-1'].add(Text("всё сложно",
                                              payload={"command": "complicated"}))
    keyboard_bank['status_choise-1'].add(Text("в активном поиске",
                                              payload={"command": "search"}))
    keyboard_bank['status_choise-1'].row()
    keyboard_bank['status_choise-1'].add(Text("влюблена",
                                              payload={"command": "in love"}))
    keyboard_bank['status_choise-1'].add(Text("в гражданском браке",
                                              payload={"command": "civil marriage"}))

    keyboard_bank['status_choise-2'].add(Text("не женат",
                                              payload={"command": "single"}))
    keyboard_bank['status_choise-2'].add(Text("встречается",
                                              payload={"command": "meets"}))
    keyboard_bank['status_choise-2'].row()
    keyboard_bank['status_choise-2'].add(Text("помолвлен",
                                              payload={"command": "engaged"}))
    keyboard_bank['status_choise-2'].add(Text("женат",
                                         payload={"command": "married"}))
    keyboard_bank['status_choise-2'].row()
    keyboard_bank['status_choise-2'].add(Text("всё сложно",
                                         payload={"command": "complicated"}))
    keyboard_bank['status_choise-2'].add(Text("в активном поиске",
                                         payload={"command": "search"}))
    keyboard_bank['status_choise-2'].row()
    keyboard_bank['status_choise-2'].add(Text("влюблен",
                                         payload={"command": "in love"}))
    keyboard_bank['status_choise-2'].add(Text("в гражданском браке",
                                         payload={"command": "civil marriage"})
                                         )

    keyboard_bank['end_keyboard'].add(Text('Снвоа искать',
                                           payload={"command": 'again'}),
                                      color=KeyboardButtonColor.POSITIVE
                                      )
    keyboard_bank['end_keyboard'].row()
    keyboard_bank['end_keyboard'].add(Text('Я всех уже нашёл',
                                           payload={"command": 'end'}
                                           )
                                      )
