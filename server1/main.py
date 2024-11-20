from fastapi import FastAPI
import pika
import json

app = FastAPI()

RABBITMQ_HOST = "rabbitmq"

@app.get("/items/")
def server1_status():
    """Test endpoint to check if Server1 is running."""
    return {"status": "Server1 is running"}

@app.post("/items/")
def send_item(item: dict):
    """Send an item message to RabbitMQ."""
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue="item_queue")

        # Publish the message
        channel.basic_publish(exchange="", routing_key="item_queue", body=json.dumps(item))
        connection.close()

        return {"message": "Item sent successfully", "item": item}
    except Exception as e:
        return {"error": str(e)}

