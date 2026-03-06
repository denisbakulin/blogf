# scripts/populate_db.py
import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from passlib.context import CryptContext

from entities import (  # импортируйте ваши модели
    User, Profile, Settings, Container, ContainerType, Post,
    Comment, Reaction, ReactionType, Subscribe, JoinRequest,
    TopicOffer, TopicOfferStatus
)





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker('ru_RU')


class DatabasePopulator:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = []
        self.containers = []
        self.posts = []
        self.comments = []



    async def create_users(self, count: int = 10):
        """Создание пользователей с профилями и настройками"""
        print(f"Создание {count} пользователей...")

        for i in range(count):
            # Создаем пользователя
            user = User(
                username=fake.unique.user_name(),
                name=fake.name(),
                password=pwd_context.hash("password123"),
                is_active=random.choice([True, True, True, False]),  # 75% активных
                is_verified=random.choice([True, True, False])  # 66% верифицированных
            )
            self.session.add(user)
            await self.session.flush()  # Чтобы получить id

            # Создаем профиль (обязательная связь 1-к-1)
            profile = Profile(
                user_id=user.id,
                bio=fake.text(max_nb_chars=200) if random.random() > 0.3 else None,
                age=random.randint(18, 70) if random.random() > 0.3 else None,
                city=fake.city() if random.random() > 0.3 else None
            )
            self.session.add(profile)

            # Создаем настройки (обязательная связь 1-к-1)
            settings = Settings(
                user_id=user.id,
                show_in_search=random.choice([True, False]),
                is_profile_public=random.choice([True, True, False])  # 66% публичных
            )
            self.session.add(settings)

            self.users.append(user)

            if (i + 1) % 10 == 0:
                print(f"Создано {i + 1} пользователей")

        await self.session.commit()
        print(f"Создано {len(self.users)} пользователей с профилями и настройками")

    async def create_containers(self, count: int = 20):
        """Создание контейнеров"""
        print(f"Создание {count} контейнеров...")

        container_types = list(ContainerType)

        for i in range(count):
            author = random.choice(self.users)

            container = Container(
                title=fake.sentence(nb_words=3)[:-1],
                slug=fake.slug() if random.random() > 0.3 else None,
                description=fake.text(max_nb_chars=500) if random.random() > 0.5 else None,
                type=random.choice(container_types),
                author_id=author.id
            )
            self.session.add(container)
            await self.session.flush()
            self.containers.append(container)

        await self.session.commit()
        print(f"Создано {len(self.containers)} контейнеров")

    async def create_posts(self, count: int = 50):
        """Создание постов"""
        print(f"Создание {count} постов...")

        for i in range(count):
            author = random.choice(self.users)
            container = random.choice(self.containers)

            post = Post(
                title=fake.sentence(nb_words=6)[:-1],
                slug=fake.unique.slug(),
                content=fake.text(max_nb_chars=2000),
                allow_comments=random.choice([True, True, False]),  # 66% разрешают комментарии
                allow_reactions=random.choice([True, True, False]),
                container_id=container.id,
                author_id=1
            )
            self.session.add(post)
            await self.session.flush()
            self.posts.append(post)

        await self.session.commit()
        print(f"Создано {len(self.posts)} постов")

    async def create_comments(self, count: int = 100):
        """Создание комментариев (включая вложенные)"""
        print(f"Создание {count} комментариев...")

        # Сначала создаем корневые комментарии
        root_comments = []
        for i in range(count // 2):
            author = random.choice(self.users)
            post = random.choice(self.posts)

            if not post.allow_comments and random.random() > 0.1:
                continue  # Пропускаем посты без комментариев

            comment = Comment(
                content=fake.text(max_nb_chars=500),
                author_id=author.id,
                post_id=post.id,
                parent_id=None
            )
            self.session.add(comment)
            await self.session.flush()
            root_comments.append(comment)

        # Создаем ответы на комментарии
        for i in range(count - len(root_comments)):
            if not root_comments:
                break

            author = random.choice(self.users)
            parent = random.choice(root_comments)

            # Находим пост родительского комментария
            stmt = select(Post).where(Post.id == parent.post_id)
            post = await self.session.scalar(stmt)

            if post and not post.allow_comments:
                continue

            comment = Comment(
                content=fake.text(max_nb_chars=300),
                author_id=author.id,
                post_id=parent.post_id,
                parent_id=parent.id
            )
            self.session.add(comment)
            self.comments.append(comment)

        await self.session.commit()
        print(f"Создано комментариев: корневых - {len(root_comments)}, ответов - {len(self.comments)}")

    async def create_reactions(self, count: int = 200):
        """Создание реакций на посты и контейнеры"""
        print(f"Создание {count} реакций...")

        reaction_types = list(ReactionType)

        for i in range(count):
            user = random.choice(self.users)

            # Выбираем случайный объект для реакции (пост или контейнер)
            if random.random() > 0.7:  # 30% реакций на контейнеры
                container = random.choice(self.containers)
                reaction = Reaction(
                    user_id=user.id,
                    container_id=container.id,
                    post_id=None,
                    type=random.choice(reaction_types)
                )
            else:  # 70% реакций на посты
                post = random.choice(self.posts)
                if not post.allow_reactions:
                    continue
                reaction = Reaction(
                    user_id=user.id,
                    post_id=post.id,
                    container_id=None,
                    type=random.choice([ReactionType.LIKE, ReactionType.DISLIKE])
                )

            self.session.add(reaction)

        await self.session.commit()
        print(f"Создано {count} реакций")

    async def create_subscribes(self, count: int = 50):
        """Создание подписок на контейнеры"""
        print(f"Создание {count} подписок...")

        for i in range(count):
            user = random.choice(self.users)
            container = random.choice(self.containers)

            # Проверяем, нет ли уже такой подписки
            stmt = select(Subscribe).where(
                Subscribe.user_id == user.id,
                Subscribe.container_id == container.id
            )
            existing = await self.session.scalar(stmt)

            if not existing:
                subscribe = Subscribe(
                    user_id=1,
                    container_id=container.id
                )
                self.session.add(subscribe)

        await self.session.commit()

        # Считаем созданные подписки
        result = await self.session.execute(select(Subscribe))
        count = len(result.scalars().all())
        print(f"Создано {count} подписок")

    async def create_join_requests(self, count: int = 30):
        """Создание запросов на вступление"""
        print(f"Создание {count} запросов на вступление...")

        for i in range(count):
            user = random.choice(self.users)
            container = random.choice(self.containers)

            # Только для закрытых типов контейнеров
            if container.type not in [ContainerType.private_channel]:
                continue

            join_request = JoinRequest(
                user_id=user.id,
                container_id=container.id
            )
            self.session.add(join_request)

        await self.session.commit()
        print(f"Создано {count} запросов на вступление")

    async def create_topic_offers(self, count: int = 15):
        """Создание предложений тем"""
        print(f"Создание {count} предложений тем...")

        statuses = list(TopicOfferStatus)

        for i in range(count):
            author = random.choice(self.users)

            # Иногда предложение обработано модератором
            process_user = random.choice(self.users) if random.random() > 0.4 else None

            # Иногда предложение привело к созданию контейнера
            release_topic = random.choice(self.containers) if random.random() > 0.7 else None

            topic_offer = TopicOffer(
                title=fake.sentence(nb_words=4)[:-1],
                description=fake.text(max_nb_chars=1000),
                status=random.choice(statuses),
                author_id=author.id,
                process_user_id=process_user.id if process_user else None,
                release_topic_id=release_topic.id if release_topic else None
            )
            self.session.add(topic_offer)

        await self.session.commit()
        print(f"Создано {count} предложений тем")

    async def print_statistics(self):
        """Вывод статистики"""
        tables = [
            (User, "Пользователей"),
            (Profile, "Профилей"),
            (Settings, "Настроек"),
            (Container, "Контейнеров"),
            (Post, "Постов"),
            (Comment, "Комментариев"),
            (Reaction, "Реакций"),
            (Subscribe, "Подписок"),
            (JoinRequest, "Запросов на вступление"),
            (TopicOffer, "Предложений тем")
        ]

        print("\n" + "=" * 50)
        print("СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("=" * 50)

        for model, name in tables:
            result = await self.session.execute(select(model))
            count = len(result.scalars().all())
            print(f"{name}: {count}")

        print("=" * 50)


async def main():
    """Основная функция"""
    # Создаем движок и сессию
    from base.db import session_maker, engine


    async with session_maker() as session:
        populator = DatabasePopulator(session)

        # Очищаем базу


        # Наполняем данными
        await populator.create_users(2)  # 15 пользователей
        await populator.create_containers(25)  # 25 контейнеров
        await populator.create_posts(60)  # 60 постов
        await populator.create_comments(120)  # 120 комментариев
        await populator.create_reactions(250)  # 250 реакций
        await populator.create_subscribes(8000)  # 80 подписок
        await populator.create_join_requests(20)  # 20 запросов
        await populator.create_topic_offers(10)  # 10 предложений

        # Выводим статистику
        await populator.print_statistics()

    await engine.dispose()
    print("\n✅ База данных успешно заполнена!")


if __name__ == "__main__":
    asyncio.run(main())