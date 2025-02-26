from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
import json
import pathlib

app = FastAPI(title="Restaurant API")

RESTAURANTS_BY_ID = {}


@app.on_event("startup")
def on_start_up():
    date_file_path = pathlib.Path(__file__).parent / "restaurants.json"

    with open(date_file_path) as f:
        raw_data = json.load(f)

        for raw_restaurant in raw_data["restaurants"]:
            (lon, lat) = raw_restaurant["location"]
            restaurant = Restaurant(
                name=raw_restaurant["name"],
                description=raw_restaurant["description"],
                id=raw_restaurant["id"],
                location=Location(
                    city=raw_restaurant["city"],
                    coordinates=Coordinates(lon=lon, lat=lat),
                ),
            )
            RESTAURANTS_BY_ID[restaurant.id] = restaurant
        print("Restaurants loaded", RESTAURANTS_BY_ID)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get(
    "/showcase-features/{user_id}",
    summary="My custom summery",
    description="My custom description",
)
def showcase_features(
    user_id: int = Path(description="The ID of the user to get"),
    debug: bool = Query(default=False, description="Debug mode"),
):
    if debug:
        print("No we are dubugging")
    return {"foo": "bar", "user_id": user_id}


class Coordinates(BaseModel):
    lon: float
    lat: float


class Location(BaseModel):
    city: str
    coordinates: Coordinates


class Restaurant(BaseModel):
    name: str = Field(description="The name of the restaurant")
    description: str
    id: str
    location: Location


@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants():
    restaurants = []
    for restaurant in RESTAURANTS_BY_ID.values():
        restaurants.append(restaurant)
    return restaurants


@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    if restaurant_id in RESTAURANTS_BY_ID:
        return RESTAURANTS_BY_ID[restaurant_id]
    raise HTTPException(status_code=404, detail="Restaurant not found")
