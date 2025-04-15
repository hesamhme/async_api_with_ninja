# from celery import shared_task
# from ninjaapp.models import Greeting
#
# # Define an asynchronous Celery task.
# @shared_task
# async def hello_from_db(name: str) -> str:
#     """
#     Query the database for the Greeting record matching the provided name,
#     and return a greeting message. If no record is found, return a default message.
#     """
#     # Query the database asynchronously using Django's async ORM.
#     greeting = await Greeting.objects.filter(name=name).afirst()
#     if greeting:
#         return f"hello {greeting.name}"
#     return "no greeting found"

import asyncio
from celery import shared_task
from ninjaapp.models import Greeting

async def hello_from_db_async(name: str) -> str:
    # Use Django's async ORM to query the Greeting
    greeting = await Greeting.objects.filter(name=name).afirst()
    if greeting:
        return f"hello {greeting.name}"
    return "no greeting found"

@shared_task
def hello_from_db(name: str) -> str:
    # Run the async function to completion, ensuring the result is a string.
    return asyncio.run(hello_from_db_async(name))
