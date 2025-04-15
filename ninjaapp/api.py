# from ninja import NinjaAPI
# from pydantic import BaseModel
# import asyncio
# from .models import Greeting
#
# api = NinjaAPI()
#
# # Request schema remains the same.
# class HelloRequest(BaseModel):
#     name: str
#
# # Response schema remains the same.
# class HelloResponse(BaseModel):
#     message: str
#
# # Synchronous endpoint for reference.
# @api.post("/hello", response=HelloResponse)
# def say_hello(request, payload: HelloRequest):
#     return HelloResponse(message=f"hello {payload.name}")
#
# # Asynchronous endpoint using 'async def'
# @api.post("/hello_async", response=HelloResponse)
# async def say_hello_async(request, payload: HelloRequest):
#     await asyncio.sleep(5)  # Simulate a delay of 5 second
#     return HelloResponse(message=f"hello {payload.name}")
#
# # Asynchronous endpoint using Django's async ORM
# @api.post("/hello_async_save", response=HelloResponse)
# async def hello_async_save(request, payload: HelloRequest):
#     # Directly use the async ORM method to create a new record
#     await asyncio.sleep(5)
#     await Greeting.objects.acreate(name=payload.name)
#     return HelloResponse(message=f"hello {payload.name} and saved to database")
#
from ninja import NinjaAPI
from pydantic import BaseModel
import asyncio
from ninjaapp.models import Greeting
from ninjaapp.tasks import hello_from_db

# Create an instance of NinjaAPI.
api = NinjaAPI()

# Request schema
class HelloRequest(BaseModel):
    name: str

# Response schema
class HelloResponse(BaseModel):
    message: str

# API endpoint that saves the name and calls an async Celery task.
@api.post("/hello_async_celery", response=HelloResponse)
async def hello_async_celery(request, payload: HelloRequest):
    # Save the name to the database using Django's async ORM.
    await Greeting.objects.acreate(name=payload.name)

    # Dispatch the celery task.
    # The task returns an AsyncResult instance.
    task_result = hello_from_db.delay(payload.name)

    # Since task_result.get() is a blocking call,
    # run it in a separate thread using asyncio.to_thread.
    message = await asyncio.to_thread(task_result.get, timeout=10)

    return HelloResponse(message=message)