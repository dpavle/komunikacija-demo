import pika
import json
import timeit
import sys

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1]))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='tasks_queue', durable=True)

# Endpoint to mark a task as completed (process asynchronously via RabbitMQ)
def complete_task(task_id):
    # Send the task ID to the RabbitMQ queue for asynchronous processing
    channel.basic_publish(exchange='',
                          routing_key='tasks_queue',
                          body=str(task_id))
    print(f"Task completion request sent for processing: {task_id}")

if __name__ == '__main__':
    # Number of requests to make
    num_requests = 5

    # Record the start time
    start_time = timeit.default_timer()

    # Simulate sending multiple RPC requests
    for task_id in range(1, num_requests + 1):
        complete_task(task_id)

    # Calculate elapsed time
    elapsed_time = timeit.default_timer() - start_time

    # Calculate throughput (requests per second)
    throughput = num_requests / elapsed_time

    print(f"Number of Requests: {num_requests}")
    print(f"Elapsed Time: {elapsed_time:.5f} seconds")
    print(f"Throughput: {throughput:.2f} requests per second")