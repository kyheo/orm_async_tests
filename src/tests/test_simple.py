from typing import Any

import pytest

from orm_async_tests.models import User


@pytest.mark.asyncio
async def test_1_is_not_2() -> None:
    assert 1 != 2


@pytest.mark.asyncio
async def test_updated_at_updated_on_change(session: Any) -> None:
    user = User(username="some-username")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.created_at == user.updated_at

    user.username = 'some-other-username'
    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.created_at != user.updated_at
