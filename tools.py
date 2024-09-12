from typing import Callable, Type, Optional
from langchain_core.tools import StructuredTool, Tool
from tool_function import get_geo_data_from_city_or_zip, get_weather, get_local_datetime
from pydantic.v1 import BaseModel, Field

class GetGeoDataToolSchema(BaseModel):
    zip_code: Optional[str] = Field(default=None, description="the zip code")
    country_name: Optional[str] = Field(default=None, description="the country name")
    city_name: Optional[str] = Field(default=None, description="the city name")

class GetWeatherToolSchema(BaseModel):
    geo_data: object = Field(description="Geographical data with latitude and longitude.")
    is_forecast:bool = Field(default=False, description= "True to get a forecast, False to get the current weather.")
    local_requested_timestamp : float = Field(default=0.0, description="Unix timestamp for the requested forecast time. Use get_local_datetime_tool to generate this.")

class GetLocalDateTimeToolSchema(BaseModel):
    geo_data: object = Field(description="Geographical data with latitude and longitude.")
    days: Optional[int] = Field(default = 0, description= "Optional parameter to specify how many days in the future to calculate the date. Default is 0 (current day).")
    hour : Optional[int] = Field(default = 10 ,description="Optional parameter to set the hour of the day for the future date. Default is 10 (10 AM).")

def get_geo_data_from_city_or_zip_tool():
   return StructuredTool(
        name="get_geo_data_from_city_or_zip",
        description="Get Geographical data with latitude and longitude using zip code and country name or city name and country name combinations. When zip code is passed, country name must be present.",
        func=get_geo_data_from_city_or_zip,
        args_schema=GetGeoDataToolSchema,
        infer_schema=True,
        verbose=True,
        handle_tool_error=True,
        handle_validation_error=True,
    )

def get_weather_tool():
    return StructuredTool(
        name="get_weather",
        description="Getting current weather or forecast for the upcoming 5 days (not more than that) at a specified geo location. Geo data must be received from get_geo_data_from_city_or_zip before calling this tool. If it's a forecast, we MUST need the local_requested_timestamp generated from get_local_datetime tool.",
        func=get_weather,
        args_schema=GetWeatherToolSchema,
        infer_schema=True,
        verbose=True,
        handle_tool_error=True,
        handle_validation_error=True,
    )

def get_local_datetime_tool():
    return StructuredTool(
        name="get_local_datetime",
        description="If a future weather forecast is queried, this tool must be called and the returned value MUST be used in get_weather function's local_requested_timestamp variable.",
        func=get_local_datetime,
        args_schema=GetLocalDateTimeToolSchema,
        infer_schema=True,
        verbose=True,
        handle_tool_error=True,
        handle_validation_error=True,
    )
    