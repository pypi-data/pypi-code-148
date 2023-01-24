"""Console script for jupyter_rstudio_singularity."""
import sys
import click
import typer
import socket
import socket
from contextlib import closing

from prefect import flow, task
import os
import tempfile
from jupyter_rstudio_singularity.utils.logging import setup_logger

"""
The origins of this script come from:

https://rocker-project.org/use/singularity.html#running-a-rocker-singularity-container-localhost-no-password

#!/bin/sh
#SBATCH --time=08:00:00
#SBATCH --signal=USR2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8192
#SBATCH --output=/home/%u/rstudio-server.job.%j
# customize --output path as appropriate (to a directory readable only by the user!)

# Create temporary directory to be populated with directories to bind-mount in the container
# where writable file systems are necessary. Adjust path as appropriate for your computing environment.
workdir=$(python -c 'import tempfile; print(tempfile.mkdtemp())')

mkdir -p -m 700 ${workdir}/run ${workdir}/tmp ${workdir}/var/lib/rstudio-server
cat > ${workdir}/database.conf <<END
provider=sqlite
directory=/var/lib/rstudio-server
END

# Set OMP_NUM_THREADS to prevent OpenBLAS (and any other OpenMP-enhanced
# libraries used by R) from spawning more threads than the number of processors
# allocated to the job.
#
# Set R_LIBS_USER to a path specific to rocker/rstudio to avoid conflicts with
# personal libraries from any R installation in the host environment

cat > ${workdir}/rsession.sh <<END
#!/bin/sh
export OMP_NUM_THREADS=${SLURM_JOB_CPUS_PER_NODE}
export R_LIBS_USER=${HOME}/R/rocker-rstudio/4.2
exec /usr/lib/rstudio-server/bin/rsession "\${@}"
END

chmod +x ${workdir}/rsession.sh

export SINGULARITY_BIND="${workdir}/run:/run,${workdir}/tmp:/tmp,${workdir}/database.conf:/etc/rstudio/database.conf,${workdir}/rsession.sh:/etc/rstudio/rsession.sh,${workdir}/var/lib/rstudio-server:/var/lib/rstudio-server"

# Do not suspend idle sessions.
# Alternative to setting session-timeout-minutes=0 in /etc/rstudio/rsession.conf
# https://github.com/rstudio/rstudio/blob/v1.4.1106/src/cpp/server/ServerSessionManager.cpp#L126
export SINGULARITYENV_RSTUDIO_SESSION_TIMEOUT=0

export SINGULARITYENV_USER=$(id -un)
export SINGULARITYENV_PASSWORD=$(openssl rand -base64 15)
# get unused socket per https://unix.stackexchange.com/a/132524
# tiny race condition between the python & singularity commands
readonly PORT=$(python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')

cat 1>&2 <<END
1. SSH tunnel from your workstation using the following command:

   ssh -N -L 8787:${HOSTNAME}:${PORT} ${SINGULARITYENV_USER}@LOGIN-HOST

   and point your web browser to http://localhost:8787

2. log in to RStudio Server using the following credentials:

   user: ${SINGULARITYENV_USER}
   password: ${SINGULARITYENV_PASSWORD}

When done using RStudio Server, terminate the job by:

1. Exit the RStudio Session ("power" button in the top right corner of the RStudio window)
2. Issue the following command on the login node:

      scancel -f ${SLURM_JOB_ID}
END

            #--auth-pam-helper-path=pam-helper \

export IMAGE="r-tidyverse_4.2.2.sif"

singularity exec --cleanenv ${IMAGE} \
    /usr/lib/rstudio-server/bin/rserver \
            --www-port ${PORT} \
            --www-root-path=/user/${USER}/proxy/${PORT}/ \
            --server-user=${USER} \
            --auth-none=1 \
            --www-frame-origin=same \
            --www-verify-user-agent=0 \
            --rsession-path=/etc/rstudio/rsession.sh
printf 'rserver exited' 1>&2
"""

logger = setup_logger()
WORKDIR = tempfile.mkdtemp()

HOME = os.environ.get("HOME")
USER = os.environ.get("USER")

app = typer.Typer()


def find_free_port():
    """Find and return a free port number.
    Shout-out to https://stackoverflow.com/a/45690594/1931274!
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def prepare_dirs(workdir: str):
    return shell_run_command(
        command=f"mkdir -p -m 700 {workdir}/run {workdir}/tmp {workdir}/var/lib/rstudio-server",
        return_all=True,
    )


def prepare_db_config(workdir: str) -> str:
    s = """provider=sqlite
directory=/var/lib/rstudio-server"""
    os.makedirs(workdir, exist_ok=True)
    database_conf = os.path.join(workdir, "database.conf")
    with open(os.path.join(workdir, "database.conf"), "w") as fh:
        fh.write(s)
    os.system(f"chmod 777 {database_conf}")
    return database_conf


def prepare_rsession_script(workdir: str, r_lib: str) -> str:
    s = [
        "#!/bin/sh"
        "export OMP_NUM_THREADS=${SLURM_JOB_CPUS_PER_NODE}"
        f"export R_LIBS_USER={r_lib}",
        'exec /usr/lib/rstudio-server/bin/rsession "\${@}"',
    ]

    os.makedirs(workdir, exist_ok=True)
    rsession_script = os.path.join(workdir, "rsession.sh")
    with open(rsession_script, "w") as fh:
        fh.write("\n".join(s))
    return rsession_script


@flow
def run_rsession(workdir: str, r_lib: str, image: str, port: int, url_prefix: str):
    logger.info(f"Launching RStudio at: {url_prefix}")
    command = f"""#!/usr/bin/env bash
export SINGULARITY_BIND="{workdir}/run:/run,{workdir}/tmp:/tmp,{workdir}/database.conf:/etc/rstudio/database.conf,{workdir}/rsession.sh:/etc/rstudio/rsession.sh,{workdir}/var/lib/rstudio-server:/var/lib/rstudio-server"
export PORT={port}

export SINGULARITYENV_USER=$(id -un)
export SINGULARITYENV_PASSWORD=$(openssl rand -base64 15)

singularity exec --cleanenv {image} \\
    /usr/lib/rstudio-server/bin/rserver \\
            --www-port {port} \\
            --www-root-path={url_prefix} \\
            --server-user={USER} \\
            --auth-none=1 \\
            --www-frame-origin=same \\
            --www-verify-user-agent=0 \\
            --rsession-path=/etc/rstudio/rsession.sh
    """
    run_session_script = os.path.join(workdir, "run-rsession.sh")
    with open(run_session_script, "w") as fh:
        fh.write(command)
    os.system(f"chmod 777 {run_session_script}")
    return


@flow
def prepare_rsession(workdir: str, r_lib: str):
    logger.info(
        f"Preparing RStudio session. Scripts and configuration are in: {workdir}"
    )
    prepare_dirs(workdir=workdir)
    prepare_db_config(workdir=workdir)
    prepare_rsession_script(workdir=workdir, r_lib=r_lib)

    return


@flow
def sanity_check_singularity_image(remote_image: str, image: str):
    image = os.path.abspath(image)
    image_dir = os.path.dirname(image)
    if not os.path.exists(image):
        logger.info("Local image doesn't exist. Pulling...")
        os.makedirs(image_dir)
        return shell_run_command(
            command=f"cd {image_dir} && singularity pull {remote_image}",
            return_all=True,
        )
    else:
        logger.info("Local image exists.")
        return True


@app.command()
def main(
    remote_image: str = typer.Option(
        "docker://dabbleofdevops/r-tidyverse:4.2.2",
        help="""Path to the remote image.
             If the local image does not exist
             we will pull the image from the remote.""",
    ),
    image: str = typer.Option("r-tidyverse_4.2.2.sif", help="Path to local image"),
    r_lib: str = typer.Option(
        os.path.join(os.environ.get["HOME"], "R", "rocker-rstudio", "4.2.2"),
        help="""Path to persist R libraries to.""",
    ),
    workdir: str = typer.Option(
        WORKDIR,
        help="Path to write out rstudio config files. Default is a temp directory.",
    ),
    port: int = typer.Option(
        find_free_port(),
        help="""Port to launch Rstudio with.
                             You can specify a port, or the program will find a free port for you.""",
    ),
):
    """Console script for jupyter_rstudio_singularity."""
    image = os.path.abspath(image)
    image_dir = os.path.dirname(image)
    os.makedirs(workdir, exist_ok=True)
    if not os.path.exists(image):
        os.makedirs(image_dir)
    url_prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/").rstrip("/")
    url_prefix = f"{url_prefix}/proxy/{port}/"
    sanity_check_singularity_image(remote_image=remote_image, image=image)
    prepare_rsession(workdir=workdir, r_lib=r_lib)
    run_rsession(
        workdir=workdir,
        r_lib=rlib,
        image=image,
        port=port,
        url_prefix=url_prefix,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
