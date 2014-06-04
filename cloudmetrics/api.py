import contextlib
import socket


class MetricsContext(object):

    units = {
        'seconds': 'Seconds',
        'microseconds': 'Microseconds',
        'milliseconds': 'Milliseconds',
        'bytes': 'Bytes',
        'kilobytes': 'Kilobytes',
        'megabytes': 'Megabytes',
        'gigabytes': 'Gigabytes',
        'terabytes': 'Terabytes',
        'bits': 'Bits',
        'kilobits': 'Kilobits',
        'megabits': 'Megabits',
        'gigabits': 'Gigabits',
        'terabits': 'Terabits',
        'percent': 'Percent',
        'count': 'Count',
        'bytes_per_second': 'Bytes/Second',
        'kilobytes_per_second': 'Kilobytes/Second',
        'megabytes_per_second': 'Megabytes/Second',
        'gigabytes_per_second': 'Gigabytes/Second',
        'terabytes_per_second': 'Terabytes/Second',
        'bits_per_second': 'Bits/Second',
        'kilobits_per_second': 'Kilobits/Second',
        'megabits_per_second': 'Megabits/Second',
        'gigabits_per_second': 'Gigabits/Second',
        'terabits_per_second': 'Terabits/Second',
        'count_per_second': 'Count/Second',
        'value': 'None',
    }

    def __init__(self, backend):
        self._backend = backend

    def flush(self):
        self._backend.flush()

    def push(self, metric_name, **kwargs):
        """
        Publish a single metric data point. One unit/value keyword argument
        must be supplied. Read the source code or documentation to see all
        supported value types.

        """

        if not isinstance(metric_name, str):
            raise TypeError('The metric name must be a string.')

        if not metric_name:
            raise ValueError('The metric name must not be empty.')

        if len(kwargs) != 1:
            raise ValueError('One unit/value keyword argument must be supplied.')

        unit, value = kwargs.items()[0]

        try:
            unit = self.units[unit]
        except KeyError:
            raise ValueError('Unsupported value type %r' % unit)

        self._backend.push_metric(
            name=metric_name,
            value=value,
            unit=unit,
        )

    def use_hostname(self, hostname=True):
        if hostname:
            if hostname is True:
                hostname = socket.gethostname()
            elif not isinstance(hostname, str):
                raise TypeError('The hostname must be either True or a string.')
        self._backend.use_hostname(hostname)


class MetricsAPI(object):

    def __init__(self, backend_class, fallback_backend_class=None):
        """Create a new metrics API using the given backend classes."""
        self._backend_class = backend_class
        self._fallback_backend_class = fallback_backend_class

    @contextlib.contextmanager
    def __call__(self, namespace, use_hostname=False):
        """Create a new metrics context using the given namespace."""

        if not isinstance(namespace, str):
            raise TypeError('The metrics namespace must be a string.')

        if not namespace:
            raise ValueError('The metrics namespace must not be empty.')

        metrics_backend = self._backend_class(namespace, self._fallback_backend_class)

        metrics_context = MetricsContext(metrics_backend)

        if use_hostname:
            metrics_context.use_hostname(use_hostname)

        try:
            yield metrics_context
        finally:
            metrics_context.flush()
