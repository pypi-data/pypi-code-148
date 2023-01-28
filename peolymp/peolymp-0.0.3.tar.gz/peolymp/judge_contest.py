from eolymp.judge import judge_pb2, acl_pb2
from eolymp.judge.acl_http import AclClient

from peolymp.judge import JudgeAPI
from peolymp.utils import download_sources_by_data


class JudgeContestAPI(JudgeAPI):

    def __init__(self, contest_id, **kwargs):
        super(JudgeContestAPI, self).__init__(**kwargs)
        self.contest_id = contest_id
        self.contest = self.client.DescribeContest(judge_pb2.DescribeContestInput(contest_id=contest_id)).contest
        self.client_acl = AclClient(self.http_client, url=self.contest.url)

    def add_admin(self, user_id):
        self.client_acl.GrantPermission(acl_pb2.GrantPermissionInput(user_id=user_id, role="ADMIN"))

    def add_participant(self, **kwargs):
        return super().add_participant(contest_id=self.contest_id, **kwargs)

    def add_problem(self, **kwargs):
        return super().add_problem(contest_id=self.contest_id, **kwargs)

    def sync_problem(self, **kwargs):
        return super().sync_problem(contest_id=self.contest_id, **kwargs)

    def sync_all_problems(self, **kwargs):
        return super().sync_all_problems(contest_id=self.contest_id, **kwargs)

    def lock_participant_by_id(self, **kwargs):
        return super().lock_participant_by_id(contest_id=self.contest_id, **kwargs)

    def get_contest(self, **kwargs):
        return super().get_contest(contest_id=self.contest_id, **kwargs)

    def delete_contest(self):
        return super().delete_contest(contest_id=self.contest_id)

    def get_problems(self):
        return super().get_problems(contest_id=self.contest_id)

    def get_scoring(self):
        return super().get_scoring(contest_id=self.contest_id)

    def allow_upsolve(self):
        return super().allow_upsolve(contest_id=self.contest_id)

    def get_participant(self, **kwargs):
        return super().get_participant(contest_id=self.contest_id, **kwargs)

    def get_participants(self):
        return super().get_participants(contest_id=self.contest_id)

    def get_submissions(self):
        return super().get_submissions(contest_id=self.contest_id)

    def rejudge_problem(self, **kwargs):
        return super().rejudge_problem(contest_id=self.contest_id, **kwargs)

    def download_sources(self, dest):
        return download_sources_by_data(dest, self.contest, self.get_problems(),
                                        self.get_participants(),
                                        self.get_submissions())
