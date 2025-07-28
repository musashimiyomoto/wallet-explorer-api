from taskiq_nats import NatsBroker

from settings import broker_settings

broker = NatsBroker(servers=broker_settings.url, queue=broker_settings.default_queue)
