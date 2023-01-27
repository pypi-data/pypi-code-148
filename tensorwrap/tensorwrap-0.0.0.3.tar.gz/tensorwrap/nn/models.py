"""Sets of functions that allow you to define a custom model or a Sequential model."""
import tensorwrap as tf
from tensorwrap.nn.layers import Layer
import jax
from jaxtyping import Array


class Model(Layer):
    """ Main superclass for all models and loads any object as a PyTree with training and inference features."""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def call(self) -> Array:
        pass

    def __call__(self, *args) -> Array:
        # inputs = tf.Variable(args)
        inputs = args[0]
        outputs = self.call(inputs)
        return outputs

    def compile(self,
                loss,
                optimizer,
                metrics):
        """Used to compile a keras model before training."""
        self.loss_fn = loss
        self.optimizer = optimizer
        self.metrics = metrics


    def train_step(self,
                   x,
                   y=None,
                   layer=None):
        y_pred = self.__call__(x)
        metric = self.metrics(y, y_pred)
        grads = jax.grad(self.loss_fn)(tf.mean(y), tf.mean(y_pred))
        self.layers = self.optimizer.apply_gradients(grads, self.layers)
        return metric

    def fit(self,
            x=None,
            y=None,
            epochs=1):
        for epoch in range(1, epochs+1):
            metric = self.train_step(x, y, self.layers)
            print(f"Epoch {epoch} complete - - - - - -  Metrics: {metric}")



class Sequential(Model):
    def __init__(self, layers=None) -> None:
        super().__init__()
        self.layers = [] if layers is None else layers
        self.trainable_variables = []

    def add(self, layer):
        self.layers.append(layer)


    def call(self, x) -> Array:
        for layer in self.layers:
            x = layer(x)
        return x
