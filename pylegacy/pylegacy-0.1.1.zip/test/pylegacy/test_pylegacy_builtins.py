"""Tests for :mod:`pylegacy.builtins`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyLegacyBuiltins(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.builtins`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] < (3, 0), reason="it exists")
    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_callable_missing(self):
        """Test that :class:`callable` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=undefined-variable
            return callable  # noqa: F821

        self.assertRaises(NameError, test_callable)

    def test_pylegacy_callable_available(self):
        """Test that :class:`pylegacy.builtins.callable` is available."""

        from pylegacy.builtins import callable

        self.assertTrue(callable(int))
        self.assertFalse(callable(1))

    @unittest.skipIf(sys.version_info[:2] >= (3, 2), reason="it exists")
    def test_resourcewarning_missing(self):
        """Test that :class:`ResourceWarning` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=undefined-variable
            return ResourceWarning  # noqa: F821

        self.assertRaises(NameError, test_callable)

    def test_pylegacy_resourcewarning_available(self):
        """Test that :class:`ResourceWarning` exists with :mod:`pylegacy`."""

        import warnings
        from pylegacy.builtins import ResourceWarning

        with self.assertWarns(ResourceWarning):
            warnings.warn("this is a ResourceWarning message", ResourceWarning)

    @unittest.skipIf(sys.version_info[:2] < (3, 0), reason="it exists")
    def test_basestring_missing(self):
        """Test that :class:`basestring` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=undefined-variable
            return basestring  # noqa: F821

        self.assertRaises(NameError, test_callable)

    def test_pylegacy_basestring_available(self):
        """Test that :class:`basestring` exists with :mod:`pylegacy`."""

        from pylegacy.builtins import basestring
        self.assertTrue(basestring)

    def test_pylegacy_basestring_error_instance_creation(self):
        """Test that :class:`basestring` exists with :mod:`pylegacy`."""

        from pylegacy.builtins import basestring
        self.assertRaises(TypeError, basestring, "hello")

    def test_pylegacy_basestring_contructor_error_unsafe_creation(self):
        """Test :class:`basestring` constructor error if called directly."""

        from pylegacy.builtins import basestring

        self.assertRaises(TypeError, basestring.__new__, str, "hello")

    def test_pylegacy_basestring_contructor_error_invalid_object(self):
        """Test :class:`basestring` constructor error with invalid object."""

        from pylegacy.builtins import basestring
        self.assertRaises(TypeError, basestring.__new__, 1)

    def test_pylegacy_basestring_contructor_error_invalid_type(self):
        """Test :class:`basestring` constructor error with invalid type."""

        from pylegacy.builtins import basestring
        self.assertRaises(TypeError, basestring.__new__, int, 1)

    def test_pylegacy_basestring_setattr_error(self):
        """Test :class:`basestring` error if trying to set attributes"""

        from pylegacy.builtins import basestring

        def test_callable():
            """Helper function."""
            basestring.x = 1

        self.assertRaises(TypeError, test_callable)

    def test_pylegacy_basestring_isinstance_true(self):
        """Assert that Python 3 strings are recognised as basestrings."""

        from pylegacy.builtins import basestring
        self.assertIsInstance("hello", basestring)

    def test_pylegacy_basestring_isinstance_false(self):
        """Assert that bytes are recognised as basestrings only in Python 2."""

        from pylegacy.builtins import basestring
        result = (sys.version_info[0] < 3)
        self.assertTrue(isinstance(b"hello", basestring) is result)

    def test_pylegacy_basestring_issubclass_true(self):
        """Assert that `str` is a subclass of `basestring`."""

        from pylegacy.builtins import basestring
        self.assertTrue(issubclass(str, basestring))

    def test_pylegacy_basestring_issubclass_false(self):
        """Assert that `bytes` is a subclass of `basestring` only in Python 2."""

        from pylegacy.builtins import basestring
        result = (sys.version_info[0] < 3)
        self.assertTrue(issubclass(bytes, basestring) is result)


if __name__ == "__main__":
    unittest.main()
