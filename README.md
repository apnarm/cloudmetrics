cloudmetrics
============

A Python library for sending metrics to CloudWatch.

Currently, the only included backend is for
CloudWatch, but custom backends are simple
to create.


Installation
------------

    pip install cloudmetrics

Usage
-----

    # Create a metrics object to use in your project.
    from cloudmetrics import MetricsAPI
    from cloudmetrics.backends.cloudwatch_backend import CloudWatchMetricsBackend
    metrics_api = MetricsAPI(CloudWatchMetricsBackend)

    # Use your metrics object to send metrics.
    with metrics_api(metric_namespace) as metrics:
        metrics.push(metric_name, **{unit: value})


Namespaces and Names
--------------------

All metrics must use a namespace and name,
which must both be strings.


Units
-----

The push method requires a single unit/value pair.

Allowed unit types:

    seconds, microseconds, milliseconds,

    percent,

    count, count_per_second

    bytes, bytes_per_second
    kilobytes, kilobytes_per_second
    megabytes, megabytes_per_second
    gigabytes, gigabytes_per_second
    terabytes, terabytes_per_second

    bits, bits_per_second
    kilobits, kilobits_per_second
    megabits, megabits_per_second
    gigabits, gigabits_per_second
    terabits,terabits_per_second

    value (unspecified unit type)

Example usage:

    with metrics_api(metric_namespace) as metrics:
        metrics.push(metric_name, count=50)
        metrics.push(metric_name2, megabytes=3)
        metrics.push(metric_name3, value='hello')


Hostnames
---------

Metrics can be dimensioned using the current hostname,
if the backend supports it.

Example usage:

    with metrics_api(metric_namespace, use_hostname=True) as metrics:
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace) as metrics:
        metrics.use_hostname()
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace, use_hostname='dogs.info') as metrics:
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace) as metrics:
        metrics.use_hostname('buffalo.info')
        metrics.push(metric_name, **{unit: value})


Buffering
---------

Metric backends can support buffering, to publish
multiple metric data points with a single request.
Buffering works within the context of a namespace.

Example usage:

    with metrics_api('SomeProcess') as metrics:
        metrics.push('ThingsProcessed', count=5)
        metrics.push('ThingsProcessed', count=9)
        metrics.push('OtherThing', kilobytes_per_second=600)


Custom Backends
---------------

It is easy to create custom metrics backends.
Here is an example that simply prints metrics
to standard output.

    from cloudmetrics import MetricsAPI
    from cloudmetrics.backends import MetricsBackend

    class PrintMetricsBackend(MetricsBackend):

        def publish(self, items):
            for (name, value, unit) in items:
                metric_name = '%s:%s' % (self.namespace, name)
                if unit != 'None':
                    value = '%s=%s' % (unit, value)
                print '%s %s' % (metric_name, value)

    metrics_api = MetricsAPI(CloudWatchMetricsBackend)
