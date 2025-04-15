
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
