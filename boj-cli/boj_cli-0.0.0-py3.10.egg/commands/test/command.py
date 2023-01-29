import time
from rich.console import Console
import yaml
from boj.commands.run import runner
import boj.core.util as util
import json


def run(args):
    console = Console(log_time=False, log_path=False)

    with console.status(
        "[bold yellow]Loading source file...",
        spinner_style="white",
    ) as status:
        problem = util.read_solution(args.file)
        time.sleep(0.4)

        console.log("[white]Loaded source file.")

        status.update("[bold yellow]Loading configuration...")
        time.sleep(0.3)

        try:
            global config
            f = util.read_file(util.config_file_path(), "r")
            config = json.loads(f)
        except:
            status.stop()
            console.print("[red]Config file is not found.")
            exit(1)

        if "filetype" not in config or problem.filetype not in config["filetype"]:
            status.stop()
            console.print("[red]Configuration is not found")
            exit(1)

        filetype_config = config["filetype"][problem.filetype]

        console.log("[white]Loaded configuration.")

        status.update("[bold yellow]Loading testcases...")
        with open("testcase.yaml", "r") as stream:
            try:
                global testcases
                testcases = yaml.safe_load(stream)
            except:
                status.stop()
                console.print("[red]Run command not found.")
                exit(1)

        console.log("[white]Loaded testcases.")
        time.sleep(0.2)

    if filetype_config["compile"]:
        status.update("[bold yellow]Compiling...")
        command = filetype_config["compile"]
        runner.compile(command, args.file)


    if not filetype_config["run"]:
        console.print("[red]Run command not found.")
        exit(1)

    command = filetype_config["run"]
    runner.run_test(command, args.file, testcases)

