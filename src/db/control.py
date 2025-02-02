#   ___  ____  __  __        ____ _
#  / _ \|  _ \|  \/  |      / ___| | __ _ ___ ___  ___  ___
# | | | | |_) | |\/| |_____| |   | |/ _` / __/ __|/ _ \/ __|
# | |_| |  _ <| |  | |_____| |___| | (_| \__ \__ \  __/\__ \
#  \___/|_| \_\_|  |_|      \____|_|\__,_|___/___/\___||___/
#

from db.models import Users, Posts
from db.core import async_session_factory
from schemas import UserReg, Login, UserFToken, Token, CreatePost, AvatarHash, LiteUser, ChangePass, MyBaseInfo, Post, ChangePost
from sqlalchemy import select, delete
from security import Hashing, JwT
from db import Errs
from fastapi import HTTPException
import exceptions
from datetime import datetime, timedelta, timezone
from typing import List
from storage.fs import ImageFS
from db.controlExt.UserProfileExt import UserProfileExt


def page_offset_calculation(page: int) -> int: # offset calculation for paging
    """
    Расчет смещения для страницы.
    Принимает номер страницы атрибутом page
    
    Возращает смещение как int
    """
    if page <= 0:
        raise exceptions.PageLessZero
    return ((page * 5) - 5)


class UserORM(UserProfileExt):
    """
    Главный класс для работы с пользователями
    """
    @staticmethod
    async def UserAdd(user: UserReg) -> str:
        """
        Создание пользователя.
        На вход принимает объект user из schemas.UserReg

        Такого вида:
            nickname: str
            email: EmailStr
            password: str
        
        Возращает токен или ошибку.
        P.S Токен возращает в формате строки
        """
        
        user.password = Hashing.create_hash(user.password) # Создание хеша
        Usr = Users(nickname=user.nickname, email=user.email.strip(), password=user.password) # Создание экземпляра User-а
        async with async_session_factory() as session:

            query = select(Users).filter(Users.email==user.email.strip())
            result = await session.execute(query) # Пытается найти пользователя с таким же email
            if result.fetchall() != []:
                await session.rollback() # Если находит то откатывает транзакцию и выплёвывает ошибку
                raise Errs.UserAlreadyCreate()
            else:
                session.add(Usr) # иначе добавляет юзера в базу
                await session.commit()
                user_get = await session.execute(select(Users).filter_by(email=user.email.strip()))
                user_get = user_get.scalars().first()
                return JwT.generateJWT(UserFToken(
                    id=user_get.id, email=user.email,
                    expires_at=(datetime.now(timezone.utc) + timedelta(hours=8)))
                ) # выдаёт токен

    @staticmethod
    async def UserLogin(user: Login)-> Token:
        """
        Функция для авторизации пользователя.

        На вход принимает в качестве аттрибута user схему Login 
        с таким видом:
            email: EmailStr
            password: str

        Возращает токен как схему.
        """
        hash_password = Hashing.create_hash(user.password) # Создание хеша пароля
        async with async_session_factory() as session:
            query = select(Users).filter_by(email=user.email.strip()) # находит пользователя по email
            result = await session.execute(query)
            result = result.first()
            if result is None:
                raise Errs.UserNotFound # Если не находит пользователя вываливает ошибку
            if result[0].email == user.email: # Проверяет на соответствие ещё раз
                if result[0].password == hash_password: # Сверяет хеши
                    return JwT.generateJWT(UserFToken(
                        id=result[0].id,
                        email=user.email,
                        expires_at=(datetime.now(timezone.utc) + timedelta(hours=8)))
                    ) # выдаёт токен
                else:
                    raise HTTPException(400, "Uncorrect password!")

    @staticmethod
    async def UserAvatarChange(image_hash: AvatarHash, token: Token):
        """
        Функция для изменения(И загрузки) аватара.

        На вход принимает специальный хеш-путь в качестве аттрибута image_hash.
        А также токен в качестве схемы.

        Возращает сообщение об успехе(по сути ничего).
        """
        try:
            if not JwT.check_token_for_expire(token): # проверка токена на свежесть
                raise exceptions.TokenWasExpire

            decode = JwT.decodeJWT(token) # Декодирует его
            async with async_session_factory() as session:
                stmnt = select(Users).filter_by(id=decode.id) # Ищет юзера по id
                res = await session.execute(stmnt)
                usr = res.scalars().first()

                if not usr: # вываливает ошибку если не находит
                    raise exceptions.UserNotFound 

                if usr.avatar_path and usr.avatar_path != image_hash.image_hash:
                    try:
                        inx = ImageFS()
                        inx.DelOldAvatar(usr.avatar_path) # удаления старого аватара
                    except Exception as e:
                        print(f"WARNING!: {e}")

                usr.avatar_path = image_hash.image_hash
                await session.commit() # Добавление пути нового аватара
                return {"message": "Succesfully!"}

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


    @staticmethod
    async def GetUserAvatarHashById(id: int) -> str:
        """
        Функция для получения хеш-пути аватара
        по id.

        Принимает id пользователя, возращает хеш-путь.
        """
        async with async_session_factory() as session:
            stmnt = select(Users).filter_by(id=id) # Находит юзера по id
            res = await session.execute(stmnt)
            res = res.scalars().first()
            if res is None:
                raise exceptions.UserNotFound
            return res.avatar_path # Отдаёт хеш-путь из базы

    @staticmethod
    async def GetUserById(id: int) -> LiteUser:
        """
        DEPRECATED!

        Функция для получения имени по id.
        Вход:
            id: int
        Выход:
            id: int
            nickname: str
        """
        async with async_session_factory() as session:
            stmnt = select(Users).filter_by(id=id) 
            res = await session.execute(stmnt)
            res = res.scalars().first()
            if res is None:
                raise exceptions.UserNotFound
            return LiteUser(id=id, nickname=res.nickname)
        
    @staticmethod
    async def ChangePassword(data: ChangePass):
        """
        Функция для смены пароля у пользователя.

        На вход принимает схему ChangePass:
            old_password: str
            new_password: str
            token: str
        """
        old_hash_password = Hashing.create_hash(data.old_password.strip())
        new_hash_password = Hashing.create_hash(data.new_password.strip()) # Создание хешей паролей
        decoded_token = JwT.decodeJWT(Token(token=data.token)) # Декодирование токена
        async with async_session_factory() as session:
            await session.begin()
            query = select(Users).filter_by(email=decoded_token.email) # Находит юзера по email
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None: # Если не находит то выдаёт ошибку
                raise exceptions.UserNotFound
            if result.email == decoded_token.email: # Дополнительно сравнивает почты
                if result.password == old_hash_password: # Сравнивает пароль в базе и старый пароль что прислал юзер 
                    result.password = new_hash_password # В случае если все правильно
                    await session.commit() # Присваивает новый пароль и делает коммит

    @staticmethod
    async def GetMyInfo(token: Token) -> MyBaseInfo:
        """
        Функция для получения базовой информации о себе.
        Принимает токен как схему.

        Возращает схему MyBaseInfo:
            id: int
            email: EmailStr
            nickname: str
        """
        decoded_token = JwT.decodeJWT(token=token) # Декодирование токена
        if not JwT.check_for_expire(decoded_token.expires_at): 
            raise exceptions.TokenWasExpire
        async with async_session_factory() as session:
            query = select(Users).filter_by(id=decoded_token.id) # получает юзера по id
            result = await session.execute(query)
            result = result.scalars().first()
            return MyBaseInfo( # Достает информацию из юзера и возращает её
                id=result.id,
                email=result.email,
                nickname=result.nickname
            )




class PostORM:
    """
    Главный класс для работы с постами
    """
    @staticmethod
    async def AddPost(post: CreatePost):
        """
        Функция для добавления поста.
        На вход принимает схему CreatePost:
            title: str
            text: str
            created_at: datetime = datetime.now(timezone.utc) #Время задаётся автоматически его не надо указывать.
            token: Token

        Возращает сообщение об успехе.
        """
        decoded_token = JwT.decodeJWT(post.token) # декодирование токена
        if JwT.check_for_expire(decoded_token.expires_at):
            async with async_session_factory() as session:
                query = select(Users).filter_by(id=decoded_token.id) # находит юзера по id
                result = await session.execute(query)
                author = result.first()[0] # получает экземпляр user-а

                stmnt = Posts(
                    title=post.title,
                    text=post.text,
                    author=author,
                    created_at=post.created_at
                ) # Создание экземпляра поста
                session.add(stmnt)
                await session.commit() # коммит
                return "Successfully!"
        else:
            raise exceptions.TokenWasExpire
        
    @staticmethod
    async def GetLastTenPosts() -> List[Post]:
        """
        Получение 10-ти последних постов.
        Используется для домашней страницы.

        На вход ничего не принимает.
        Возращает список со схемами Post.
        """
        async with async_session_factory() as session:
            stmnt = select(Posts).order_by(Posts.created_at.desc()).limit(10)
            result = await session.execute(stmnt) # получение 10-ти последних постов
            result = result.scalars().all()
            if result == []: # Ошибка если посты не найдены 0_o
                raise exceptions.PostsNotFound 

            final = [] 
            for i in result: # перебор всех постов и добавление в чистый список
                # Это нужно чтобы подтянуть никнейм автора
                await session.refresh(i, attribute_names=['author']) # подтягиваем данные автора
                username = i.author.nickname # получаем никнейм

                final.append(
                    Post( # Создаём схему поста и добавляем её в список
                        id=i.id,
                        title=i.title,
                        text=i.text,
                        created_at=i.created_at,
                        author_id=i.author_id,
                        author_name=username
                    )
                )
            return final

    @staticmethod
    async def GetLastPagePosts(page: int) -> List[Post]:
        """
        Функция для получения последних постов по страницам.

        На вход принимает страницу
            page: int
        На выход отдаёт список со схемами постов.
            List[Post]
        """
        offset = page_offset_calculation(page)
        async with async_session_factory() as session:
            stmnt = select(Posts).order_by(Posts.created_at.desc()).offset(offset=offset).limit(20) 
            result = await session.execute(stmnt) # Сложный запрос на получения 20 постов по страницам
            result = result.scalars().all()
            if result == []: # Ошибка если посты не найдены
                raise exceptions.PostsNotFound
            final = []
            for i in result:
                await session.refresh(i, attribute_names=["author"]) # подтягиваем данные автора
                username = i.author.nickname
                final.append(
                    Post( # Создаём схему поста и добавляем её в список
                        id=i.id,
                        title=i.title,
                        text=i.text,
                        created_at=i.created_at,
                        author_id=i.author_id,
                        author_name=username
                    )
                )
            return final
    
    @staticmethod
    async def GetPostById(id: int) -> Post:
        """
        Получение поста по id.
        
        Даже добавить нечего.
        """
        async with async_session_factory() as session:
            stmnt = select(Posts).filter_by(id=id) 
            res = await session.execute(stmnt) # получает пост по id
            result = res.scalars().first()
            if result == None:
                raise exceptions.PostNotFound
            await session.refresh(result, attribute_names=['author']) # подтягиваем данные автора
            username = result.author.nickname
            return Post( # создаём схему поста и возращаем
                id=result.id,
                title=result.title,
                text=result.text,
                created_at=result.created_at,
                author_id=result.author_id,
                author_name=username,
            )
        
    @staticmethod
    async def DeletePostByID(post_id: int):
        """
        Удаление поста по id
        """
        async with async_session_factory() as session:
            query = delete(Posts).where(Posts.id == post_id)
            res = await session.execute(query)
            await session.commit()
            return res

    @staticmethod
    async def ChangePost(data: ChangePost):
        try:
            decoded_token = JwT.decodeJWT(Token(token=data.token))
            if not JwT.check_for_expire(decoded_token.expires_at):
                raise exceptions.TokenWasExpire
            async with async_session_factory() as session:
                stmnt = select(Posts).filter_by(id=data.post_id)
                res = await session.execute(stmnt)
                res = res.scalar_one()  
                if not res:
                    raise exceptions.PostNotFound
                if decoded_token.id != res.author_id:
                    raise exceptions.IsNotYourPost
                else:
                    res.text = data.text
                    res.title = data.title
                    await session.commit()
                    return {"message": "Succesfully!"}
        except Exception as e:
            print(e)
            raise e

