class QuerySettings:
    def __init__(self, streaming, batch_size, timeout, frm, to, selector, sampler=None, object_type=None):
        self.streaming = streaming
        self.batch_size = batch_size
        self.timeout = timeout
        self.frm = frm
        self.to = to
        self.selector = selector
        self.sampler = sampler
        self.object_type = object_type

    def with_streaming(self, streaming):
        self.streaming = streaming

    def with_batch_size(self, batch_size):
        self.batch_size = batch_size

    def with_timeout(self, timeout):
        self.timeout = timeout

    def with_from(self, frm):
        self.frm = frm

    def with_to(self, to):
        self.to = to

    def with_selector(self, selector):
        self.selector = selector

    def with_tick_sampler(self, sampler):
        self.sampler = sampler