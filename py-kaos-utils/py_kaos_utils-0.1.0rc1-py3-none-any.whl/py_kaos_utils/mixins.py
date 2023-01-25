# Credit to ChatGPT for this implementation
class TrackChangesMixin:
    """
    Mixin class that tracks changes made to fields specified in Config.fields_to_track.

    Example:
        >>> class MyModel(TrackChangesMixin, Model):
        >>>    name = CharField()
        >>>    age = IntegerField()
        >>>    class Config:
        >>>        fields_to_track = ['name']
        >>>
        >>> model = MyModel(name="John", age=30)
        >>> model.name = "Mark"
        >>> model.has_field_changed("name") # True
        >>> model.has_field_changed("age") # False
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_values = {}

    def __setattr__(self, name, value):
        """
        Save the original value of the field if it hasn't been saved yet and field is in fields_to_track
        """

        if name in self.Config.fields_to_track:
            # Save the original value of the field if it hasn't been saved yet
            if name not in self.__original_values:
                try:
                    self.__original_values[name] = getattr(self, name)
                except AttributeError:
                    pass

        super().__setattr__(name, value)

    def has_field_changed(self, field_name):
        """
        Check if the field has changed from its original value

        :param field_name: name of the field to check
        :type field_name: str
        :return: bool indicating whether the field has changed or not
        """

        if field_name in self.__original_values:
            # Return whether the field's value has changed from the original value
            return getattr(self, field_name) != self.__original_values[field_name]
        # The field has not been changed if it doesn't have an original value
        return False

    def get_original_value(self, field_name):
        return self.__original_values[field_name]


__all__ = (
    'TrackChangesMixin',
)
