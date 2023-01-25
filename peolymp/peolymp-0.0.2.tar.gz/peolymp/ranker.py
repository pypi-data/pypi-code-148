from eolymp.ranker import ranker_pb2, scoreboard_pb2, format_pb2
from eolymp.ranker.ranker_http import RankerClient
from eolymp.wellknown import direction_pb2

from peolymp.abstract import AbstractAPI
from peolymp.utils import get_many


class RankerAPI(AbstractAPI):
    def __init__(self, **kwargs):
        super(RankerAPI, self).__init__(**kwargs)
        self.client = RankerClient(self.http_client, url=self.get_url())

    def create_scoreboard(self, key, name, ioi=True):
        scoreboard = scoreboard_pb2.Scoreboard(key=key, name=name,
                                               format=format_pb2.Format.IOI if ioi else format_pb2.Format.ICPC)
        res = self.client.CreateScoreboard(ranker_pb2.CreateScoreboardInput(scoreboard=scoreboard))
        return res.scoreboard_id

    def add_attribute(self, scoreboard_id, attribute_key, key, name, full_name, filterable=True, sortable=False,
                      index=0):
        type_attribute = scoreboard_pb2.Scoreboard.Column.Type.ATTRIBUTE
        column = scoreboard_pb2.Scoreboard.Column(key=key, name=full_name, short_name=name, type=type_attribute,
                                                  community_attribute_key=attribute_key, index=index,
                                                  filterable=filterable, visible=True, sortable=sortable)
        return self.client.AddScoreboardColumn(
            ranker_pb2.AddScoreboardColumnInput(scoreboard_id=scoreboard_id, column=column))

    def add_total(self, scoreboard_id, key, name, full_name, filterable=True, sortable=False, index=0):
        type_total = scoreboard_pb2.Scoreboard.Column.Type.TOTAL
        column = scoreboard_pb2.Scoreboard.Column(key=key, name=full_name, short_name=name, type=type_total,
                                                  index=index, filterable=filterable, visible=True, sortable=sortable)
        return self.client.AddScoreboardColumn(
            ranker_pb2.AddScoreboardColumnInput(scoreboard_id=scoreboard_id, column=column)).column_id

    def add_name(self, scoreboard_id, key='name', short_name='Ім\'я', name='Ім\'я', index=1):
        type_name = scoreboard_pb2.Scoreboard.Column.Type.NAME
        column = scoreboard_pb2.Scoreboard.Column(key=key, name=name, short_name=short_name, type=type_name,
                                                  index=index)
        return self.client.AddScoreboardColumn(
            ranker_pb2.AddScoreboardColumnInput(scoreboard_id=scoreboard_id, column=column))

    def get_columns(self, scoreboard_id):
        return self.client.ListScoreboardColumns(ranker_pb2.ListScoreboardColumnsInput(scoreboard_id=scoreboard_id))

    def delete_column(self, column_id):
        return self.client.DeleteScoreboardColumn(ranker_pb2.DeleteScoreboardColumnInput(column_id=column_id))

    def add_contest(self, scoreboard_id, contest_scoreboard_id, key, name, full_name, parent_id="", index=0):
        type_contest = scoreboard_pb2.Scoreboard.Column.Type.CONTEST
        column = scoreboard_pb2.Scoreboard.Column(key=key, name=full_name, short_name=name, type=type_contest,
                                                  judge_contest_id=contest_scoreboard_id, index=index,
                                                  visible=True, sortable=True, parent_id=parent_id)
        return self.client.AddScoreboardColumn(
            ranker_pb2.AddScoreboardColumnInput(scoreboard_id=scoreboard_id, column=column)).column_id

    def rebuild(self, scoreboard_id):
        return self.client.RebuildScoreboard(ranker_pb2.RebuildScoreboardInput(scoreboard_id=scoreboard_id))

    def get_scoreboard(self, scoreboard_id):
        return self.client.DescribeScoreboard(
            ranker_pb2.DescribeScoreboardInput(scoreboard_id=scoreboard_id)).scoreboard

    def get_scoreboards(self):
        def __get_scoreboards(offset, size):
            return self.client.ListScoreboards(request=ranker_pb2.ListScoreboardsInput(offset=offset, size=size))

        return get_many(__get_scoreboards)

    def delete_scoreboard(self, scoreboard_id):
        return self.client.DeleteScoreboard(ranker_pb2.DeleteScoreboardInput(scoreboard_id=scoreboard_id))

    def delete_all_scoreboards(self):
        for scoreboard in self.get_scoreboards():
            self.delete_scoreboard(scoreboard.id)

    def make_default_sort_column(self, scoreboard_id, column_id):
        scoreboard = scoreboard_pb2.Scoreboard(id=scoreboard_id, default_sort_column=column_id,
                                               default_sort_order=direction_pb2.DESC)
        return self.client.UpdateScoreboard(
            ranker_pb2.UpdateScoreboardInput(scoreboard_id=scoreboard_id, scoreboard=scoreboard,
                                             patch=[ranker_pb2.UpdateScoreboardInput.DEFAULT_SORT]))
