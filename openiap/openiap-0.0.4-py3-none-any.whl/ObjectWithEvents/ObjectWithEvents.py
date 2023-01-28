class ObjectWithEvents(object):
    callbacks = None

    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)
    def trigger(self, event_name, argument1, argument2, argument3):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self,argument1, argument2, argument3)
