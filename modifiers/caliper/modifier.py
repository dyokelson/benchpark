# Copyright 2023 Lawrence Livermore National Security, LLC and other
# Benchpark Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

from ramble.modkit import *
import json


class Caliper(SpackModifier):
    """Define a modifier for Caliper"""

    name = "caliper"

    tags("profiler", "performance-analysis")

    maintainers("pearce8")

    mode("time", description="Platform-independent collection of time")

    _cali_datafile = "{experiment_run_dir}/{experiment_name}.cali"

    # Write experiment metadata to a json file for caliper to add to metadata
    _experiment_metadata_file = "{experiment_run_dir}/{experiment_name}_metadata.json"
    application_name = "{exe_name}"
    experiment_name = "{experiment_name}"
    metadata_dict = {"application_name": application_name, "experiment_name": experiment_name}
    # Serializing json
    json_object = json.dumps(metadata_dict, indent=4)
    # Writing to sample.json
    with open(_experiment_metadata_file, "w") as outfile:
        outfile.write(json_object)

    env_var_modification(
        "CALI_CONFIG",
        "spot(output={}),metadata(file={})".format(_cali_datafile, _experiment_metadata_file),
        #"spot(output={}),metadata(application={})".format(_cali_datafile, application_name),
        method="set",
        modes=["time"],
    )

    archive_pattern(_cali_datafile)

    software_spec("caliper", pkg_spec="caliper")

    required_package("caliper")
