import os
from dotenv import find_dotenv, load_dotenv
import asyncpg
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from .database import postgis_query_to_geojson


class NewVote(BaseModel):
    """
    A vote requires the user's email address
    and a list of the trailhead IDs that were selected
    """

    email_address: str
    trailheads: List[int]


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
async def get_all_trailheads_as_geojson():
    """Get all trailhead points as geojson"""

    query = """
        select
            gid,
            geom as geometry
        from trailheads
    """
    return await postgis_query_to_geojson(query, ["gid", "geometry"], DATABASE_URL)


@app.get(URL_PREFIX + "/trail-segments", tags=["geojson"])
async def get_all_trail_segments_as_geojson():
    """Get all trail segment lines as geojson"""

    query = """
        select
            delcogis_5 as trail_name,
            status_f_1 as status,
            geom as geometry
        from trail_segments
    """
    return await postgis_query_to_geojson(query, ["trail_name", "status", "geometry"], DATABASE_URL)


@app.post(URL_PREFIX + "/add-vote/", tags=["vote"])
async def define_new_group_of_tazs(vote: NewVote):
    """
    Add a new row to the 'user_votes' table with the provided
    email address and list of trailhead IDs.
    """

    conn = await asyncpg.connect(DATABASE_URL)

    await conn.execute(
        """
        INSERT INTO user_votes(email_address, submitted_on, trailheads)
        VALUES($1, $2, $3)
    """,
        vote.email_address,
        datetime.now(),
        vote.trailheads,
    )
    await conn.close()

    return {"data": vote}
