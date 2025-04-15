from ninja import NinjaAPI
from pydantic import BaseModel
import asyncio
from .models import Greeting

api = NinjaAPI()

# Request schema remains the same.
class HelloRequest(BaseModel):
    name: str

# Response schema remains the same.
class HelloResponse(BaseModel):
    message: str

# Synchronous endpoint for reference.
@api.post("/hello", response=HelloResponse)
def say_hello(request, payload: HelloRequest):
    return HelloResponse(message=f"hello {payload.name}")

# Asynchronous endpoint using 'async def'
@api.post("/hello_async", response=HelloResponse)
async def say_hello_async(request, payload: HelloRequest):
    await asyncio.sleep(5)  # Simulate a delay of 5 second
    return HelloResponse(message=f"hello {payload.name}")

# Asynchronous endpoint using Django's async ORM
@api.post("/hello_async_save", response=HelloResponse)
async def hello_async_save(request, payload: HelloRequest):
    # Directly use the async ORM method to create a new record
    await Greeting.objects.acreate(name=payload.name)
    return HelloResponse(message=f"hello {payload.name} and saved to database")

