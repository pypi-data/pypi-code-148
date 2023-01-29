import git
from script_master_helper.executor.schemas import GitSchema

from process_executor.app import logger
from process_executor.settings import Settings


class Repo:
    def __init__(self, schema: GitSchema):
        self.schema = schema
        self.name = schema.get_repo_name()
        self.path = Settings().scripts_dir / self.name

    def clone_or_pull(self):
        if self.path.exists():
            logger.info(f"Repository pull {self.path}")
            repo = git.Repo.init(self.path)
            repo.remotes.origin.pull()
        else:
            logger.info(f"Repository clone {self.schema.url} to {self.path}")
            repo = git.Repo.clone_from(self.schema.url, self.path)

        return repo
