import pytest

from py_kaos_utils.mixins import TrackChangesMixin


class TestTrackChangesMixin:
    @pytest.fixture
    def mock_model(self):
        """
        Fixture that returns a mock Model that uses the TrackChangesMixin
        """

        class MyModel(TrackChangesMixin):
            class Config:
                fields_to_track = ['name']

        model = MyModel()
        model.name = "John"
        model.age = 30
        return model

    def test_has_field_changed(self, mock_model):
        assert not mock_model.has_field_changed("name")
        assert not mock_model.has_field_changed("age")

        mock_model.name = "Mark"
        assert mock_model.has_field_changed("name")
        assert not mock_model.has_field_changed("age")

    def test___setattr__(self, mock_model):
        # Test that original value is saved when field is in fields_to_track
        mock_model.name = "Mark"
        assert mock_model.get_original_value('name') == 'John'

        # Test that original value is not saved when field is not in fields_to_track
        mock_model.age = 40
        with pytest.raises(KeyError):
            mock_model.get_original_value('age')
