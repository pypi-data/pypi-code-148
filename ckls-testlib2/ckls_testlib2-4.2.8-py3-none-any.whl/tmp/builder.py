import os
import shutil
import subprocess
import sys
import nbformat
from pyspark.sql import SparkSession

from tmp.nb_nodes import Nodes


def nbformat_to_ipynb(out_path, nb):
    with open(out_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def ipynb_to_nbformat(in_path):
    with open(in_path) as f:
        return nbformat.read(f, as_version=4)


def log_process(result: subprocess.CompletedProcess):
    print("______________STDOUT:")
    print(result.stdout.decode())
    print("______________STDERR:")
    print(result.stderr.decode())


drive_folder = 'https://drive.google.com/drive/folders/1MCQqsoZB4UAZuZuvvKrCwt3tj2oyJyEW?usp=share_link'

repo_root = '/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696'
python_root = f'{repo_root}/python'
java_location = '/home/ckl/.jdks/corretto-1.8.0_352/bin/java'
sbt_jar_location = '/home/ckl/.local/share/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5921.22.plugins/Scala/launcher/sbt-launch.jar'
scala_target_dir = f'{repo_root}/target/scala-2.12/'
python_dist_dir = f'{python_root}/dist/'
python_exec = sys.executable

base_notebook = '/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/python/tmp/base_notebook.ipynb'
out_folder = '/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/python/tmp/out_folder'
nb_out_file_name = f'{out_folder}/test_notebook.ipynb'


def make_jar():
    os.chdir(repo_root)

    # 0. CODE AUTH!?!?

    # 1. Make jar
    make_jar_cmd = f'{java_location} -jar {sbt_jar_location} assembly'

    r = subprocess.run([java_location, f'-jar', sbt_jar_location, 'assembly'], capture_output=True)
    log_process(r)
    # print(make_jar_cmd)

    # 2 Find Jar
    jar_path = next(filter(lambda x: 'spark-nlp-jsl-assembly' in x, os.listdir(scala_target_dir)))
    jar_path = f'{scala_target_dir}/{jar_path}'
    print(f'New Jar in {jar_path}')
    return jar_path


# https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars/spark-nlp-assembly-${env.NLP_VERSION}.jar

def make_wheel():
    shutil.rmtree(python_dist_dir, ignore_errors=True)
    os.chdir(python_root)
    os.system(f'{python_exec} setup.py sdist bdist_wheel ')
    wheel_path = next(filter(lambda x: 'spark_nlp_jsl' in x and '.whl' in x, os.listdir(python_dist_dir)))
    wheel_path = f'{python_dist_dir}/{wheel_path}'
    print(f'New Wheel in {wheel_path}')
    return wheel_path


def make_notebook(enterprise_nlp_secret):
    jar_path = make_jar()
    wheel_path = make_wheel()
    shutil.copy(jar_path, f'{out_folder}sparknlp-jsl.jar')
    shutil.copy(wheel_path, f'{out_folder}/enterprise_nlp.whl')
    # TODO version + branch !?

    # Nodes.auth_with_jsl_lib['source'] = Nodes.auth_with_jsl_lib['source'].replace('<SECRET>', enterprise_nlp_secret)
    # nb = ipynb_to_nbformat(base_notebook)
    # for inject_node in [Nodes.auth_with_jsl_lib, Nodes.get_sample_text_df]:
    #     nb['cells'].insert(len(nb['cells']), inject_node)
    # nbformat_to_ipynb(nb_out_file_name, nb)
    # print('t')


make_notebook('4.2.2-4c5a3dfd6d33f997bd128037de5489f827696641')