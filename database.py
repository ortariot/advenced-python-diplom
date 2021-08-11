import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy.sql.expression import insert
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, ForeignKey, PrimaryKeyConstraint, select, func
from sqlalchemy.sql.sqltypes import Boolean


class VkinderAppDb():
    def __init__(self, su_name, su_pass, usr_name, usr_pass,
                 db_allready_exist=True):
        if db_allready_exist is False:
            self._db_create(su_name, su_pass, 'vkinder',
                            usr_name, usr_pass)

        db = f"postgresql://{usr_name}:{usr_pass}@localhost:5432/{'vkinder'}"
        self.engine = create_engine(db)
        self.metadata = MetaData()
        self._table_create()

        if db_allready_exist is False:
            self.metadata.create_all(self.engine)

    def _db_create(self, su_name, su_pass, db_name, u_name, u_pass):
        connection = psycopg2.connect(user=su_name, password=su_pass)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f'CREATE DATABASE {db_name}')
        cursor.execute(f"CREATE USER {u_name} WITH PASSWORD '{u_pass}'")
        cursor.execute(f"ALTER DATABASE {db_name} OWNER TO {u_name}")
        cursor.close()
        connection.close()

    def _table_create(self):
        self.users = Table("Users", self.metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('vk_id', String(255), nullable=False)
                           )

        self.profile = Table("Profile", self.metadata,
                             Column('id', Integer(), primary_key=True),
                             Column('vk_id', String(255), nullable=False),
                             Column('favorite', Boolean()),
                             Column('blacklist', Boolean())
                             )

        self.users_profile = Table("UserProfile", self.metadata,
                                   Column('user_id', ForeignKey('Users.id')),
                                   Column('profile_id',
                                          ForeignKey('Profile.id')),
                                   PrimaryKeyConstraint('user_id',
                                                        'profile_id',
                                                        name='pk_usr_prof'
                                                        )
                                   )

    def ins_to_table(self, table, data):
        connection = self.engine.connect()
        connection.execute(insert(table), data)
        filter = func.max(table.c.id)
        sel_last_id = select(filter)
        last_id = connection.execute(sel_last_id).fetchone()[0]
        connection.close()
        return last_id

    def load_users(self, vk_id):
        connection = self.engine.connect()
        sel_id = select(self.users).where(self.users.c.id == vk_id)
        out = connection.execute(sel_id).fetchone()
        connection.close()
        if out:
            last_id = out.id
        else:
            data = {'vk_id': vk_id}
            last_id = self.ins_to_table(self.users, data)
        return last_id

    def load_profile(self, vk_id: str, favorite: bool, blaklist: bool) -> int:
        connection = self.engine.connect()
        sel_id = select(self.users).where(self.users.c.id == vk_id)
        out = connection.execute(sel_id).fetchone()
        connection.close()
        if out:
            last_id = out.id
        else:
            data = {'vk_id': vk_id,
                    'favorite': favorite,
                    'blaklist': blaklist
                    }
            last_id = self.ins_to_table(self.profile, data)
        return last_id

    def load_users_profile(self, user_id, profile_id):
        users_profile_data = {'user_id': user_id, 'profile_id': profile_id}
        connection = self.engine.connect()
        connection.execute(insert(self.users_profile), users_profile_data)

    def get_profile_list(self, user_vk_id):
        sel = select(self.profile.c.vk_id
                     ).select_from(self.profile
                                   .join(self.users_profile)
                                   .join(self.users)
                                   ).where(self.users.c.vk_id == str(user_vk_id))
        conntion = self.engine.connect()
        out = conntion.execute(sel)
        conntion.close()
        return [i[0] for i in out.fetchall()]

if __name__ == '__main__':
    database = VkinderAppDb('postgres', 'postgres',
                            'vkinder', 'vkinder')
