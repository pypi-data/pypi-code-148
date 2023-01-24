from typing import Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from kaiju_tools.functions import retry

from kaiju_tools.streams import Consumer, Producer, Listener

__all__ = ['KafkaConsumer', 'KafkaProducer', 'KafkaListener']


class KafkaConsumer(Consumer):
    """Stream consumer."""

    def __init__(self, *args, timeout_ms: int = 1000, max_records: int = 500, **kws):
        """Initialize."""
        super().__init__(*args, **kws)
        self.timeout_ms = max(0, int(timeout_ms)) if timeout_ms else 0
        self.max_records = max(1, int(max_records)) if max_records else None
        self._consumer = None

    async def _init(self):
        self._transport = AIOKafkaConsumer(**self._settings)
        await self._transport.start()
        self._transport.subscribe(topics=[self.topic])
        self.logger.info('TOPIC %s', self.topic)

    async def _close(self):
        await self._transport.stop()
        self._transport = None

    async def _get_message_batch(self):
        batch = await self._transport.getmany(timeout_ms=self.timeout_ms, max_records=self.max_records)
        return batch

    async def _process_batch(self, batch):
        if not batch:
            return
        commits = {}
        try:
            for tp, messages in batch.items():
                for msg in messages:
                    _ = msg.key.decode() if msg.key else None
                    body = msg.value
                    headers = {key: value.decode('utf-8') for key, value in msg.headers}
                    await self._process_request(headers, body)
                    commits[tp] = msg.offset + 1
        finally:
            if commits:
                await retry(self._transport.commit, (commits,), retries=10, retry_timeout=5.0, logger=self.logger)


class KafkaProducer(Producer):
    """Stream message producer."""

    async def init_topic(self, topic: str):
        topic = Consumer.get_topic_key(self.app.env, self._namespace, topic)
        self.logger.info('Starting topic "%s".', topic, extra={'topic': topic})
        result = await self._send_request(topic, None, {}, b'', wait=True)
        self.logger.debug(result)

    async def _init(self):
        self._transport = AIOKafkaProducer(**self._settings)
        await self._transport.start()

    async def _close(self):
        await self._transport.stop()
        self._transport = None

    async def _send_request(self, topic: str, key: Optional, headers: dict, request: bytes, wait=False, **kws):
        if key:
            key = key.encode('utf-8')
        if headers:
            headers = [(key, str(value).encode('utf-8')) for key, value in headers.items()]
        if wait:
            resp = await self._transport.send_and_wait(topic=topic, key=key, value=request, headers=headers, **kws)
        else:
            resp = await self._transport.send(topic=topic, key=key, value=request, headers=headers, **kws)
        self.logger.debug('New record: [%s] %s', topic, resp)
        return resp


class KafkaListener(Listener):
    """Stream service."""

    service_name = 'streams.kafka'
    consumer_class = KafkaConsumer
    producer_class = KafkaProducer
    transport_class = None
