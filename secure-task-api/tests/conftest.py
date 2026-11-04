import pytest
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models import Task, User

@pytest.fixture(scope="session")
def test_engine():
    """create an SQLAlchemy engine connected only to the test database."""


    test_database_url = URL.create(
        drivername="mysql+pymysql",
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.TEST_MYSQL_DATABASE,
    )

    engine = create_engine(test_database_url,
        pool_pre_ping=True,
    )

    yield engine

    engine.dispose()

@pytest.fixture()
def test_database(test_engine):
    """create clean tables before each test and remove them afterward."""

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db_session(test_database):
    """Provide a database session connected to the test database."""

    TestingSessionLocal = sessionmaker(
        bind=test_database,
        autoflush=False,
        autocommit=False,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(test_database):
    """Proviide a FasrAPI test client using a test database."""

    TestingSessionLocal = sessionmaker(
        bind=test_database,
        autoflush=False,
        autocommit=False,
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
