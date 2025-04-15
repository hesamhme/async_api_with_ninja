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
from pydantic import BaseModel, HttpUrl
from ninjaapp.tasks import process_order
import asyncio
from ninjaapp.models import Greeting, Order
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


# Define request schema
class OrderRequest(BaseModel):
    link: HttpUrl  # HttpUrl type validates URL format automatically
    count: int


# Define response schema
class OrderResponse(BaseModel):
    message: str


# Endpoint to create an order and trigger asynchronous processing
@api.post("/order", response=OrderResponse)
def create_order(request, payload: OrderRequest):
    # Save the order in the database; defaults to "registered" status
    order = Order.objects.create(link=payload.link, count=payload.count)

    # Dispatch the Celery task to process this order asynchronously
    process_order.delay(order.id)

    # Respond immediately to the user
    return OrderResponse(message="Your order is registered")

@api.get("/order/{order_id}", response=OrderResponse)
def get_order_status(request, order_id: int):
    try:
        order = Order.objects.get(id=order_id)
        message = order.result_message or f"Order status: {order.status}"
        return OrderResponse(message=message)
    except Order.DoesNotExist:
        return OrderResponse(message="Order not found")
