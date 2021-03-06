import json
import asyncpg
import shapely
import geopandas


def encode_geometry(geometry):
    """
    Transform `shapely.geometry' into PostGIS type
    """
    if not hasattr(geometry, "__geo_interface__"):
        raise TypeError("{g} does not conform to " "the geo interface".format(g=geometry))

    shape = shapely.geometry.asShape(geometry)
    return shapely.wkb.dumps(shape)


def decode_geometry(wkb):
    """
    Transform PostGIS type into `shapely.geometry'
    """
    return shapely.wkb.loads(wkb)


async def postgis_query_to_geojson(query: str, columns: list, uri: str):
    """
    Connect to postgres via `asyncpg` and return spatial query output
    as a geojson file
    """
    conn = await asyncpg.connect(uri)

    try:

        await conn.set_type_codec(
            "geometry",
            encoder=encode_geometry,
            decoder=decode_geometry,
            format="binary",
        )

        result = await conn.fetch(query)

    finally:
        await conn.close()

    gdf = geopandas.GeoDataFrame.from_records(result, columns=columns)

    return json.loads(gdf.to_json())
