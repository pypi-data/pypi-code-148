#!/usr/bin/env python3
# (C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import climetlab as cml


def test_source():
    ds = cml.load_source(
        "google-drive",
        file_id="1PCkX-c1HQCjvmEmGJLyhPqhEGp6oVPiM",
    )
    # IFAB pointwise postprocessing
    # Trying to improve the IFS forecast at station observations.
    # Observations are sparse in time and space so a local approach is the natural one.
    # This means the problem is small, suitable for a RF/regression/MLP.
    # Lots of IFS model fields, so things can be done with interpretability, or holding out key predictors.
    
    for arr in ds:
        nparr = arr.to_numpy()
        print(nparr)


if __name__ == "__main__":
    test_source()
