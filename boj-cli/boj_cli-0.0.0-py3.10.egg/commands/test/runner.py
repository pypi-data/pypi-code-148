from subprocess import Popen, PIPE

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def compile(command, file):
    console = Console(log_time=False, log_path=False)

    try:
        command = command.replace("$file", file)
        process = Popen(
            str.split(command, " "),
            stdout=PIPE,
            stderr=PIPE,
        )

        output, err = process.communicate()
        console.log()

        with console.status("[bold yellow]Compiling..") as status:
            if err:
                console.log("[bold yellow]Compile output:")
                console.log("[white]" + err.decode("utf-8"))

            if output:
                console.log("[bold yellow]Compile output:")
                console.log("[white]" + output.decode("utf-8"))

            if process.returncode != 0:
                status.stop()
                console.print("[red]Compile error.")
                exit(1)

    except Exception as e:
        console.log(e)
        console.print("[red]Compileerror.")

    return


def run_test(command, file, testcase_dict):
    command = command.replace("$file", file)
    testcases = []

    for k in testcase_dict:
        testcases.append(testcase_dict[k])

    run_command(command, testcases)

    #
    # asyncio.run(
    #     run_command_async(
    #         command,
    #         testcases,
    #     )
    # )


def run_command(command, testcases: list):
    progress = Progress(
        SpinnerColumn(style="white", finished_text="•"),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )

    tasks = []
    for t in testcases:
        tasks.append(progress.add_task("Running", total=1))

    with progress:
        for t in testcases:
            process = Popen(
                str.split(command, " "),
                text=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
            )

            input = t["input"] if "input" in t else ""
            answer = t["output"] if "output" in t else ""

            out, err = process.communicate(input=input)
            task_id = tasks[testcases.index(t)]

            if err:
                print("hi")
                progress.update(task_id, description="Error  ")

            if out:
                print(out)
                if answer.rstrip() == out.rstrip():
                    progress.update(task_id, description="Passed ", completed=1)

            if process.returncode != 0:
                print("hi3")
                progress.update(task_id, description="Error  ", completed=1)

    # if stdout:
    #     print(f"[stdout]\n{stdout.decode()}")
    # if stderr:
    #     print(f"[stderr]\n{stderr.decode()}")
