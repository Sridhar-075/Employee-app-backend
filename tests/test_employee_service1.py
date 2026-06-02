# `pytest_asyncio` provides the *async-aware* fixture decorator. Plain
# `@pytest.fixture` doesn't know how to drive an `async def` body — you
# have to use `@pytest_asyncio.fixture` whenever the fixture itself is
# async or yields an async resource.
import pytest_asyncio

# Same async-flavoured SQLAlchemy imports as the previous slide.
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from auth.utils import hash_password
from database import Base
from employees import service as employee_service
from models.employee import Employee
import pytest


# The fixture: a single function that owns the engine, the schema, and
# the session — and tears it all back down when the test finishes.
@pytest_asyncio.fixture
async def db_session():
    # ── SETUP — runs before each test that requests `db_session` ──────
    # Build a fresh in-memory engine. Every test gets its own DB.
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # Open an async transactional connection and create every ORM table.
    # `run_sync` bridges SQLAlchemy's sync DDL onto the async connection.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Build the session factory and immediately open one session for the test.
    # `expire_on_commit=False` keeps loaded attrs usable after commit().
    db = async_sessionmaker(engine, expire_on_commit=False)()

    # ── HAND-OFF — pytest pauses the fixture here and runs the test ──
    try:
        yield db  # test receives this as the `db_session` arg

    finally:
        # ── TEARDOWN — runs even if the test raised an exception ────────
        # `try / finally` is the guarantee — without it a failing assert
        # would skip the cleanup and the next test would inherit junk.
        # Release the connection back to the engine's pool.
        await db.close()
        # Wipe the schema. Belt-and-braces — the engine is being disposed
        # next anyway, but explicit cleanup is the lesson here.
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        # Dispose the engine — closes the underlying connection pool.
        await engine.dispose()


# The test is now pure "act + assert" — no engine, no create_all, no
# cleanup. Pytest sees the `db_session` parameter, runs the fixture
# above, and hands the yielded session in.
@pytest.mark.asyncio
async def test_get_by_id_returns_seeded_employee(db_session):

    # Seed a row directly via the ORM. We construct Employee ourselves
    # (with a real `password_hash`) because service.create currently
    # drops the password field — bypassing it keeps this test focused.
    seeded = Employee(
        name="Ada", email="ada@example.com", password_hash=hash_password("secret123")
    )
    # `add()` is sync — it just stages the row in the session.
    db_session.add(seeded)
    # `commit()` is the IO step. Must be awaited.

    await db_session.commit()

    # `refresh()` re-reads the row so `seeded.id` is populated.

    await db_session.refresh(seeded)

    # Call the function under test — async, so we await.

    fetched = await employee_service.get_by_id(db_session, seeded.id)

    assert fetched.id == seeded.id
    assert fetched.email == "ada@example.com"
