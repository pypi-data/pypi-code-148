from asyncio import Task, ensure_future
from math import log10, sqrt
from typing import Dict, List, Optional, Union

from kh_common.auth import KhUser
from kh_common.caching import AerospikeCache
from kh_common.caching.key_value_store import KeyValueStore
from kh_common.config.constants import epoch
from kh_common.exceptions.http_error import BadRequest
from kh_common.sql import SqlInterface
from scipy.stats import norm

from fuzzly_posts.models import PostId, Score


"""
resources:
	https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx
	https://steamdb.info/blog/steamdb-rating
	https://www.evanmiller.org/how-not-to-sort-by-average-rating.html
	https://redditblog.com/2009/10/15/reddits-new-comment-sorting-system
	https://www.reddit.com/r/TheoryOfReddit/comments/bpmd3x/how_does_hot_vs_best_vscontroversial_vs_rising/envijlj
"""


# this is the z-score of 0.8, z is calulated via: norm.ppf(1-(1-0.8)/2)
z_score_08 = norm.ppf(0.9)


def _sign(x: Union[int, float]) -> int :
	return (x > 0) - (x < 0)


def hot(up: int, down: int, time: float) -> float :
	s: int = up - down
	return _sign(s) * log10(max(abs(s), 1)) + (time - epoch) / 45000


def controversial(up: int, down: int) -> float :
	return (up + down)**(min(up, down)/max(up, down)) if up or down else 0


def confidence(up: int, total: int) -> float :
	# calculates a confidence score with a z score of 0.8
	if not total :
		return 0
	phat = up / total
	return (
		(phat + z_score_08 * z_score_08 / (2 * total)
		- z_score_08 * sqrt((phat * (1 - phat)
		+ z_score_08 * z_score_08 / (4 * total)) / total)) / (1 + z_score_08 * z_score_08 / total)
	)


def best(up: int, total: int) -> float :
	if not total :
		return 0
	s: float = up / total
	return s - (s - 0.5) * 2**(-log10(total + 1))


ScoreCache: KeyValueStore = KeyValueStore('kheina', 'score')
VoteCache: KeyValueStore = KeyValueStore('kheina', 'votes')


class Scoring(SqlInterface) :

	def _validateVote(self, vote: Optional[bool]) -> None :
		if not isinstance(vote, (bool, type(None))) :
			raise BadRequest('the given vote is invalid (vote value must be integer. 1 = up, -1 = down, 0 or null to remove vote)')


	def vote(self, user: KhUser, post_id: PostId, upvote: Optional[bool]) -> Score :
		self._validateVote(upvote)
		with self.transaction() as transaction :
			data = transaction.query("""
				INSERT INTO kheina.public.post_votes
				(user_id, post_id, upvote)
				VALUES
				(%s, %s, %s)
				ON CONFLICT ON CONSTRAINT post_votes_pkey DO 
					UPDATE SET
						upvote = %s
					WHERE post_votes.user_id = %s
						AND post_votes.post_id = %s;

				SELECT COUNT(post_votes.upvote), SUM(post_votes.upvote::int), posts.created_on
				FROM kheina.public.posts
					LEFT JOIN kheina.public.post_votes
						ON post_votes.post_id = posts.post_id
							AND post_votes.upvote IS NOT NULL
				WHERE posts.post_id = %s
				GROUP BY posts.post_id;
				""",
				(
					user.user_id, post_id.int(), upvote,
					upvote, user.user_id, post_id.int(),
					post_id.int(),
				),
				fetch_one=True,
			)

			up: int = data[1] or 0
			total: int = data[0] or 0
			down: int = total - up
			created: float = data[2].timestamp()

			top: int = up - down
			hot: float = hot(up, down, created)
			best: float = confidence(up, total)
			cont: float = controversial(up, down)

			transaction.query("""
				INSERT INTO kheina.public.post_scores
				(post_id, upvotes, downvotes, top, hot, best, controversial)
				VALUES
				(%s, %s, %s, %s, %s, %s, %s)
				ON CONFLICT ON CONSTRAINT post_scores_pkey DO 
					UPDATE SET
						upvotes = %s,
						downvotes = %s,
						top = %s,
						hot = %s,
						best = %s,
						controversial = %s
					WHERE post_scores.post_id = %s;
				""",
				(
					post_id.int(), up, down, top, hot, best, cont,
					up, down, top, hot, best, cont, post_id.int(),
				),
			)

			transaction.commit()

		score: Dict[str, int] = {
			'up': up,
			'down': down,
			'total': total,
		}
		ScoreCache.put(post_id, score)

		user_vote = 0 if upvote is None else (1 if upvote else -1)
		VoteCache.put(f'{user.user_id}.{post_id}', user_vote)

		return Score(
			**score,
			user_vote = user_vote,
		)


	@AerospikeCache('kheina', 'score', '{post_id}', _kvs=ScoreCache)
	async def _get_score(self, post_id: PostId) -> Optional[Dict[str, int]] :
		data: List[int] = await self.query_async("""
			SELECT
				post_scores.upvotes,
				post_scores.downvotes
			FROM kheina.public.post_scores
			WHERE post_scores.post_id = %s
			""",
			(post_id.int(),),
			fetch_one=True,
		)

		if not data :
			return None

		return  {
			'up': data[0],
			'down': data[1],
			'total': sum(data),
		}


	@AerospikeCache('kheina', 'votes', '{user}.{post_id}', _kvs=VoteCache)
	async def _get_vote(self, user: int, post_id: PostId) -> int :
		data: List[int] = await self.query_async("""
			SELECT
				upvote
			FROM kheina.public.post_votes
			WHERE post_votes.user_id = %s
				AND post_votes.post_id = %s;
			""",
			(user, post_id.int()),
			fetch_one=True,
		)

		if not data :
			return 0

		return 1 if data[0] else -1


	async def getScore(self, user: KhUser, post_id: PostId) -> Optional[Score] :
		score: Task[Dict[str, int]] = ensure_future(self._get_score(post_id))
		vote: Task[int] = ensure_future(self._get_vote(user.user_id, post_id))

		score: Optional[Dict[str, int]] = await score

		if not score :
			return None

		return Score(
			user_vote=await vote,
			**score,
		)
