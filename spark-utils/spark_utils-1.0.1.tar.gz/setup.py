# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spark_utils',
 'spark_utils.common',
 'spark_utils.dataframes',
 'spark_utils.dataframes.sets',
 'spark_utils.delta_lake',
 'spark_utils.models']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0,<36.1',
 'delta-spark>=2.1.1,<2.2.0',
 'hadoop-fs-wrapper>=0.5.2,<0.6.0']

extras_require = \
{'k8s': ['kubernetes==24.2.0']}

setup_kwargs = {
    'name': 'spark-utils',
    'version': '1.0.1',
    'description': 'Utility classes for comfy Spark job authoriing.',
    'long_description': '# Introduction\n\nUtility functions and classes for working with Dataframes, provisioning SparkSession and much more.\n\nCore features:\n\n- Provisioning Spark session with some routine settings set in advance, including Delta Lake configuration. You must\n  have delta-core jars in class path for this to work.\n- Spark job argument wrappers, allowing to specify job inputs for `spark.read.format(...).options(...).load(...)` and\n  outputs for `spark.write.format(...).save(...)` in a generic way. Those are exposed as `source` and `target` built-in\n  arguments (see example below).\n\nConsider a simple Spark Job that reads `json` data from `source` and stores it as `parquet` in `target`. This job can be\ndefined using `spark-utils` as below:\n\n```python\nfrom spark_utils.common.spark_job_args import SparkJobArgs\nfrom spark_utils.common.spark_session_provider import SparkSessionProvider\n\n\ndef main(args=None):\n    """\n     Job entrypoint\n    :param args:\n    :return:\n    """\n    spark_args = SparkJobArgs().parse(args)\n\n    source_table = spark_args.source(\'json_source\')\n    target_table = spark_args.output(\'parquet_target\')\n\n    # Spark session and hadoop FS\n    spark_session = SparkSessionProvider().get_session()\n    df = spark_session.read.format(source_table.data_format).load(source_table.data_path)\n    df.write.format(target_table.data_format).save(target_table.data_path)\n```\n\nYou can also provision Spark Session using Kubernetes API server as a resource manager. Use Java options from the\nexample below for Java 17 installations:\n\n```python\nfrom spark_utils.common.spark_session_provider import SparkSessionProvider\nfrom spark_utils.models.k8s_config import SparkKubernetesConfig\n\nconfig = {\n    \'spark.local.dir\': \'/tmp\',\n    \'spark.driver.extraJavaOptions\': "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:InitiatingHeapOccupancyPercent=35 -XX:OnOutOfMemoryError=\'kill -9 %p\' -XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED --add-opens=java.base/java.util.stream=ALL-UNNAMED",\n    \'spark.executor.extraJavaOptions\': "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:InitiatingHeapOccupancyPercent=35 -XX:OnOutOfMemoryError=\'kill -9 %p\' -XX:+IgnoreUnrecognizedVMOptions --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED --add-opens=java.base/java.util.stream=ALL-UNNAMED",\n    \'spark.executor.instances\': \'5\'\n}\n\nspc = SparkKubernetesConfig(\n  application_name=\'test\',\n  k8s_namespace=\'my-spark-namespace\',\n  spark_image=\'myregistry.io/spark:v3.3.1\',\n  executor_node_affinity={\n    \'kubernetes.mycompany.com/sparknodetype\': \'worker\', \n    \'kubernetes.azure.com/scalesetpriority\': \'spot\'\n  },\n  executor_name_prefix=\'spark-k8s-test\'\n)\nssp = SparkSessionProvider(additional_configs=config).configure_for_k8s(\n  master_url=\'https://my-k8s-cluster.mydomain.io\',\n  spark_config=spc\n)\n\nspark_session = ssp.get_session()\n```\n\nNow we can call this job directly or with `spark-submit`. Note that you must have `spark-utils` in PYTHONPATH before\nrunning the script:\n\n```commandline\nspark-submit --master local[*] --deploy-mode client --name simpleJob ~/path/to/main.py --source \'json_source|file://tmp/test_json/*|json\' --output \'parquet_target|file://tmp/test_parquet/*|parquet\'\n```\n\n- Job argument encryption is supported. This functionality requires an encryption key to be present in a cluster\n  environment variable `RUNTIME_ENCRYPTION_KEY`. The only supported algorithm now is `fernet`. You can declare an\n  argument as encrypted using `new_encrypted_arg` function. You then must pass an encrypted value to the declared\n  argument, which will be decrypted by `spark-utils` when a job is executed and passed to the consumer.\n\nFor example, you can pass sensitive spark configuration (storage access keys, hive database passwords etc.) encrypted:\n\n```python\nimport json\n\nfrom spark_utils.common.spark_job_args import SparkJobArgs\nfrom spark_utils.common.spark_session_provider import SparkSessionProvider\n\n\ndef main(args=None):\n    spark_args = SparkJobArgs()\n        .new_encrypted_arg("--custom-config", type=str, default=None,\n                           help="Optional spark configuration flags to pass. Will be treated as an encrypted value.")\n        .parse(args)\n\n    spark_session = SparkSessionProvider(\n        additional_configs=json.loads(\n            spark_args.parsed_args.custom_config) if spark_args.parsed_args.custom_config else None).get_session()\n\n    ...\n```\n\n- Delta Lake utilities\n    - Table publishing to Hive Metastore.\n    - Delta OSS compaction with row count / file optimization target.\n- Models for common data operations like data copying etc. Note that actual code for those operations will be migrated\n  to this repo a bit later.\n- Utility functions for common data operations, for example, flattening parent-child hierarchy, view concatenation,\n  column name clear etc.\n\nThere are so many possibilities with this project - please feel free to open an issue / PR adding new capabilities or\nfixing those nasty bugs!\n\n# Getting Started\n\nSpark Utils must be installed on your cluster or virtual env that Spark is using Python interpreter from:\n\n```commandline\npip install spark-utils\n```\n\n# Build and Test\n\nTest pipeline runs Spark in local mode, so everything can be tested against our current runtime. Update the image used\nin `build.yaml` if you require a test against a different runtime version.\n',
    'author': 'ECCO Sneaks & Data',
    'author_email': 'esdsupport@ecco.com',
    'maintainer': 'GZU',
    'maintainer_email': 'gzu@ecco.com',
    'url': 'https://github.com/SneaksAndData/spark-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
