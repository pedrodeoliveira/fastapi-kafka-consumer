from aiokafka import AIOKafkaConsumer
import asyncio
import json


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# global variables
loop = asyncio.get_event_loop()


async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=KAFKA_CONSUMER_GROUP_PREFIX)
    # get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            # x = json.loads(msg.value)
            print(f"Consumed msg: {msg}")
    finally:
        # will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

loop.run_until_complete(consume())
