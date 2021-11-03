from peewee import Model, CharField, AutoField, SqliteDatabase

db = SqliteDatabase('database.db')
db.connect()


class User(Model):
    id = AutoField(primary_key=True, null=False)
    username = CharField()
    password = CharField()
    email = CharField()
    birth_date = CharField()
    profile_picture = CharField()

    class Meta:
        database = db


db.create_tables([User])
