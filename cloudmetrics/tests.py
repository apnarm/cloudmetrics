import socket
import unittest

from cloudmetrics.api import MetricsAPI
from cloudmetrics.backends.test_backend import TestMetricsBackend, FallbackTestMetricsBackend


class MetricsAPITestCase(unittest.TestCase):

    def setUp(self):
        self.metrics_api = MetricsAPI(
            backend_class=TestMetricsBackend,
            fallback_backend_class=FallbackTestMetricsBackend,
        )

    def test_push(self):

        with self.metrics_api('TestPush') as metrics:
            metrics.push('First', count=1)
            metrics.push('Second', percent=2)

        expected = [
            'TestPush:First Count=1',
            'TestPush:Second Percent=2',
        ]

        self.assertEqual(metrics._backend.published, expected)

    def test_hostname(self):

        with self.metrics_api('TestHostName', use_hostname=True) as metrics:
            metrics.push('First', value=3)
            metrics.push('Second', value='dogs')

        expected = [
            'TestHostName:First:HostName:%s 3' % socket.gethostname(),
            'TestHostName:Second:HostName:%s dogs' % socket.gethostname(),
        ]

        self.assertEqual(metrics._backend.published, expected)

        with self.metrics_api('Hits', use_hostname='dogs.info') as metrics:
            metrics.push('Path', value='/buffalo/')

        expected = ['Hits:Path:HostName:dogs.info /buffalo/']

        self.assertEqual(metrics._backend.published, expected)

    def test_noop(self):

        with self.metrics_api('TestNoop') as metrics:
            pass

        expected = []

        self.assertEqual(metrics._backend.published, expected)

    def test_fallback(self):

        # Clear the fallback's published list just in case.
        FallbackTestMetricsBackend.consume_published()

        with self.metrics_api('TestFallback1') as metrics:

            # Break the published list to trigger the use of the fallback.
            metrics._backend.published = None

            metrics.push('One', value=1)
            metrics.push('Two', value=2)

        expected = [
            'TestFallback1:One 1',
            'TestFallback1:Two 2',
        ]
        self.assertEqual(FallbackTestMetricsBackend.consume_published(), expected)


if __name__ == '__main__':
    unittest.main()
