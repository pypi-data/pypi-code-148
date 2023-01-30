import logging
import os
from datetime import datetime


class VisitNotFound(Exception):
    pass


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
def get_visit_year(beamline, visit):
    # Get the visit's year.
    date = datetime.now()
    earliest_year = 2000
    found = False
    for year in range(date.year, earliest_year - 1, -1):
        visit_directory = f"/dls/{beamline}/data/{year}/{visit}"
        if os.path.isdir(visit_directory):
            found = True
            break
    if not found:
        raise VisitNotFound(
            f"could not find visit {visit}"
            f" for any year between {date.year} back to {earliest_year}"
        )

    logger.info(f"visit directory determined to be {visit_directory}")

    return year
