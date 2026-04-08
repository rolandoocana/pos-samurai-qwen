from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
try:
    from . import config
except ImportError:
    import config
engine = create_engine(f"sqlite:///{config.DB_PATH}?check_same_thread=False")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase): pass
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        for p in ["PRAGMA journal_mode=WAL;", "PRAGMA synchronous=NORMAL;", "PRAGMA cache_size=-2000;", "PRAGMA foreign_keys=ON;", "PRAGMA busy_timeout=5000;"]:
            conn.execute(text(p))
        conn.commit()
