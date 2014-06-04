from boto.ec2.cloudwatch import CloudWatchConnection
from boto.exception import NoAuthHandlerFound

from cloudmetrics.backends import MetricsBackend


# Limit defined by Amazon - don't change it unless they do.
AWS_MAX_BATCH_SIZE = 10


# This relies on /etc/boto.cfg being configured.
try:
    CLOUDWATCH_CONNECTION = CloudWatchConnection()
except NoAuthHandlerFound:
    raise


class CloudWatchMetricsBackend(MetricsBackend):

    # Send as many items as possible in each CloudWatch API call.
    BUFFER_SIZE = AWS_MAX_BATCH_SIZE

    # Set this per environment.
    ENVIRONMENT = 'production'

    def _get_dimensions(self):
        """
        Create a dimensions dictionary. Use the hostname if "use_hostname"
        has been called. Differentiate between production, staging, dev,
        etc, because CloudWatch is a single pool of metric data.

        """

        if self.hostname:
            return {
                'Environment': self.ENVIRONMENT,
                'HostName': self.hostname,
            }
        else:
            return {
                'Environment': self.ENVIRONMENT,
            }

    def publish(self, items):
        """Send the buffered metric data to CloudWatch."""

        # Read the items into three separate lists.
        # This is how CloudWatch accepts multiple items.
        names = []
        values = []
        units = []
        for (name, value, unit) in items:
            names.append(name)
            values.append(value)
            units.append(unit)

        CLOUDWATCH_CONNECTION.put_metric_data(
            namespace=self.namespace,
            name=names,
            value=values,
            unit=units,
            dimensions=self._get_dimensions(),
        )
