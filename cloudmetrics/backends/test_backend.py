from cloudmetrics.backends import MetricsBackend


class TestMetricsBackend(MetricsBackend):
    """
    A backend used for testing purposes.
    It puts everything onto a list which can be inspected.

    """

    def __init__(self, *args, **kwargs):
        super(TestMetricsBackend, self).__init__(*args, **kwargs)
        self.published = []

    def publish(self, items):

        for (name, value, unit) in items:

            name_parts = [self.namespace, name]
            if self.hostname:
                name_parts.extend(('HostName', self.hostname))
            metric_name = ':'.join(name_parts)

            if unit != 'None':
                value = '%s=%s' % (unit, value)

            self.published.append('%s %s' % (metric_name, value))


class FallbackTestMetricsBackend(TestMetricsBackend):
    """
    This is duplicate backend which uses a class level published list,
    so the tests can check it without having access to the instance.

    """

    published = []

    def __init__(self, *args, **kwargs):
        super(TestMetricsBackend, self).__init__(*args, **kwargs)

    @classmethod
    def consume_published(cls):
        """Return and clear the published list."""
        published = cls.published
        cls._published = []
        return published
