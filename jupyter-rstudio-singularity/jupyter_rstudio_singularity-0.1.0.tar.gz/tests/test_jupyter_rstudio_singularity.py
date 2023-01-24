#!/usr/bin/env python

"""Tests for `jupyter_rstudio_singularity` package."""


import unittest
from click.testing import CliRunner

from jupyter_rstudio_singularity import jupyter_rstudio_singularity
from jupyter_rstudio_singularity import cli


class TestJupyter_rstudio_singularity(unittest.TestCase):
    """Tests for `jupyter_rstudio_singularity` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert "jupyter_rstudio_singularity.cli.main" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output
