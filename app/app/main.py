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


@app.get(URL_PREFIX + "/trailheads", tags=["geojson"])
async def trailheads():
    """Get all trailhead points as geojson"""
    query = """
        select gid, geom as geometry from trailheads
    """
    return await postgis_query_to_geojson(query, ["gid", "geometry"], DATABASE_URL)


@app.get(URL_PREFIX + "/trail-segments", tags=["geojson"])
async def trail_segments():
    """Get all trail segment lines as geojson"""
    query = """
        select
            delcogis_5 as trail_name,
            status_f_1 as status,
            geom as geometry
        from trail_segments
    """
    return await postgis_query_to_geojson(query, ["trail_name", "status", "geometry"], DATABASE_URL)
