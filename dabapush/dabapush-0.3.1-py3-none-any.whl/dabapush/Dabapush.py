"""Dabapush is the main application class of this project.


"""
from pathlib import Path
import yaml
from loguru import logger as log

from .Configuration.ProjectConfiguration import ProjectConfiguration

class Dabapush(object):
    """This is the main class for this application.

    It is a Singleton pattern class and follows the interface pattern as well.

    Parameters
    ----------

    Returns
    -------

    """

    __instance__ = None

    def __new__(
        cls,
        install_dir: Path = Path(__file__).parent.parent,
        working_dir: Path = Path().resolve(),  # automagically defaults to cwd
    ):
        if cls.__instance__ is None:
            cls.__instance__ = super(Dabapush, cls).__new__(cls)
            # init code here: ...
            cls.__instance__.working_dir = working_dir
            cls.__instance__.install_dir = install_dir
            # load global config
            cls.__instance__.gc_load()
            if not cls.__instance__.pr_read():
                cls.__instance__.pr_init()
            log.debug(
                f"Staring DabaPush instance with gc: {cls.__instance__.global_config} and cf: {cls.__instance__.config}"
            )
        return cls.__instance__

    def update_reader_targets(self, name: str) -> None:
        """

        Parameters
        ----------
        name :
            str:
        name :
            str:
        name: str :


        Returns
        -------

        """
        pass

    # PROJECT specific methods
    def pr_init(self):
        """Initialize a new project in the current directory"""
        self.config = ProjectConfiguration()
        # self.pr_write()

    def pr_write(self):
        """Write the current configuration to the project configuration file in the current directory"""
        if self.config is not None:
            conf_path = self.working_dir / "dabapush.yml"
            log.debug(f"writing the following project configuration: {self.config}")
            with conf_path.open("w") as file:
                yaml.dump(self.config, file)

    def pr_read(self) -> bool:
        """Read the project configuration file in the current directory

        Parameters
        ----------

        Returns
        -------
        type
            bool Indicates wether loading load successful

        """
        conf_path = self.working_dir / "dabapush.yml"
        if conf_path.exists():
            with conf_path.open("r") as file:
                self.config = yaml.full_load(file)
            return True
        else:
            return False

    # READER specific methods
    def rd_add(self, reader: str, name: str):
        """add a reader to the current project

        Parameters
        ----------
        reader :
            str:
        name :
            str:

        Returns
        -------

        """
        self.config.add_reader(reader, name)

    def rd_list(self):
        """Lists all available readers"""
        return self.global_config.list_all_readers()

    def rd_rm(self, name: str):
        """remove a reader from the current configuration"""
        if name in self.config.readers:
            self.config.readers.__delitem__(name)
        else:
            log.warning(f"Cannot delete {name} as it does not exist.")

    def rd_update(self, name: str, config: dict[str, str]):
        """update a reader's configuration"""
        obj = self.config.readers[name] if name in self.config.readers else None

        if obj is not None:
            for k, v in config.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
                else:
                    log.warning(f"key {k} not valid in type: {obj.__class__.__name__}")

    # WRITER specific methods
    def wr_add(self, type: str, name: str):
        """add a reader to the current project"""
        self.config.add_writer(type, name)

    def wr_rm(self, name: str):
        """remove a reader from the current configuration"""
        if name in self.config.readers:
            self.config.readers.__delitem__(name)
        else:
            log.warning(f"Cannot delete {name} as it does not exist.")

    def wr_update(self, name: str, config: dict[str, str]):
        """update a reader's configuration"""
        obj = self.config.writers[name] if name in self.config.readers else None

        if obj is not None:
            for k, v in config.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
                else:
                    log.warning(f"key {k} not valid in type: {obj.__class__.__name__}")

    def wr_list(self):
        """Lists all available readers"""
        return self.global_config.list_all_writers()

    # JOB specific methods
    def jb_run(self, targets: list[str]):
        """runs the job(s) configured in the current directory

        Parameters
        ----------
        targets :
            list[str]:

        Returns
        -------

        """
        conf_targets = [reader for reader in self.config.readers]

        if len(conf_targets) == 0:
            log.error("No jobs are configured. Nothing to run.")
            return
        # single dispatch all jobs
        if len(targets) == 1 and targets[0] == "all":
            log.debug(f'Running all jobs: {", ".join(conf_targets)}.')
            [self.__dispatch_job__(target) for target in conf_targets]
        # run multiple jobs
        else:
            for target in targets:
                if target in conf_targets:
                    self.__dispatch_job__(target)
                else:
                    # run specific jop
                    log.error(
                        f"Target {target} is not configured. Consider adding it yourself."
                    )

    def __dispatch_job__(self, target: str) -> None:
        # find all candidate files
        # process them accordingly
        # finish
        log.info(f"Dispatching job for {target}")
        reader = self.config.readers[target].get_instance()
        writer = self.config.writers[target].get_instance()
        writer.write(reader.read())

    def jb_update(self):
        """update the current job's targets"""
        pass

    def gc_load(self):
        """load the global registry and configuration"""
        conf_path = self.install_dir / "config.yml"
        with conf_path.open("r") as file:
            self.global_config = yaml.full_load(file)
