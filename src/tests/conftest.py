from typing import Any

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest.mark.asyncio
@pytest.fixture
async def session() -> Any:
    dsn = "postgresql+asyncpg://docker:docker@localhost/docker"

    engine = create_async_engine(
        dsn,
        future=True,
        # echo=True,
    )

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session: sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, future=True
    )
    return async_session()
