import pika
import os

# Sample data (you can replace this with your own data or database)
tasks = [
    {"id": 1, "title": "Task 1", "description": "Description for Task 1", "done": False},
    {"id": 2, "title": "Task 2", "description": "Description for Task 2", "done": False},
    {"id": 3, "title": "Task 3", "description": "Description for Task 3", "done": False},
    {"id": 4, "title": "Task 4", "description": "Description for Task 4", "done": False},
    {"id": 5, "title": "Task 5", "description": "Description for Task 5", "done": False},
]

def process_task_completion(task_id):
    # Simulate completion by adding a delay (you can replace this with actual task completion logic)
    import time
    time.sleep(2)

    completed_task = next((t for t in tasks if t["id"] == task_id), None)
    if completed_task:
        completed_task["done"] = True
        return completed_task
    else:
        return None

def on_request(ch, method, properties, body):
    task_id = int(body)
    response = process_task_completion(task_id)

    # Send the response back to the callback queue specified in properties
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                     body=str(response))

    # Acknowledge the RPC request
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOSTNAME'] or 'rabbitmq'))
channel = connection.channel()

# Declare an RPC queue to receive RPC requests from RabbitMQ
channel.queue_declare(queue='rpc_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print("RPC Server is waiting for RPC requests. To exit press CTRL+C")
channel.start_consuming()
