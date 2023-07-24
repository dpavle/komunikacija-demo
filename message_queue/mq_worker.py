import pika
import time
import os

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOSTNAME'] or 'rabbitmq'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='tasks_queue', durable=True)

# Callback function to process messages
def process_task(ch, method, properties, body):
    task = body.decode()
    print(f"Received task: {task}")

    # Simulate time-consuming task
    time.sleep(5)
    print(f"Task '{task}' completed")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume tasks from the queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='tasks_queue', on_message_callback=process_task)

print(' [*] Waiting for tasks. To exit, press CTRL+C')
channel.start_consuming()
