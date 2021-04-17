import asyncio
import random
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.sql.expression import Delete

from orm_async_tests.db import async_session
from orm_async_tests.models import TrackPoint, User


async def cleanup() -> None:
    print("cleanup: Start.")
    async with async_session.begin() as session:
        await session.execute(Delete(TrackPoint))
        await session.execute(Delete(User))
    print("cleanup: Stop.")


async def load_data() -> None:
    print("load_data: Start.")
    session = async_session()
    try:
        for i in range(100):
            session.add(User(username=f"username-{i}"))
            if i > 0 and i % 10 == 0:
                print(f"load_data: Commit {i}.")
                sleep = random.randint(1, 5)  # noqa: S311
                await session.commit()
                print(f"load_data: Sleep {sleep} seconds.")
                await asyncio.sleep(sleep)
                session = async_session()
    finally:
        print("load_data: Task ended. Commit remainder")
        await session.commit()
    print("load_data: Stop.")


async def add_tracking_points_to_user_30() -> None:
    print("add_tracking_points_to_user_30: Start.")
    user = None
    async with async_session() as session:
        while user is None:
            print("add_tracking_points_to_user_30: User not found ...")
            qs = select(User).filter(User.username == "username-30")
            res = await session.execute(qs)
            user = res.scalars().first()
            await asyncio.sleep(1)

    session = async_session()
    try:
        print("add_tracking_points_to_user_30: User found.")
        for i in range(100000):
            session.add(TrackPoint(user=user, lat=i, lon=i * -1, date=datetime.utcnow()))
            if i > 0 and i % 500 == 0:
                print(f"add_tracking_points_to_user_30: Commit {i}.")
                await session.commit()
                sleep = random.randint(1, 5)  # noqa: S311
                print(f"add_tracking_points_to_user_30: Sleep {sleep} seconds.")
                await asyncio.sleep(sleep)
                session = async_session()
    finally:
        print("add_tracking_points_to_user_30: Task ended. Commit remainder")
        await session.commit()


async def async_main() -> None:
    await cleanup()
    tasks = [
        asyncio.create_task(load_data()),
        asyncio.create_task(add_tracking_points_to_user_30()),
    ]
    await asyncio.gather(*tasks)


def run() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    run()
