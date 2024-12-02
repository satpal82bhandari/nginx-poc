import time
import pika
import threading
import json
from fastapi import FastAPI

app = FastAPI()

RABBITMQ_HOST = "rabbitmq"

# In-memory store for items received from RabbitMQ
received_items = []

LOG_FILE = "/app/logs/server3.log"

@app.get("/")
def server3_status():
    """Test endpoint to check if Server3 is running."""
    return {"status": "Server3 is running"}

def consume_messages():
    """Consume messages from RabbitMQ and store them in memory."""
    while True:
        try:
            # Connect to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()

            # Declare a queue
            channel.queue_declare(queue="item_queue")

            # Callback to process messages
            def callback(ch, method, properties, body):
                item = json.loads(body)
                received_items.append(item)
                log_message = f"Server3 called: Received item {item}"
                print(log_message)

                # Write to log file
                with open(LOG_FILE, "a") as log_file:
                    log_file.write(log_message + "\n")

            # Start consuming
            channel.basic_consume(queue="item_queue", on_message_callback=callback, auto_ack=True)
            print("Waiting for messages...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ connection failed. Retrying in 5 seconds...")
            time.sleep(5)

@app.on_event("startup")
def startup_event():
    """Start a thread for consuming RabbitMQ messages."""
    threading.Thread(target=consume_messages, daemon=True).start()

@app.get("/orders/")
def get_orders():
    """Retrieve all orders received from RabbitMQ."""
    return received_items
