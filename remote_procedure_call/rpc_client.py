import pika
import uuid
import timeit
import sys

class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1]))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, task_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(task_id))

        while self.response is None:
            self.connection.process_data_events()

        return self.response

if __name__ == "__main__":
    client = RpcClient()

    # Number of requests to make
    num_requests = 5

    # Record the start time
    start_time = timeit.default_timer()

    # Simulate sending multiple RPC requests
    for task_id in range(1, num_requests + 1):
        response = client.call(task_id)
        print(f"RPC Response for Task ID {task_id}: {response}")

    # Calculate elapsed time
    elapsed_time = timeit.default_timer() - start_time

    # Calculate throughput (requests per second)
    throughput = num_requests / elapsed_time

    print(f"Number of Requests: {num_requests}")
    print(f"Elapsed Time: {elapsed_time:.5f} seconds")
    print(f"Throughput: {throughput:.2f} requests per second")