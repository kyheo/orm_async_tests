import asyncio

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from orm_async_tests.db import async_session
from orm_async_tests.models import TrackPoint


async def stream_track_point() -> None:
    print("stream_track_point: Start.")
    try:
        async with async_session() as session:
            qs = select(TrackPoint).options(joinedload(TrackPoint.user)).order_by(TrackPoint.id)
            async_result = await session.stream(qs)
            async for row in async_result:
                print(f"stream_track_point: {row[0]}")
                await asyncio.sleep(1)
        print("stream_track_point: End reached.")
    finally:
        print("stream_track_point: Task ended.")
        await session.close()
    print("stream_track_point: Stop.")


async def async_main() -> None:
    await stream_track_point()


def run() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    run()
