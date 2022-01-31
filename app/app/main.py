import os
from dotenv import find_dotenv, load_dotenv
import asyncpg
from asyncio import sleep
from typing import List
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .database import postgis_query_to_geojson, sql_query_raw

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL", None)
URL_PREFIX = os.getenv("URL_PREFIX", "")

app = FastAPI(docs_url=URL_PREFIX)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get(URL_PREFIX + "/hello-world", tags=["boilerplate"])
async def zone_names_with_list_of_taz_ids():
    """
    """
    return {"hello": "world"}
