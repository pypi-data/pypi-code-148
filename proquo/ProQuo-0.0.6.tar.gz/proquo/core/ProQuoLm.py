import re
from typing import List, Tuple
from quid.match.Match import Match
from quid.match.MatchSpan import MatchSpan
from proquo.match.MatchRef import MatchRef
from proquo.core.Quote import Quote
from datasketch import MinHash, MinHashLSH
from rapidfuzz.distance import Levenshtein
import tensorflow as tf


# noinspection PyMethodMayBeStatic
class ProQuoLm:
    HASH_PERM: int = 128
    LSH_THRESHOLD: float = 0.70
    SCORE_CUTOFF: int = 0.85
    WITHOUT_REF_SEARCH_RADIUS = 500
    SOURCE_PARALLEL_LAST_PAGE = 63
    LONG_MIN_LENGTH = 5
    LINKING_MAX_LENGTH = 200

    BERT_LINK_MIN_PROB: float = 0.5

    def __init__(self, linking_model, linking_vectorizer):
        self.source_cache = {}
        self.hashes = None
        self.source_text_parallel_print = False
        self.linking_model = linking_model
        self.linking_vectorizer = linking_vectorizer

    def compare(self, source_text: str, target_text: str, quid_matches: List[Match]):

        source_text = self.__clean_text(source_text)
        source_text_hash = hash(source_text)
        if source_text_hash in self.source_cache:
            self.hashes = self.source_cache[source_text_hash]
        else:
            self.hashes = self.__init_lsh_hashes(source_text)
            self.source_cache[source_text_hash] = self.hashes

        short_matches = self.__filter_short_matches(source_text, target_text, quid_matches)

        all_quotes: List[Quote] = self.__get_quotations(target_text)
        footnote_ranges = self.__get_footnote_ranges(target_text)

        main_quotes = []

        for q in all_quotes:
            if not self.__is_in_footnote(q.start, q.end, footnote_ranges):
                main_quotes.append(q)

        result_matches_bert: List[MatchRef] = self.__link_with_bert(main_quotes, short_matches, source_text,
                                                                    target_text)
        return result_matches_bert

    def __get_footnote_ranges(self, input_text):
        result = []

        for re_match in re.finditer(r'\[\[\[((?:.|\n)+?)]]]', input_text):
            start = re_match.start()
            end = re_match.end()
            result.append((start, end))

        return result

    def __is_in_footnote(self, start, end, footnote_ranges):
        for rf in footnote_ranges:
            if (rf[0] <= start < rf[1]) or (rf[0] <= end <= rf[1]):
                return True

        return False

    def __get_quotations(self, input_text: str) -> List[Quote]:
        quotes = []

        for re_match in re.finditer(r'\"([^"]+?)\"', input_text):
            start = re_match.span(1)[0]
            end = re_match.span(1)[1]
            text = re_match.group(1)

            if len(text.split()) < self.LONG_MIN_LENGTH:
                quotes.append(Quote(start, end, text))

        return quotes

    def __create_match(self, source_text, quote_source_start, quote_source_end, sq):
        # quote_source_end = quote_source_start + len(sq.text)
        quote_source_text = source_text[quote_source_start:quote_source_end]

        source_span = MatchSpan(quote_source_start, quote_source_end, quote_source_text)
        target_span = MatchSpan(sq.start, sq.end, sq.text)
        match = MatchRef(source_span, target_span, None)
        return match

    def __filter_short_matches(self, source_text, target_text, matches):
        result = []
        for match in matches:
            match_source_text = source_text[match.source_span.start:match.source_span.end]
            match_target_text = target_text[match.target_span.start:match.target_span.end]
            source_length = len(match_source_text.split())
            target_length = len(match_target_text.split())

            if source_length < self.LONG_MIN_LENGTH or target_length < self.LONG_MIN_LENGTH:
                result.append(match)

        return result

    def __clean_text(self, input_text: str) -> str:
        output_text = re.sub('(\\[\\.\\.\\.]|\\[…]|\\.\\.\\.|…)', lambda x: ' ' * len(x.group(1)), input_text)
        output_text = re.sub(f'[^a-zA-Z\\däüöÄÜÖß\n ]', ' ', output_text)

        if len(input_text) != len(output_text):
            raise Exception('Length of source text changed')

        return output_text.lower()

    def __normalize_special_chars(self, input_word: str) -> str:
        input_word = input_word.replace('ß', 'ss')
        input_word = input_word.replace('ä', 'ae')
        input_word = input_word.replace('ö', 'oe')
        input_word = input_word.replace('ü', 'ue')
        input_word = input_word.replace('ey', 'ei')

        input_word = input_word.replace('[', '')
        input_word = input_word.replace(']', '')
        return input_word

    def __init_lsh_hashes(self, source_text) -> MinHashLSH:
        hashes = MinHashLSH(threshold=self.LSH_THRESHOLD, num_perm=self.HASH_PERM)

        for match in re.finditer(r'\S+', source_text):
            token = self.__normalize_special_chars(match.group())

            if len(token) > 0:
                text_begin_pos = match.start()
                text_end_pos = match.end()

                token_character_set = set(token)
                token_hash = MinHash(num_perm=self.HASH_PERM)

                for char in token_character_set:
                    token_hash.update(char.encode('utf8'))

                hashes.insert(f'{text_begin_pos}_{text_end_pos}_{token}', token_hash, True)

        return hashes

    # TODO: improve with better normalization
    def __strict_match(self, word: str, search_space: str):
        word = self.__clean_text(word)
        # word = self.__normalize_special_chars(word)
        # word = re.sub(' +', ' ', word, flags=re.DOTALL)
        # word = word.strip()

        # search_space = self.__normalize_special_chars(search_space)

        re_matches_iter = re.finditer(r'\b' + re.escape(word) + r'\b', search_space, flags=re.IGNORECASE)
        re_matches = list(re_matches_iter)
        return re_matches

    def __fuzzy_match(self, word: str, range_start: int, range_end: int) -> List[Tuple[int, int]]:
        word = self.__clean_text(word)
        word = self.__normalize_special_chars(word)
        word = re.sub(' +', ' ', word, flags=re.DOTALL)
        word = word.strip()
        word_character_set = set(word)
        word_hash = MinHash(num_perm=self.HASH_PERM)

        for char in word_character_set:
            word_hash.update(char.encode('utf8'))

        candidates = self.hashes.query(word_hash)
        candidates_split = []

        for candidate in candidates:
            parts = candidate.split('_')
            candidates_split.append((parts[0], parts[1], parts[2]))

        candidates_split.sort(key=lambda e: int(e[0]))

        result = []

        for candidate in candidates_split:
            c_start = int(candidate[0])
            c_end = int(candidate[1])
            token = candidate[2]

            ratio = Levenshtein.normalized_similarity(word, token)

            if ratio < self.SCORE_CUTOFF:
                continue

            if c_start >= range_start and c_end <= range_end:
                result.append((c_start, c_end))

        return result

    def __link_with_bert(self, short_quotes, short_matches, source_text, target_text):
        result = []

        for sq in short_quotes:
            match_len = len(sq.text.split())

            if match_len == 1:
                candidates = self.__search_single_word(sq, source_text)
            else:
                candidates = self.__search_multi_word(short_matches, sq, source_text)

            if len(candidates) == 0:
                continue

            combinations = []

            for c in candidates:
                le_source_text, le_target_text = self.__prepare_link_texts(sq, c, source_text, target_text, False)
                combinations.append((le_source_text, le_target_text))

            preds = self.__predict_link(combinations)

            best_candidate = None
            best_pred = 0

            for c, pred in zip(candidates, preds):
                if pred > self.BERT_LINK_MIN_PROB:
                    if pred > best_pred:
                        best_pred = pred
                        best_candidate = c

            if best_candidate:
                result.append(self.__create_match(source_text, best_candidate[0], best_candidate[1], sq))

        return result

    def __prepare_link_texts(self, sq, candidate, source_text, target_text, is_masked):
        source_start = candidate[0]
        source_end = candidate[1]
        target_start = sq.start
        target_end = sq.end

        source_quote_text = source_text[source_start:source_end].replace('\n', ' ')
        source_rest_len = self.LINKING_MAX_LENGTH

        if not is_masked:
            source_quote_length = len(source_quote_text.split())
            source_rest_len = self.LINKING_MAX_LENGTH - source_quote_length

        target_quote_text = target_text[target_start:target_end].replace('\n', ' ')
        target_rest_len = self.LINKING_MAX_LENGTH

        if not is_masked:
            target_quote_length = len(target_quote_text.split())
            target_rest_len = self.LINKING_MAX_LENGTH - target_quote_length

        if source_rest_len <= 0 or target_rest_len <= 0:
            return '', ''

        source_text_before = source_text[:source_start]
        source_text_after = source_text[source_end:]

        source_text_before = re.sub(r'\[\[\[((?:.|\n)+?)]]]', ' ', source_text_before)
        source_text_after = re.sub(r'\[\[\[((?:.|\n)+?)]]]', ' ', source_text_after)

        target_text_before = target_text[:target_start]
        target_text_after = target_text[target_end:]

        target_text_before = re.sub(r'\[\[\[((?:.|\n)+?)]]]', ' ', target_text_before)
        target_text_after = re.sub(r'\[\[\[((?:.|\n)+?)]]]', ' ', target_text_after)

        # TODO: check if is in footnote

        source_parts_before = source_text_before.split()
        source_parts_after = source_text_after.split()

        source_parts_before_count = len(source_parts_before)
        source_parts_after_count = len(source_parts_after)

        source_count_before = min(round(source_rest_len / 2), source_parts_before_count)
        source_count_after = min(source_rest_len - source_count_before, source_parts_after_count)

        source_text_before = ' '.join(source_parts_before[-source_count_before:])
        source_text_after = ' '.join(source_parts_after[:source_count_after])

        if is_masked:
            le_source_text = f'{source_text_before} <S> {source_text_after}'
        else:
            le_source_text = f'{source_text_before} <S> {source_quote_text} </S> {source_text_after}'

        target_parts_before = target_text_before.split()
        target_parts_after = target_text_after.split()

        target_parts_before_count = len(target_parts_before)
        target_parts_after_count = len(target_parts_after)

        target_count_before = min(round(target_rest_len / 2), target_parts_before_count)
        target_count_after = min(target_rest_len - target_count_before, target_parts_after_count)

        target_text_before = ' '.join(target_parts_before[-target_count_before:])
        target_text_after = ' '.join(target_parts_after[:target_count_after])

        if is_masked:
            le_target_text = f'{target_text_before[:-1]} <T> {target_text_after[1:]}'
        else:
            le_target_text = f'{target_text_before[:-1]} <T> {target_quote_text} </T> {target_text_after[1:]}'

        if is_masked:
            source_quote_text = re.escape(source_quote_text)
            source_quote_text = self.__replace_special_chars_for_regex(source_quote_text)

            target_quote_text = re.escape(target_quote_text)
            target_quote_text = self.__replace_special_chars_for_regex(target_quote_text)

            le_source_text = re.sub(r'\b' + source_quote_text + r'\b', '<Q>', le_source_text, flags=re.IGNORECASE)
            le_target_text = re.sub(r'\b' + target_quote_text + r'\b', '<Q>', le_target_text, flags=re.IGNORECASE)

        return le_source_text, le_target_text

    def __replace_special_chars_for_regex(self, input_word: str) -> str:
        input_word = input_word.replace('ß', '(?:ß|ss)')
        input_word = input_word.replace('ä', '(?:ä|ae)')
        input_word = input_word.replace('ö', '(?:ö|oe)')
        input_word = input_word.replace('ü', '(?:ü|ue)')
        input_word = input_word.replace('ey', '(?:ey|ei)')
        return input_word

    def __predict_link(self, pairs):
        if len(pairs) == 0:
            return []

        test_data = self.linking_vectorizer.vectorize(pairs)
        prediction = self.linking_model.predict(test_data)
        prediction_logits = prediction.logits
        probs = tf.nn.softmax(prediction_logits, axis=1).numpy()
        preds = [row[1] for row in probs]
        return preds

    def __search_single_word(self, sq, source_text):
        re_matches = self.__strict_match(sq.text, source_text)
        strict_matches_count = len(re_matches)

        if strict_matches_count > 0:
            result = []

            for re_match in re_matches:
                result.append((re_match.start(), re_match.end()))

            return result

        fuzzy_candidates = self.__fuzzy_match(sq.text, 0, len(source_text))
        return fuzzy_candidates

    def __search_multi_word(self, short_matches, sq, source_text):
        re_matches = self.__strict_match(sq.text, source_text)

        if len(re_matches) > 0:
            result = []

            for re_match in re_matches:
                result.append((re_match.start(), re_match.end()))

            return result

        candidates = []

        for short_match in short_matches:
            overlap_start = max(short_match.target_span.start, sq.start)
            overlap_end = min(short_match.target_span.end, sq.end)
            overlap_length = overlap_end - overlap_start
            quote_length = sq.end - sq.start
            percentage = overlap_length / quote_length

            if percentage >= 0.7:
                candidates.append((short_match.source_span.start, short_match.source_span.end))

        return candidates
