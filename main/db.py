from imports import (DeclarativeBase, AsyncSession, create_async_engine, async_sessionmaker, Column, Integer, String,
                     Float, DateTime, Text, desc, select, status, datetime)
import pytz

DATABASE_URL = "mysql+aiomysql://root:My8041SQLite@localhost/db_project"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
ukrainian_time = pytz.timezone('Europe/Kiev')

class Base(DeclarativeBase):
    pass

# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(1000), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    genre = Column(String(200), nullable=False)
    rating_igdb = Column(Float, nullable=False)
    trailer = Column(String(1000), nullable=False)
    platforms = Column(String(100), nullable=False)
    avg_users_rating = Column(Float, nullable=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    name = Column(String(50), nullable=True)
    age = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    contacts = Column(String(50), nullable=True)
    favourite_game = Column(String(50), nullable=True)


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    review = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)


async def get_users():
    async with async_session() as session:
        users = await session.execute(select(User.__table__.columns))
    return users.mappings().all()

async def get_profile_data(username):
    async with async_session() as session:
        data = await session.execute(select(Profile.__table__.columns).where(Profile.username == username))
    return data.fetchone()
async def get_games():
    async with async_session() as session:
        games = await session.execute(select(Game.__table__.columns))
    return games.fetchall()

async def get_game(id):
    async with async_session() as session:
        games = await session.execute(select(Game.__table__.columns).where(Game.id == id))
    return games.fetchone()


async def get_reviews(game_id):
    async with async_session() as session:
        reviews = await session.execute(select(Review.__table__.columns).where(Review.game_id == game_id))
    return reviews.fetchall()


async def add_user(username: str, email: str, password: str):
    async with async_session() as session:
        async with session.begin():
            new_user = User(username=username, email=email, password=password)
            session.add(new_user)
    return {'mess': 'User registered', 'status': status.HTTP_200_OK}


async def add_profile(username: str):
    async with async_session() as session:
        async with session.begin():
            new_profile = Profile(username=username)
            session.add(new_profile)
    return {'mess': 'User registered', 'status': status.HTTP_200_OK}


async def add_review(id: int, username: str, review: str, rating: int, created: datetime = datetime.now(ukrainian_time)):
    async with async_session() as session:
        async with session.begin():
            new_review = Review(game_id=id, username=username, review=review, rating=rating, created=created)
            session.add(new_review)
    return {'status': status.HTTP_200_OK}


async def update_profile(name: str, age: str, country: str, city: str, contacts: str, favourite_game: str, username):
    async with async_session() as session:
        async with session.begin():
            users_profile = await session.execute(select(Profile).where(Profile.username == username))
            result = users_profile.scalar_one_or_none()
            if result:
                result.name = name
                result.age = age
                result.country = country
                result.city = city
                result.contacts = contacts
                result.favourite_game = favourite_game
                await session.commit()
    return {'status': status.HTTP_200_OK}


async def update_avg_users_rating(avg_users_rating: float, game_id):
    async with async_session() as session:
        async with session.begin():
            game = await session.execute(select(Game).where(Game.id == game_id))
            result = game.scalars().first()
            result.avg_users_rating = avg_users_rating
            await session.commit()
    return {'status': status.HTTP_200_OK}


async def update_review(review: str, rating: int, game_id, username):
    async with async_session() as session:
        async with session.begin():
            selected_review = await session.execute(select(Review).where(Review.game_id == game_id, Review.username == username))
            result = selected_review.scalars().first()
            result.review = review
            result.rating = rating
            result.created = datetime.now(ukrainian_time)
            await session.commit()
    return {'status': status.HTTP_200_OK}


async def get_users_ratings():
    async with async_session() as session:
        users_ratings = await session.execute(select(Game.id, Game.title, Game.avg_users_rating).order_by(desc(Game.avg_users_rating)))
    return users_ratings.fetchall()

async def get_experts_ratings():
    async with async_session() as session:
        experts_ratings = await session.execute(select(Game.id, Game.title, Game.rating_igdb).order_by(desc(Game.rating_igdb)))
    return experts_ratings.fetchall()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_game(img, title, description, genre, rating_igdb, trailer, platforms, avg_users_rating):
    async with async_session() as session:
        async with session.begin():
            new_game = Game(image=img, title=title, description=description, genre=genre,
                            rating_igdb=rating_igdb, trailer=trailer, platforms=platforms, avg_users_rating=avg_users_rating)
            session.add(new_game)
    return {'status': status.HTTP_200_OK}

async def check_review(game_id, username):
    async with async_session() as session:
        checking = await session.execute(select(Review.__table__.columns).where(Review.game_id == game_id, Review.username == username))
    return bool(checking.fetchone())