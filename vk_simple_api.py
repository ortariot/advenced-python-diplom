from vkbottle.api import API
import time
import datetime
from database import VkinderAppDb

DATABASE_U_USER = 'vkinder'
DATABASE_U_PASS = 'vkinder'


class VkSimpleApi():
    status_enum = {'single': 1,
                   'meets': 2,
                   'engaged': 3,
                   'married': 4,
                   'complicated': 5,
                   'search': 6,
                   'in love': 7,
                   'civil marriage': 8
                   }

    def __init__(self, token):
        self.api = API(token)
        self.db = VkinderAppDb(DATABASE_U_USER, DATABASE_U_PASS)

    async def user_get(self, vk_id: str) -> dict:
        u_params = {'user_ids': vk_id,
                    'fields': 'bdate,relation,city,sex'
                    }

        year = datetime.datetime.now().year
        profile = await self.api.request('users.get', u_params)

        search_parameter = {'gender': None,
                            'age_from': None,
                            'age_to': None,
                            'status': 'search',
                            'city': None,
                            'user_id': profile['response'][0]['id']
                            }

        gender_inverter = {1: 2,
                           2: 1
                           }
        try:
            search_parameter['gender'] = gender_inverter.get(profile['response'][0]['sex'], None)
            search_parameter['age_from'] = int(year) - int(profile['response'][0]['bdate'][5:]) - 4,
            search_parameter['age_to'] = int(year) - int(profile['response'][0]['bdate'][5:]) + 4
            search_parameter['city'] = profile['response'][0]['city']['title']
        except ValueError:
            pass

        return [search_parameter,
                {'first_name': profile['response'][0]['first_name'],
                 'last_name': profile['response'][0]['last_name'],
                 'url': f'https://vk.com/id{vk_id}'
                 }
                ]

    async def user_search(self, gender: str, age_from: int, age_to: int,
                          city: str, status: str, user_id) -> dict:
        u_params = {'sort': 0,
                    'count': 1000,
                    'hometown': city,
                    'sex': gender,
                    'status': self.status_enum[status],
                    'age_from': age_from,
                    'age_to': age_to,
                    'has_photo': 1,
                    }

        profiles = await self.api.request('users.search', u_params)

        profile_list = self.db.get_profile_list(user_id)

        out_list = []
        for usr in profiles['response']['items']:
            if usr['is_closed'
                   ] is False and str(usr['id']) not in profile_list:
                out_list.append({'id': usr["id"],
                                 'link': f'https://vk.com/id{usr["id"]}',
                                 'name': usr['first_name'
                                             ] + ' ' + usr['last_name']
                                 }
                                )

            if len(out_list) == 20:
                break

        db_user_id = self.db.load_users(user_id)

        for usr in out_list:
            p_params = {'owner_id': usr['id'],
                        'album_id': 'profile',
                        'extended': 1
                        }
            usr_photos = await self.api.request('photos.get', p_params)

            db_profile_id = self.db.load_profile(usr['id'], False, False)
            self.db.load_users_profile(db_user_id, db_profile_id)

            tmp = [{'likes': photo['likes']['count'],
                    'photo_id': photo['id']
                    } for photo in usr_photos['response']['items']]

            photo_id_list = []
            for num, pos in enumerate(reversed(sorted(tmp,
                                                      key=lambda
                                                      link: link['likes']))):
                photo_id_list.append(pos['photo_id'])
                if num == 2:
                    break

            usr['photo_id'] = photo_id_list
            time.sleep(1)

        return out_list
