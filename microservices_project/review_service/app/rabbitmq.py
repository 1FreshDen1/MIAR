import aio_pika
import os
import json

AMQP_URL = os.getenv("AMQP_URL")

async def send_review_message(review_data: dict):
    connection = await aio_pika.connect_robust(AMQP_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(review_data).encode()),
            routing_key="review_created"
        )
