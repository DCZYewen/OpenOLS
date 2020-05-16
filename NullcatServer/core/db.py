from .config import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

db_url = conf.get("database", "database_url")
is_debug = conf.get("database", "debug")
mem_db = None

Base = declarative_base()
if db_url.find("sqlite") == 0:
    engine = create_engine(db_url, poolclass=SingletonThreadPool, echo=is_debug,
                           connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url, encoding="utf-8", convert_unicode=True, echo=is_debug)
if conf.get("database", "use_memcached"):
    from memcache import Client
    mem_db_url = conf.get("database", "memcached_url")
    if not mem_db_url:
        raise ValueError("must define memcached_url in config before use memcached")
    mem_db = Client([mem_db_url], is_debug)
DBSession = sessionmaker(bind=engine)
