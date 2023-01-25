from unittest import TestCase

from ossapi import (RankingType, BeatmapsetEventType, AccessDeniedError,
    InsufficientScopeError, Mod, GameMode)

from tests import api

class TestBeatmapsetDiscussionPosts(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_posts()

class TestUserRecentActivity(TestCase):
    def test_deserialize(self):
        api.user_recent_activity(12092800)

class TestSpotlights(TestCase):
    def test_deserialize(self):
        api.spotlights()

class TestUserBeatmaps(TestCase):
    def test_deserialize(self):
        api.user_beatmaps(user_id=12092800, type_="most_played")

class TestUserKudosu(TestCase):
    def test_deserialize(self):
        api.user_kudosu(user_id=3178418)

class TestBeatmapScores(TestCase):
    def test_deserialize(self):
        api.beatmap_scores(beatmap_id=1981090)

class TestBeatmap(TestCase):
    def test_deserialize(self):
        api.beatmap(beatmap_id=221777)

        # beatmap with a diff owner
        bm = api.beatmap(beatmap_id=1604098)
        # might need to be updated when
        # https://github.com/ppy/osu-web/issues/9784 is addressed.
        self.assertIsNone(bm.owner)

class TestBeatmapset(TestCase):
    def test_deserialize(self):
        api.beatmapset(beatmap_id=3207950)

class TestBeatmapsetEvents(TestCase):
    def test_deserialize(self):
        api.beatmapset_events()

    def test_all_types(self):
        # beatmapset_events is a really complicated endpoint in terms of return
        # types. We want to make sure both that we're not doing anything wrong,
        # and the osu! api isn't doing anything wrong by returning something
        # that doesn't match their documentation.
        for event_type in BeatmapsetEventType:
            api.beatmapset_events(types=[event_type])

class TestRanking(TestCase):
    def test_deserialize(self):
        api.ranking("osu", RankingType.PERFORMANCE, country="US")

class TestUserScores(TestCase):
    def test_deserialize(self):
        api.user_scores(12092800, "best")

class TestBeatmapUserScore(TestCase):
    def test_deserialize(self):
        api.beatmap_user_score(beatmap_id=221777, user_id=2757689, mode="osu")

class TestBeatmapUserScores(TestCase):
    def test_deserialize(self):
        api.beatmap_user_scores(beatmap_id=221777, user_id=2757689, mode="osu")

class TestSearch(TestCase):
    def test_deserialize(self):
        api.search(query="peppy")

class TestComment(TestCase):
    def test_deserialize(self):
        api.comment(comment_id=1)

class TestDownloadScore(TestCase):
    def test_deserialize(self):
        # api instance is using client credentials which doesn't have access to
        # downloading replays
        self.assertRaises(AccessDeniedError,
            lambda: api.download_score(mode="osu", score_id=2797309065))

class TestSearchBeatmaps(TestCase):
    def test_deserialize(self):
        api.search_beatmapsets(query="the big black")

class TestUser(TestCase):
    def test_deserialize(self):
        api.user(12092800)

    def test_key(self):
        # make sure it automatically falls back to username if not specified
        api.user("tybug2")
        api.user("tybug2", key="username")

        self.assertRaises(Exception, lambda: api.user("tybug2", key="id"))

class TestMe(TestCase):
    def test_deserialize(self):
        # requires an authorization code api for the identify scope, client
        # credentials can only request the public scope
        self.assertRaises(InsufficientScopeError, api.get_me)

class TestWikiPage(TestCase):
    def test_deserialize(self):
        api.wiki_page("en", "Welcome")

class TestChangelogBuild(TestCase):
    def test_deserialize(self):
        api.changelog_build("stable40", "20210520.2")

class TestChangelogListing(TestCase):
    def test_deserialize(self):
        api.changelog_listing()

class TestChangelogLookup(TestCase):
    def test_deserialize(self):
        api.changelog_lookup("lazer")

class TestForumTopic(TestCase):
    def test_deserialize(self):
        api.forum_topic(141240)

class TestBeatmapsetDiscussionVotes(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_votes().votes[0].score

class TestBeatmapsetDiscussions(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussions()

class TestNewsListing(TestCase):
    def test_deserialize(self):
        api.news_listing(year=2021)

class TestNewsPost(TestCase):
    def test_deserialize(self):
        # querying the same post by id or slug should give the same result.
        post1 = api.news_post(1025, key="id")
        post2 = api.news_post("2021-10-04-halloween-fanart-contest", key="slug")

        self.assertEqual(post1.id, post2.id)
        self.assertEqual(post1, post2)

class TestSeasonalBackgrounds(TestCase):
    def test_deserialize(self):
        api.seasonal_backgrounds()

class TestBeatmapAttributes(TestCase):
    def test_deserialize(self):
        api.beatmap_attributes(221777, ruleset="osu")
        api.beatmap_attributes(221777, mods=Mod.HDDT)
        api.beatmap_attributes(221777, mods="HR")
        api.beatmap_attributes(221777, ruleset_id=0)

class TestUsers(TestCase):
    def test_deserialize(self):
        api.users([12092800])

class TestBeatmaps(TestCase):
    def test_deserialize(self):
        api.beatmaps([221777])

class TestScore(TestCase):
    def test_deserialize(self):
        # downloadable
        api.score(GameMode.OSU, 2243145877)
        # downloadable, my score
        api.score(GameMode.OSU, 3685255338)
        # not downloadable, my score
        api.score(GameMode.OSU, 3772000814)

        # other gamemodes
        api.score(GameMode.TAIKO, 176904666)
        api.score(GameMode.MANIA, 524674141)
        api.score(GameMode.CATCH, 211167989)

# TODO requires friends.read scope
# class TestFriends(TestCase):
#     def test_deserialize(self):
#         api.friends()

# TODO requires chat.write scope
# class TestCreateNewPM(TestCase):
#     def test_deserialize(self):
#         api.create_pm(2070907, "Unit test from ossapi "
#             "(https://github.com/circleguard/ossapi/), please ignore")
