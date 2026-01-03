from configs.config_manager import read_azure_service_bus_config

import asyncio
from azure.servicebus.aio import ServiceBusClient

async def run_trigger():
    az_settings = read_azure_service_bus_config()

    async with ServiceBusClient.from_connection_string(
        conn_str= az_settings["connection_string"],
        logging_enable=True
        ) as servicebus_client:

        async with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(
                queue_name=az_settings["queue_name"]
            )
            async with receiver:
                received_msgs = await receiver.receive_messages(
                    max_wait_time=5, max_message_count=20
                    )
                for msg in received_msgs:
                    print("Received: " + str(msg))
                    # complete the message so that the message is removed from the queue
                    await receiver.complete_message(msg)


if __name__ == "__main__":
    asyncio.run(run_trigger())
