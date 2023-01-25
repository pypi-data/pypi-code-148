# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fhirstarter',
 'fhirstarter.fhir_specification',
 'fhirstarter.scripts',
 'fhirstarter.tests']

package_data = \
{'': ['*'], 'fhirstarter.fhir_specification': ['examples/*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'fhir.resources>=6.4.0,<6.5.0',
 'lxml>=4.9.2,<5.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvloop>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'fhirstarter',
    'version': '0.13.4',
    'description': 'An ASGI FHIR API framework built on top of FastAPI and FHIR Resources',
    'long_description': '# fhirstarter\n\n<p>\n  <a href="https://github.com/canvas-medical/fhirstarter/actions/workflows/test.yml">\n    <img src="https://github.com/canvas-medical/fhirstarter/actions/workflows/test.yml/badge.svg">\n  </a>\n  <a href="https://pypi.org/project/fhirstarter/">\n    <img src="https://img.shields.io/pypi/v/fhirstarter">\n  </a>\n  <a href="https://pypi.org/project/fhirstarter/">\n    <img src="https://img.shields.io/pypi/pyversions/fhirstarter">\n  </a>\n  <a href="https://pypi.org/project/fhirstarter/">\n    <img src="https://img.shields.io/pypi/l/fhirstarter">\n  </a>\n  <a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000">\n  </a>\n</p>\n\nAn ASGI FHIR API framework built on top of [FastAPI](https://fastapi.tiangolo.com) and\n[FHIR Resources](https://pypi.org/project/fhir.resources/).\n\nThe only version of FHIR that is currently supported is 4.0.1.\n\n## Installation\n\n```bash\npip install fhirstarter\n```\n\n## Features\n\n* Automatic, standardized API route creation\n* Automatic validation of inputs and outputs through the use of FHIR Resources Pydantic models\n* Automatically-generated capability statement that can be customized, and a capability statement\n  API route\n* An exception-handling framework that produces FHIR-friendly responses (i.e. OperationOutcomes)\n* Automatically-generated, integrated documentation generated from the FHIR specification\n* Custom search parameters for search endpoints\n\n### Disclaimer\n\nFHIRStarter was built based on the business needs of Canvas Medical. At any point in time, it may\nnot be broadly applicable to the industry at large. Canvas Medical open-sourced the project so that\nit can be used by healthcare software developers whose needs it might also meet. Ongoing support and\ndevelopment will be based on the business needs of Canvas Medical.\n\n## Background\n\nFHIRStarter uses a provider-decorator pattern. Developers can write functions that implement FHIR\ninteractions -- such as create, read, search-type, and update -- and plug them into the framework.\nFHIRStarter then automatically creates FHIR-compatible API routes from these developer-provided\nfunctions. FHIR interactions that are supplied must use the resource classes defined by the\n[FHIR Resources](https://pypi.org/project/fhir.resources/) Python package, which is a collection of\nPydantic models for FHIR resources.\n\nIn order to stand up a FHIR server, all that is required is to create a FHIRStarter and a\nFHIRProvider instance, register a FHIR interaction with the provider, add the provider to the\nFHIRStarter instance, and pass the FHIRStarter instance to an ASGI server.\n\n## Usage\n\n### Currently-supported functionality\n\nFHIRStarter supports create, read, search-type, and update endpoints across all FHIR R4 resource\ntypes, and will automatically generate the `/metadata` capabilities statement endpoint.\n\n### Example\n\nA detailed example is available here: \n[fhirstarter/scripts/example.py](fhirstarter/scripts/example.py).\n\n```python\nimport uvicorn\nfrom fhir.resources.fhirtypes import Id\nfrom fhir.resources.patient import Patient\n\nfrom fhirstarter import FHIRProvider, FHIRStarter, InteractionContext\nfrom fhirstarter.exceptions import FHIRResourceNotFoundError\n\n# Create the app\napp = FHIRStarter()\n\n# Create a provider\nprovider = FHIRProvider()\n\n\n# Register the patient read FHIR interaction with the provider\n@provider.read(Patient)\nasync def patient_read(context: InteractionContext, id_: Id) -> Patient:\n    # Get the patient from the database\n    patient = ...\n\n    if not patient:\n        raise FHIRResourceNotFoundError\n\n    return Patient(\n        **{\n            # Map patient from database to FHIR Patient structure\n        }\n    )\n\n\n# Add the provider to the app\napp.add_providers(provider)\n\n\nif __name__ == "__main__":\n    # Start the server\n    uvicorn.run(app)\n```\n\n### Custom search parameters\n\nCustom search parameters can be defined in a configuration file that can be passed to the app on\ncreation.\n\n```toml\n[search-parameters.Patient.nickname]\ntype = "string"\ndescription = "Nickname"\nuri = "https://hostname/nickname"\ninclude-in-capability-statement = true\n```\n\nAdding a custom search parameter via configuration allows this name to be used as an argument when\ndefining a search-type interaction handler and also adds this search parameter to the API\ndocumentation for the search endpoint.\n\n### Capability statement\n\nIt is possible to customize the capability statement by setting a capability statement modifier:\n\n```python\ndef amend_capability_statement(\n    capability_statement: MutableMapping[str, Any], request: Request, response: Response\n) -> MutableMapping[str, Any]:\n    capability_statement["publisher"] = "Canvas Medical"\n    return capability_statement\n\napp.set_capability_statement_modifier(amend_capability_statement)\n```\n\n### FastAPI dependency injection\n\nFastAPI\'s dependency injection is exposed at various levels:\n\n* **application**: the `__init__` method on the FHIRStarter class\n* **provider**: the `__init__` method on the FHIRProvider class\n* **handler**: the `create`, `read`, `search_type`, or `update` decorator used to add a handler to a provider\n\nDependencies specified at the application level will be injected into all routes in the application.\n\nDependencies specified at the provider level will be injected into all routes that are added to\nthe application from that specific provider.\n\nDependencies specified at the handler level only apply to that specific FHIR interaction.\n\n## Forward compatibility\n\nAt some point in the future, it will be necessary to support FHIR R5. How this might be supported on\na server that continues to support R4 has not yet been determined (e.g. a header that specifies the\nversion, adding the FHIR version to the URL path, etc.). It may be necessary to support alteration\nof how the URL path is specified through the provider construct. Currently, the FHIR version is not\npart of the URL path, so the default behavior is that an API route defined as `/Patient` will be an\nR4 endpoint.\n',
    'author': 'Christopher Sande',
    'author_email': 'christopher.sande@canvasmedical.com',
    'maintainer': 'Canvas Medical Engineering',
    'maintainer_email': 'engineering@canvasmedical.com',
    'url': 'https://github.com/canvas-medical/fhirstarter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
