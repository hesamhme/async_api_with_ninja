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
from ninjaapp.models import Greeting, Order


async def process_order_async(order_id: int) -> str:
    # Asynchronously wait for 10 seconds
    await asyncio.sleep(10)

    # Retrieve the order asynchronously
    try:
        order = await Order.objects.aget(id=order_id)
    except Order.DoesNotExist:
        return "Order not found"

    order.status = "done"
    order.result_message = (
        f"Your order is done for link '{order.link}' and count of '{order.count}' "
        f"with id '{order.id}'."
    )

    # Save the order asynchronously; if your Django version doesn't
    # support asave(), wrap it with asyncio.to_thread:
    try:
        await order.asave()
    except AttributeError:
        # Fallback if asave() is unavailable:
        await asyncio.to_thread(order.save)

    return order.result_message


@shared_task
def process_order(order_id: int) -> str:
    # Execute the async function to completion and get the final result.
    return asyncio.run(process_order_async(order_id))

