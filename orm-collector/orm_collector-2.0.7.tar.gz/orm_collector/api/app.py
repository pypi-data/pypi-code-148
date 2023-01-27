import aiomcache
import os
from typing import Union
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends,  HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from orm_collector.manager import SessionCollector
from rich import print
from pathlib import Path
#import aioredis
from networktools.time import now
from fastapi_cache.backends.memcached import MemcachedBackend

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:6060",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://165.232.132.187:8000",
    "http://10.54.217.99:8888"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    mc = aiomcache.Client("127.0.0.1", 11211)
    FastAPICache.init(MemcachedBackend(mc), prefix="fastapi-cache")


def get_db():
    schema = "COLLECTOR"
    dbdata = dict(
        dbuser=os.environ.get('%s_DBUSER' % schema),
        dbpass=os.environ.get('%s_DBPASS' % schema),
        dbname=os.environ.get('%s_DBNAME' % schema),
        dbhost=os.environ.get('%s_DBHOST' % schema),
        dbport=os.environ.get('%s_DBPORT' % schema)
    )

    base_log_path = Path(os.getenv("ORM_LOG_PATH", "~")).resolve().absolute()
    log_path = base_log_path / "log" / "api-orm.log"

    session = SessionCollector(
        log_path=log_path, active='true', server='bellaco', **dbdata)
    try:
        yield session
    except Exception as e:
        print("Error al crear sesion", e)
    finally:
        print(now(), "Closing database connection")
        session.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stations")
@cache(expire=300)
async def all_stations(session: SessionCollector = Depends(get_db),
                       code: Union[str, None] = None, name: Union[str, None] = None):
    server_name = os.getenv("ORM_SERVER_NAME", "bellaco")
    stations = session.get_station_data(server=server_name)
    dataset = []
    for item in stations:
        station_id = item["id"]
        dbdata = {d.priority: d for d in
                  session.get_dbserver_data(station_id)}
        item["dbdata"] = dbdata
        dataset.append(item)
    if code:
        return [d for d in dataset if code.lower() in d["code"].lower()]
    if name:
        return [d for d in dataset if name.lower() in d["name"].lower()]

    return dataset


@app.get("/databases")
@cache(expire=300)
async def all_databases(session: SessionCollector = Depends(get_db)):
    dbs = session.get_dbservers()
    dataset = [d for d in dbs]
    return dataset


@app.get("/networks")
@cache(expire=300)
async def all_networks(session: SessionCollector = Depends(get_db)):
    nets = session.get_network()
    dataset = [d for d in nets]
    return dataset


@app.get("/servers")
@cache(expire=300)
async def all_servers(session: SessionCollector = Depends(get_db)):
    servers = session.get_server()
    dataset = [d for d in servers]
    return dataset


@app.get("/protocols")
@cache(expire=300)
async def all_protocols(session: SessionCollector = Depends(get_db)):
    queryset = session.get_protocol()
    dataset = [d for d in queryset]
    return dataset


@app.get("/dbtypes")
@cache(expire=300)
async def all_dbtypes(session: SessionCollector = Depends(get_db)):
    queryset = session.get_dbtype()
    dataset = [d for d in queryset]
    return dataset


"""
get, port, list (last n=10)
"""


@app.get("/active_db")
@cache(expire=300)
async def active_db(session: SessionCollector = Depends(get_db)):
    active_db = session.get_active_db()
    return active_db
