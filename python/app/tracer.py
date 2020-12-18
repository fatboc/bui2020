from jaeger_client import Config
from flask_opentracing import FlaskTracing
import logging
import time

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'jaeger-agent',
                'reporting_port': '6831',
            },
            'logging': True,
        },
        service_name='bui2020',
        validate=True,
    )

    return config.initialize_tracer()

tracer = init_tracer('hello-world')
