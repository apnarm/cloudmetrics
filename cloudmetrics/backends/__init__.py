from Queue import Empty, Full, Queue


class MetricsBackend(object):

    BUFFER_SIZE = 1

    def __init__(self, namespace, fallback_backend_class=None):
        self.namespace = namespace
        self.hostname = None
        self._fallback_backend_class = fallback_backend_class
        self._buffer = Queue(maxsize=self.BUFFER_SIZE)

    def flush(self):
        """
        Flushes the buffered metric items. In the event of an error, this will
        use the fallback metrics API if it has been configured to have one.

        """

        # Read the items in from the buffer, exactly as
        # they were provided to the push_metric method.
        items = []
        for x in xrange(self._buffer.maxsize):
            try:
                items.append(self._buffer.get(block=False))
            except Empty:
                break

        try:

            # Publish the items. The publish method is very specific to
            # the backend subclass, and is where their main logic is.
            self.publish(items)

        except Exception:

            # The backend failed for some reason, so fall back to another one.
            if self._fallback_backend_class:
                # TODO: log the issue
                pass
            else:
                raise

            # Reproduce the calls made from the metrics context object.
            backend = self._fallback_backend_class(self.namespace)
            backend.use_hostname(self.hostname)
            for (name, value, unit) in items:
                backend.push_metric(
                    name=name,
                    value=value,
                    unit=unit,
                )
            backend.flush()

    def push_metric(self, name, value, unit):
        """
        Put the metric data in the buffer queue.
        If it is full, flush the buffer to make room.

        """

        item = (name, value, unit)
        while True:
            try:
                self._buffer.put(item, block=False)
            except Full:
                self.flush()
            else:
                break

    def use_hostname(self, hostname):
        self.hostname = hostname

    ############################################################################
    # Subclasses should implement everything below here.
    ############################################################################

    def publish(self, items):
        """Publish metric data items."""
        raise NotImplementedError
