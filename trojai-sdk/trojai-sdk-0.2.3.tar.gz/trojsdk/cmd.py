from trojsdk.core import client_utils
from python_hosts import Hosts, HostsEntry
import webbrowser
import sys


def run(args):
    import subprocess

    with subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as process:
        for line in process.stdout:
            print(line.decode("utf8"), end="")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="trojsdk", description="Troj sdk command line utils"
    )
    parser.add_argument(
        "-config", metavar="-c", type=str, help="Path to the config file"
    )
    parser.add_argument(
        "-test", action="store_true", help="Run tests with TrojAI supplied configs."
    )
    parser.add_argument("-gp", action="store_true", help="Get pods")
    parser.add_argument("-gpw", action="store_true", help="Get pods watch")
    parser.add_argument("-nossl", action="store_true", help="No ssl flag")
    parser.add_argument(
        "-minio",
        nargs="?",
        const="127.0.0.1",
        metavar="IP ADDRESS",
        type=str,
        help=argparse.SUPPRESS,
        # help="Install the host entry and open the MinIO dashboard for the local cluster. Default value of 127.0.0.1.",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.test:
        docker_metadata = {
            "docker_image_url": "trojai/troj-engine-base-tabular:5ff25917a36c1480a82be756ddf77dbac1bf55f0",
            "docker_secret_name": "trojaicreds",
        }
        config = {
            "test_run_name": "test_run_audit",
            "task_type": "tabular",
            "subtask": "regression",
            "audit": "true",
            "attacks": [
                {
                    "attack_name": "FeatureToNan",
                    "display_name": "Feature to NaN attack on age feature",
                    "column_names": ["age"],
                    "attack_kwargs": {"rmse_thresh": 2000},
                },
                {
                    "attack_name": "AbsurdValue",
                    "display_name": "Absurd value attack on smoker feature",
                    "column_names": ["smoker"],
                    "attack_kwargs": {"rmse_thresh": 2000},
                },
                {
                    "attack_name": "AbsurdValue",
                    "display_name": "Absurd value attack on region feature",
                    "column_names": ["region"],
                    "attack_kwargs": {"rmse_thresh": 2000},
                },
                {
                    "attack_name": "NumberToString",
                    "display_name": "Number to string attack attack on children feature",
                    "column_names": ["children"],
                    "attack_kwargs": {"rmse_thresh": 2000},
                },
                {
                    "attack_name": "ScaleShift",
                    "display_name": "Scale shift attack on bmi feature",
                    "column_names": ["bmi"],
                    "attack_kwargs": {"rmse_thresh": 2000},
                },
            ],
            "run_attacks_from_model_profile": "true",
            "integrity_checks": [{"check_name": "EppsSingletonDriftCheck"}],
            "dataset": {
                "name": "insurance_test_dataset",
                "path_to_data": "s3://trojai-object-storage/medical_insurance/data/insurance_test.csv",
                "data_loader_config": {"batch_size": 3, "shuffle": "false"},
                "label_column": "charges",
            },
            "train_dataset": {
                "name": "insurance_train_dataset",
                "path_to_data": "s3://trojai-object-storage/medical_insurance/data/insurance_train.csv",
                "data_loader_config": {"batch_size": 3, "shuffle": "false"},
                "label_column": "charges",
            },
            "deploy_dataset": {
                "name": "insurance_train_dataset",
                "path_to_data": "s3://trojai-object-storage/medical_insurance/data/insurance_test.csv",
                "data_loader_config": {"batch_size": 3, "shuffle": "false"},
                "label_column": "charges",
            },
            "model": {
                "name": "polynomial_regression",
                "path_to_model_file": "s3://trojai-object-storage/medical_insurance/model/model.py",
                "model_args_dict": {
                    "path_to_model_file": "s3://trojai-object-storage/medical_insurance/model/model.pkl",
                    "path_to_polynomial": "s3://trojai-object-storage/medical_insurance/model/polynomial.pkl",
                },
            },
            "auth_config": {
                "api_endpoint": "http://localhost/api/v1",
                "auth_keys": {
                    "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMGI4MGFmNC00MDIxLTExZWQtYjg3OC0wMjQyYWMxMjAwMDIiLCJ1c2VybmFtZSI6InRyb2prOHMiLCJlbWFpbCI6Im5vcmVwbHlAdHJvai5haSIsImlhdCI6MTUxNjIzOTAyMn0._xCVejGSmTrgst2JQOSUzC9AHzvqjkO-YyXJCAyndE4",
                    "refresh_token": "undefined",
                    "api_key": "undefined",
                },
                "secrets": {
                    "AWS_ACCESS_KEY_ID": "AKIAQASF3SJBUF24YMZI",
                    "AWS_SECRET_ACCESS_KEY": "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",
                },
                "project_name": "medical_insurance_estimation",
                "dataset_name": "medical_insurance_data",
            },
            "docker_metadata": {
                "docker_image_url": "trojai/troj-engine-base-tabular:76ec58dc36215953c6a56d84194428ea179e1467",
                "docker_secret_name": "trojaicreds",
                "image_pull_policy": "IfNotPresent",
            },
        }
        client_utils.submit_evaluation(
            config=config, docker_metadata=docker_metadata, nossl=args.nossl
        )

        print("Test finished")
        exit()

    if args.gp:
        import subprocess

        # open kubectl get pods -n=trojai
        process = run(["kubectl", "get", "pods", "-n=trojai"])

    if args.gpw:
        # open kubectl get pods -n=trojai -w
        try: 
            process = run(["kubectl", "get", "pods", "-n=trojai", "-w"])
        except KeyboardInterrupt:
            print("Exiting watch...")

    if args.config:
        client_utils.submit_evaluation(path_to_config=args.config, nossl=args.nossl)

    if args.minio:
        address = args.minio
        name = "trojai.minio"
        comment = "Trojai MinIO host"

        hosts = Hosts()
        hosts.remove_all_matching(comment=comment)

        try:
            host_entry = HostsEntry(
                entry_type="ipv4", address=address, names=[name], comment=comment
            )
        except Exception as e:
            try:
                host_entry = HostsEntry(
                    entry_type="ipv6", address=address, names=[name], comment=comment
                )
            except Exception as e2:
                raise e from e2

        hosts.add([host_entry])
        hosts.write()
        webbrowser.open_new_tab("http://" + name)


if __name__ == "__main__":
    main()
