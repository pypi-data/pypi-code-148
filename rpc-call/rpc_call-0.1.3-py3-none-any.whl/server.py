import pika
import orjson
from loguru import logger
from pydantic import AmqpDsn
from .types import Task, CallbackHandler
from .helpers import handle_errors


class RPCServer:
    def __init__(
        self, callback_handler: CallbackHandler, amqp_dsn: str, queue_name: str
    ) -> None:
        self.callback_handler = callback_handler()  # callback handler class
        self.amqp_dsn = amqp_dsn  # RMQ connection string
        self.queue_name = queue_name  # RMQ queue name
        connection = pika.BlockingConnection(pika.URLParameters(self.amqp_dsn))
        channel = connection.channel()
        # channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.on_request
        )
        logger.info(" [x] Awaiting RPC requests")
        channel.start_consuming()

    @handle_errors
    def call_procedure(self, body: bytes):
        task = Task.parse_obj(orjson.loads(body))
        logger.info(f"task -> {task}")
        return getattr(self.callback_handler, task.procedure)(**task.kwargs)

    def on_request(self, ch, method, props, body) -> None:
        response = orjson.dumps(self.call_procedure(body))
        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=response,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


# #
# class TestCallbackHandler:
#     def test(self, arg1, arg2=0):
#         return {'result': 'test({arg1}, {arg2})'}


# def start():
#     RPCServer(callback_handler = TestCallbackHandler())
