from peewee import Model, CharField, AutoField, SqliteDatabase, DateTimeField, ForeignKeyField

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


class Group(Model):
    id = AutoField(primary_key=True, null=False)
    name = CharField()
    group_profile = CharField()
    group_banner = CharField()
    detail = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db


class Post(Model):
    id = AutoField(primary_key=True, null=False)
    content = CharField()
    owner_id = ForeignKeyField(User)
    group_id = ForeignKeyField(Group)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        database = db


class Comment(Model):
    id = AutoField(primary_key=True, null=False)
    post_id = ForeignKeyField(Post)
    content = CharField()
    owner_id = ForeignKeyField(User)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        database = db


class GroupMember(Model):
    group = ForeignKeyField(Group, on_delete=True)
    member = ForeignKeyField(User, on_delete=True)

    class Meta:
        database = db


class PostLike(Model):
    post = ForeignKeyField(Post, on_delete=True)
    user = ForeignKeyField(User, on_delete=True)

    class Meta:
        database = db


db.create_tables([User, Group, Post, Comment, GroupMember, PostLike])
