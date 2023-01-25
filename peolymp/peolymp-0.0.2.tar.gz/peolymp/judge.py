import time

from eolymp.judge import judge_pb2, contest_pb2
from eolymp.judge.judge_http import JudgeClient
from google.protobuf import timestamp_pb2

from peolymp.abstract import AbstractAPI
from peolymp.utils import get_many, download_sources_by_data


class JudgeAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(JudgeAPI, self).__init__(**kwargs)
        self.client = JudgeClient(self.http_client, url=self.get_url())

    def add_participant(self, member_id, contest_id):
        return self.client.AddParticipant(
            judge_pb2.AddParticipantInput(contest_id=contest_id, member_id=member_id)).participant_id

    def add_problem(self, problem_id, index, contest_id, submit_limit=50, score_by_best_testset=True):
        return self.client.ImportProblem(
            judge_pb2.ImportProblemInput(contest_id=contest_id, import_id=str(problem_id), index=index,
                                         submit_limit=submit_limit, score_by_best_testset=score_by_best_testset))

    def sync_problem(self, problem_id, contest_id):
        return self.client.SyncProblem(judge_pb2.SyncProblemInput(problem_id=problem_id, contest_id=contest_id))

    def sync_all_problems(self, contest_id, problem_number=-1):
        problems = self.get_problems(contest_id)
        counter = 0
        for problem in problems:
            if problem_number == -1 or counter == problem_number:
                self.sync_problem(problem.id, contest_id)
                time.sleep(5)
            counter += 1

    def lock_participant_by_id(self, participant_id, contest_id):
        out = self.client.ResetPasscode(
            judge_pb2.ResetPasscodeInput(participant_id=participant_id, contest_id=contest_id))
        return out.passcode

    def get_contest(self, contest_id):
        return self.client.DescribeContest(judge_pb2.DescribeContestInput(contest_id=contest_id)).contest

    def get_contests(self):
        def __get_contests(offset, size):
            return self.client.ListContests(request=judge_pb2.ListContestsInput(offset=offset, size=size))

        return get_many(__get_contests)

    def get_scoring(self, contest_id):
        return self.client.DescribeScoring(judge_pb2.DescribeScoringInput(contest_id=contest_id)).scoring

    def delete_contest(self, contest_id):
        self.client.DeleteContest(judge_pb2.DeleteContestInput(contest_id=contest_id))

    def delete_all_contests(self):
        for contest in self.get_contests():
            self.delete_contest(contest.id)

    def get_problems(self, contest_id):
        return self.client.ListProblems(judge_pb2.ListProblemsInput(contest_id=contest_id)).items

    def create_contest(self, name, domain, start, end, ioi=True):
        contest = contest_pb2.Contest(
            name=name,
            starts_at=timestamp_pb2.Timestamp(seconds=start),
            ends_at=timestamp_pb2.Timestamp(seconds=end),
            status=contest_pb2.Contest.Status.SCHEDULED,
            visibility=contest_pb2.Contest.Visibility.PRIVATE,
            participation_mode=contest_pb2.Contest.ParticipationMode.ONLINE,
            format=contest_pb2.Contest.Format.IOI if ioi else contest_pb2.Contest.Format.ICPC,
            domain=domain + '.eolymp.io'
        )
        res = self.client.CreateContest(judge_pb2.CreateContestInput(contest=contest))
        return res.contest_id

    def allow_upsolve(self, contest_id):
        return self.client.ConfigureScoring(judge_pb2.ConfigureScoringInput(contest_id=contest_id,
                                                                            scoring=contest_pb2.Contest.Scoring(
                                                                                allow_upsolving=True)))

    def get_participant(self, participant_id, contest_id):
        return self.client.DescribeParticipant(
            judge_pb2.DescribeParticipantInput(contest_id=contest_id, participant_id=participant_id)).participant

    def get_submissions(self, contest_id):
        def __get_submissions(offset, size):
            return self.client.ListSubmissions(
                request=judge_pb2.ListSubmissionsInput(offset=offset, size=size, contest_id=contest_id))

        return get_many(__get_submissions)

    def rejudge_problem(self, problem_id, contest_id):
        self.client.RetestProblem(judge_pb2.RetestProblemInput(contest_id=contest_id, problem_id=problem_id))

    def get_participants(self, contest_id):
        def __get_participants(offset, size):
            return self.client.ListParticipants(
                request=judge_pb2.ListParticipantsInput(contest_id=contest_id, offset=offset, size=size))

        return get_many(__get_participants)

    def download_sources(self, dest, contest_id):
        return download_sources_by_data(dest, self.get_contest(contest_id), self.get_problems(contest_id),
                                        self.get_participants(contest_id), self.get_submissions(contest_id))
