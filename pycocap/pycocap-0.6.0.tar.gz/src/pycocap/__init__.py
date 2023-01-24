# -*- coding: utf-8 -*-
"""
Purpose
=======

pyCOCAP is the Python interface to the common COCAP database.

Functions
=========

.. currentmodule:: pycocap.pycocap

.. autosummary::
    :toctree: generated

    cases
    deaths
    R
    npi
    npis
    hospital_daily_occupancy
    hospital_weekly_admissions
    icu_daily_occupancy
    icu_weekly_admissions
    vaccinations_daily
    vaccinations_people
    vaccinations_people_fully
    vaccinations_total
    vaccinations_total_booster
    reports
    timeseries
"""

from pycocap import pycocap
from pycocap.pycocap import (
    cases,
    deaths,
    hospital_daily_occupancy,
    hospital_weekly_admissions,
    icu_daily_occupancy,
    icu_weekly_admissions,
    npi,
    npis,
    R,
    reports,
    vaccinations_daily,
    vaccinations_people,
    vaccinations_people_fully,
    vaccinations_total,
    vaccinations_total_booster,
)

try:
    from pycocap._version import __version__
except ModuleNotFoundError:
    # package is not installed
    __version__ = '0.0.0.dev0'

__all__ = ['__version__']
__all__ += [
    'cases',
    'deaths',
    'hospital_daily_occupancy',
    'hospital_weekly_admissions',
    'icu_daily_occupancy',
    'icu_weekly_admissions',
    'npi',
    'npis',
    'R',
    'reports',
    'vaccinations_daily',
    'vaccinations_people',
    'vaccinations_people_fully',
    'vaccinations_total',
    'vaccinations_total_booster',
]
