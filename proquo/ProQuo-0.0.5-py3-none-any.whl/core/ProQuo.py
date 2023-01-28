import sys
import itertools
import re
from typing import Optional, List, Tuple
from quid.match.Match import Match
from quid.match.MatchSpan import MatchSpan

from proquo.match.MatchRef import MatchRef
from proquo.core.Quote import Quote
from proquo.core.QuoteRef import QuoteRef
from proquo.core.Reference import Reference
import numpy as np
from sklearn.cluster import SpectralClustering
from datasketch import MinHash, MinHashLSH
from rapidfuzz.distance import Levenshtein
import tensorflow as tf


# noinspection PyMethodMayBeStatic
class ProQuo:
    # References
    MAX_BRACKET_LENGTH = 25
    LONG_MIN_LENGTH = 5
    REF_EXAMPLE_COUNT = 5
    # Relation
    REF_MIN_PROB: float = 0.7
    REL_MIN_PROB: float = 0.5
    REL_MAX_DISTANCE = 100
    REL_MAX_WORDS: int = 120
    # Linking
    WITHOUT_REF_SEARCH_RADIUS = 500
    SOURCE_PARALLEL_LAST_PAGE = 63
    # Fuzzy matching
    HASH_PERM: int = 128
    LSH_THRESHOLD: float = 0.70
    SCORE_CUTOFF: int = 0.85

    def __init__(self, reference_model, reference_vectorizer, relation_model, relation_vectorizer):
        self.reference_model = reference_model
        self.reference_vectorizer = reference_vectorizer
        self.relation_model = relation_model
        self.relation_vectorizer = relation_vectorizer
        self.source_cache = {}
        self.hashes = None
        self.source_text_parallel_print = False

    def compare(self, source_text: str, target_text: str, quidl_matches: List[Match],
                source_text_parallel_print=False) -> List[MatchRef]:
        source_text = self.__clean_text(source_text)
        source_text_hash = hash(source_text)
        if source_text_hash in self.source_cache:
            self.hashes = self.source_cache[source_text_hash]
        else:
            self.hashes = self.__init_lsh_hashes(source_text)
            self.source_cache[source_text_hash] = self.hashes

        self.source_text_parallel_print = source_text_parallel_print

        long_matches = self.__filter_long_matches(source_text, quidl_matches)
        short_matches = self.__filter_short_matches(source_text, target_text, quidl_matches)

        matches_with_reference: List[MatchRef] = self.__add_reference_to_match(target_text, long_matches)
        matches_with_reference.sort(key=lambda x: x.target_span.end - x.target_span.start, reverse=True)
        longest_matches: List[MatchRef] = []

        for match_with_reference in matches_with_reference:
            if match_with_reference.reference:
                if re.search(r'\d', match_with_reference.reference.text):
                    longest_matches.append(match_with_reference)

            if len(longest_matches) >= self.REF_EXAMPLE_COUNT:
                break

        all_references: List[Reference] = self.__get_references(target_text, longest_matches)
        all_quotes: List[Quote] = self.__get_quotations(target_text)
        footnote_ranges = self.__get_footnote_ranges(target_text)

        main_references = []
        footnote_references = []

        for ref in all_references:
            if not self.__is_in_footnote(ref.start, ref.end, footnote_ranges):
                main_references.append(ref)
            else:
                footnote_references.append(ref)

        main_quotes = []
        footnote_quotes = []

        for q in all_quotes:
            if not self.__is_in_footnote(q.start, q.end, footnote_ranges):
                main_quotes.append(q)
            else:
                footnote_quotes.append(q)

        main_quotes = self.__filter_quotes_not_in_source(main_quotes, 0, len(source_text))

        main_references.sort(key=lambda x: x.start)
        main_quotes.sort(key=lambda x: x.start)

        quote_ref_combos_main = self.__get_combinations(target_text, main_references, main_quotes, footnote_ranges)

        quote_ref_combos: List[QuoteRef] = []
        quote_ref_combos.extend(quote_ref_combos_main)

        short_quotes: List[QuoteRef] = self.__get_short_quotes(quote_ref_combos)
        short_quotes = self.__filter_duplicates(short_quotes)

        matches_with_reference.sort(key=lambda x: 0 if x.reference is None else x.reference.page)
        result_matches: List[MatchRef] = []

        page_size, first_page_known_pos, first_page_nr = self.__get_page_size(matches_with_reference)

        # quotes with ref first
        for sq in short_quotes:
            start, end, page_known_pos = self.__get_quote_range_with_ref(sq, page_size, first_page_known_pos,
                                                                         first_page_nr, len(source_text))

            match_len = len(sq.quote.text.split())

            if match_len == 1:
                quote_source_start, quote_source_end = self.__search_single_word(sq.quote, source_text, start, end,
                                                                                 page_known_pos)
            else:
                quote_source_start, quote_source_end = self.__search_multi_word(short_matches, sq, start, end,
                                                                                source_text)

            if quote_source_start > -1:
                quote_source_text = source_text[quote_source_start:quote_source_end]
                source_span = MatchSpan(quote_source_start, quote_source_end, quote_source_text)
                target_span = MatchSpan(sq.quote.start, sq.quote.end, sq.quote.text)
                match = MatchRef(source_span, target_span, sq.reference)
                result_matches.append(match)

        # then quotes without ref
        short_quotes_without_ref = []

        for mq in main_quotes:
            found = False

            for sq in short_quotes:
                if sq.quote.start == mq.start and sq.quote.end == mq.end:
                    found = True
                    break

            if not found:
                short_quotes_without_ref.append(QuoteRef(mq, None, ''))

        # add result matches
        matches_with_reference.extend(result_matches)
        matches_with_ref_in_appearance = sorted(matches_with_reference, key=lambda x: x.target_span.start)

        # search for short quotes without ref
        for sq in short_quotes_without_ref:
            start, end, page_known_pos = self.__get_quote_range_without_ref(sq, matches_with_ref_in_appearance,
                                                                            len(source_text), page_size)

            quote_source_start = -1
            quote_source_end = -1
            match_len = len(sq.quote.text.split())

            if match_len == 1:
                if page_known_pos > -1:
                    quote_source_start, quote_source_end = self.__search_single_word(sq.quote, source_text, start, end,
                                                                                     page_known_pos)
            else:
                quote_source_start, quote_source_end = self.__search_multi_word(short_matches, sq, start, end,
                                                                                source_text)

            if quote_source_start > -1:
                quote_source_text = source_text[quote_source_start:quote_source_end]

                source_span = MatchSpan(quote_source_start, quote_source_end, quote_source_text)
                target_span = MatchSpan(sq.quote.start, sq.quote.end, sq.quote.text)
                match = MatchRef(source_span, target_span, sq.reference)
                result_matches.append(match)

        return result_matches

    def __predict_ref(self, sentences_1: List[str], sentences_2: List[str]) -> List[float]:
        if len(sentences_1) == 0 or len(sentences_2) == 0:
            return []

        test_data_x_1 = self.reference_vectorizer.vectorize(sentences_1)
        test_data_x_2 = self.reference_vectorizer.vectorize(sentences_2)
        preds = list(self.reference_model.predict([test_data_x_1, test_data_x_2], verbose=1).ravel())
        return preds

    def __predict_rel(self, quote_ref_combos):
        if len(quote_ref_combos) == 0:
            return []

        sentences = []

        for qrc in quote_ref_combos:
            text = qrc.text
            text = re.sub(f'"', ' " ', text, flags=re.DOTALL)
            sentences.append(text)

        test_data = self.relation_vectorizer.vectorize(sentences)

        prediction = self.relation_model.predict(test_data)
        prediction_logits = prediction.logits
        probs = tf.nn.softmax(prediction_logits, axis=1).numpy()
        preds = [row[1] for row in probs]

        return preds

    def __filter_long_matches(self, input_text: str, matches):
        result = []
        for match in matches:
            text = input_text[match.source_span.start:match.source_span.end]
            length = len(text.split())

            if length >= self.LONG_MIN_LENGTH:
                result.append(match)

        return result

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

    def __add_reference_to_match(self, input_text, matches) -> List[MatchRef]:
        result: List[MatchRef] = []

        for match in matches:
            match_ref = MatchRef.from_match(match)
            end = match.target_span.end
            context_text = input_text[end:end + 20]

            re_match = re.search(r'\((.+?)\)', context_text)
            if re_match:
                ref_start = re_match.start(1)
                ref_end = re_match.end(1)
                ref_text = re_match.group(1)
                page_nr = self.__extract_page_from_reference(ref_text)

                reference = Reference(ref_start, ref_end, ref_text, page_nr)
                match_ref.reference = reference

            result.append(match_ref)

        return result

    def __get_references(self, input_text: str, match_ref_examples: List[MatchRef]) -> List[Reference]:
        num_examples = len(match_ref_examples)

        if num_examples == 0:
            return []

        match_ref_ex_with_id = []

        index = 0

        if num_examples > 2:
            for pos, mre in enumerate(match_ref_examples):
                match_ref_ex_with_id.append((pos, mre))

            match_ref_combinations = itertools.combinations(match_ref_ex_with_id, 2)
            sentences_1: List[str] = []
            sentences_2: List[str] = []
            combinations = []

            perm: Tuple[Tuple[int, MatchRef], Tuple[int, MatchRef]]
            for perm in match_ref_combinations:
                sentences_1.append(perm[0][1].reference.text)
                sentences_2.append(perm[1][1].reference.text)
                combinations.append((perm[0], perm[1]))

            if len(sentences_1) == 0 or len(sentences_2) == 0:
                return []

            preds = self.__predict_ref(sentences_1, sentences_2)
            num_examples = len(match_ref_examples)

            matrix = np.eye(num_examples, dtype=float)

            for perm, pred in zip(combinations, preds):
                x = perm[0][0]
                y = perm[1][0]
                # matrix has to be symmetrical
                matrix[x][y] = pred
                matrix[y][x] = pred

            labels = SpectralClustering(2, affinity='precomputed').fit_predict(matrix)
            labels = labels.tolist()

            num_occ_cluster_0 = labels.count(0)
            num_occ_cluster_1 = labels.count(1)

            if num_occ_cluster_0 > num_occ_cluster_1:
                index = labels.index(0)
            else:
                index = labels.index(1)

        best_bibl = match_ref_examples[index]

        bracket_positions = {}
        stack = []

        for i, c in enumerate(input_text):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if len(stack) > 0:
                    # There will be errors, so we just ignore them
                    bracket_positions[stack.pop()] = i

        possible_references = []

        for start, end in bracket_positions.items():
            if end - start > self.MAX_BRACKET_LENGTH:
                continue

            ref_text = input_text[start + 1:end]
            # TODO: resolve ebd.
            page_nr = self.__extract_page_from_reference(ref_text)
            possible_references.append(Reference(start + 1, end, input_text[start + 1:end], page_nr))

        possible_permutations = itertools.product([x.text for x in possible_references], [best_bibl.reference.text])

        poss_bibl_sentences_1 = []
        poss_bibl_sentences_2 = []

        for perm in list(possible_permutations):
            poss_bibl_sentences_1.append(perm[0])
            poss_bibl_sentences_2.append(perm[1])

        preds_2 = self.__predict_ref(poss_bibl_sentences_1, poss_bibl_sentences_2)

        references: List[Reference] = []

        for pr, pred in zip(possible_references, preds_2):
            if pred >= self.REF_MIN_PROB:
                references.append(pr)

        return references

    def __get_quotations(self, input_text: str) -> List[Quote]:
        quotes = []

        for re_match in re.finditer(r'\"([^"]+?)\"', input_text):
            start = re_match.span(1)[0]
            end = re_match.span(1)[1]
            text = re_match.group(1)

            if len(text.split()) < self.LONG_MIN_LENGTH:
                quotes.append(Quote(start, end, text))

        return quotes

    def __replace_other_ref(self, input_text, references, start, end):
        other_refs = []

        for ref in references:
            if ref.start >= start and ref.end <= end:
                other_refs.append(ref)

        text = input_text[start:end]

        other_refs.sort(key=lambda x: x.start, reverse=True)

        for ref in other_refs:
            text = f'{text[:ref.start - start]} <OREF> {text[ref.end - start:]}'

        text = re.sub(r'\[\[\[((?:.|\n)+?)]]]', '', text, flags=re.DOTALL)

        return text

    def __get_combinations(self, input_text, references, quotes, footnote_ranges: Optional[List], offset=0):
        my_permutations = itertools.product(quotes, references)

        result: List[QuoteRef] = []

        for perm in my_permutations:
            quote = perm[0]
            reference = perm[1]

            if quote.start < reference.end:
                start = quote.start - offset
                end = reference.end - offset
                between_start = quote.end - offset
                between_end = reference.start - offset
                words_in_fn_count = 0

                if footnote_ranges:
                    words_in_fn_count = self.__count_words_in_footnotes(input_text, footnote_ranges, start, end)

                dist = len(input_text[between_start:between_end].split()) - words_in_fn_count
                if dist > self.REL_MAX_DISTANCE:
                    continue

                text_replaced = self.__replace_other_ref(input_text, references, quote.end, reference.start)
                text = f' <Q> {input_text[quote.start:quote.end]} </Q> {text_replaced} <REF> '
            else:
                start = reference.start - offset
                end = quote.end - offset
                between_start = reference.end - offset
                between_end = quote.start - offset
                words_in_fn_count = 0

                if footnote_ranges:
                    words_in_fn_count = self.__count_words_in_footnotes(input_text, footnote_ranges, start, end)

                dist = len(input_text[between_start:between_end].split()) - words_in_fn_count
                if dist > self.REL_MAX_DISTANCE:
                    continue

                text_replaced = self.__replace_other_ref(input_text, references, reference.end, quote.start)
                text = f' <REF> {text_replaced} <Q> {input_text[quote.start:quote.end]} </Q> '

            length = len(text.split())

            if length > self.REL_MAX_WORDS:
                continue

            rest_len = self.REL_MAX_WORDS - length

            parts_before = input_text[:start].split()
            parts_after = input_text[end:].split()

            parts_before_count = len(parts_before)
            parts_after_count = len(parts_after)

            count_before = min(round(rest_len / 2), parts_before_count)
            count_after = min(rest_len - count_before, parts_after_count)

            text_before = ''
            temp_end = start

            for i in range(len(parts_before) - 1, len(parts_before) - 1 - count_before, -1):
                part = parts_before[i]
                part_len = len(part)
                temp_start = temp_end - 1 - part_len

                if not footnote_ranges or not self.__is_in_footnote(temp_start, temp_end, footnote_ranges):
                    text_before = f'{parts_before[i]} {text_before}'

                temp_end = temp_start

            text_after = ''
            temp_start = end

            for i in range(0, count_after):
                part = parts_after[i]
                part_len = len(part)
                temp_end = temp_start + 1 + part_len

                if not footnote_ranges or not self.__is_in_footnote(temp_start, temp_end, footnote_ranges):
                    text_after += f' {parts_after[i]}'

                temp_start = temp_end

            text_before_replaced = self.__replace_other_ref(input_text, references, start - len(text_before), start)
            text_after_replaced = self.__replace_other_ref(input_text, references, end, end + len(text_after))

            text = f'{text_before_replaced} {text} {text_after_replaced}'

            result.append(QuoteRef(quote, reference, text))

        return result

    def __get_combinations_in_footnotes(self, input_text, quotes, references, footnote_ranges):
        result = []

        for fn_range in footnote_ranges:
            fn_quotes = []
            fn_references = []

            for q in quotes:
                if fn_range[0] <= q.start < fn_range[1]:
                    fn_quotes.append(q)

            for ref in references:
                if fn_range[0] <= ref.start < fn_range[1]:
                    fn_references.append(ref)

            if len(fn_quotes) > 0 and len(fn_references) > 0:
                text = input_text[fn_range[0]:fn_range[1]]
                combos = self.__get_combinations(text, fn_references, fn_quotes, None, fn_range[0])
                result.extend(combos)

        return result

    def __get_short_quotes(self, quote_ref_combos) -> List[QuoteRef]:
        preds = self.__predict_rel(quote_ref_combos)
        result = []

        for qrc, pred in zip(quote_ref_combos, preds):
            if pred >= self.REL_MIN_PROB:
                qrc.pred = pred
                result.append(qrc)

        return result

    def __filter_quotes_not_in_source(self, quotes: List[Quote], start, end) -> List[Quote]:
        result: List[Quote] = []

        for quote in quotes:
            if len(quote.text.split()) > 1:
                result.append(quote)
                continue

            candidates = self.__fuzzy_match(quote.text, start, end)
            if len(candidates) == 0:
                continue

            result.append(quote)

        return result

    def __filter_duplicates(self, short_quotes):
        result = []

        for sq in short_quotes:
            found = False
            replace_pos = -1

            for pos, r in enumerate(result):
                if r.quote.start == sq.quote.start and r.quote.end == sq.quote.end:
                    found = True

                    if sq.pred > r.pred:
                        replace_pos = pos
                    break

            if not found:
                result.append(sq)
            elif replace_pos > -1:
                result[replace_pos] = sq

        return result

    def __count_odd_numbers_in_range(self, start, end):
        if end > start:
            if end <= self.SOURCE_PARALLEL_LAST_PAGE:
                return (end - start) // 2
            elif start < self.SOURCE_PARALLEL_LAST_PAGE:
                return self.__count_odd_numbers_in_range(start, self.SOURCE_PARALLEL_LAST_PAGE)
        else:
            if start <= self.SOURCE_PARALLEL_LAST_PAGE:
                return (start - end) // 2
            elif end < self.SOURCE_PARALLEL_LAST_PAGE:
                return self.__count_odd_numbers_in_range(end, self.SOURCE_PARALLEL_LAST_PAGE)

        return 0

    def __extract_page_from_reference(self, text: str, prev_match_with_ref: Optional[MatchRef] = None) -> int:
        re_match = re.search(r'S\. ?(\d+)', text)
        if re_match:
            page_nr = int(re_match.group(1))
            return page_nr

        re_match = re.search(r'^(\d+)', text)
        if re_match:
            page_nr = int(re_match.group(1))
            return page_nr

        re_match = re.search(r'\W(\d+)', text)
        if re_match:
            page_nr = int(re_match.group(1))
            return page_nr

        page_nr = self.__resolve_non_number_page(text, prev_match_with_ref)
        return page_nr

    def __resolve_non_number_page(self, text: str, prev_match_with_ref: MatchRef) -> int:
        if not prev_match_with_ref:
            return 0

        if text.startswith('ebd'):
            return prev_match_with_ref.reference.page

        return 0

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

    def __count_words_in_footnotes(self, input_text, footnote_ranges, start, end):
        count = 0

        for fr in footnote_ranges:
            if start <= fr[0] < end:
                text = input_text[fr[0]:fr[1]]
                count += len(text.split())

        return count

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

    def __get_page_size(self, matches_with_reference) -> Tuple[int, int, int]:
        mwr_sorted = sorted(matches_with_reference, key=lambda x: x.source_span.start)

        start = -1
        end = -1
        first_page = 0
        last_page = 0

        for match_ref in mwr_sorted:
            if match_ref.reference and match_ref.reference.page > 0:
                if start == -1:
                    start = match_ref.source_span.start
                    first_page = match_ref.reference.page
                elif first_page > match_ref.reference.page:
                    start = -1

        for match_ref in reversed(mwr_sorted):
            if match_ref.reference and match_ref.reference.page > 0:
                if end == -1:
                    end = match_ref.source_span.end
                    last_page = match_ref.reference.page
                elif last_page < match_ref.reference.page:
                    end = -1

        page_size = 0

        if self.source_text_parallel_print:
            page_diff = last_page - first_page - self.__count_odd_numbers_in_range(first_page, last_page)
        else:
            page_diff = last_page - first_page

        if 0 < first_page != last_page > 0:
            page_size = ((end - start) // page_diff)

        return page_size, start, first_page

    def __get_quote_range_with_ref(self, sq, page_size, first_page_known_pos, first_page_nr, source_text_len):
        start = 0
        end = source_text_len
        page_known_pos = -1

        if sq.reference.page > 0:
            if page_size > 0 and first_page_nr > 0:

                if self.source_text_parallel_print:
                    page_diff = sq.reference.page - first_page_nr - \
                                self.__count_odd_numbers_in_range(first_page_nr, sq.reference.page)
                else:
                    page_diff = sq.reference.page - first_page_nr

                page_known_pos = first_page_known_pos + (page_diff * page_size)
                start = max(0, page_known_pos - page_size)
                end = min(source_text_len, page_known_pos + page_size)

        # in this special case we search the whole text
        if end <= start:
            start = 0
            end = source_text_len

        return start, end, page_known_pos

    def __get_quote_range_without_ref(self, sq, matches_with_reference, source_text_len, page_size):
        mwr_best = None
        best_dist = sys.maxsize

        for pos, match_with_reference in enumerate(matches_with_reference):
            if not match_with_reference.reference:
                continue

            mwr_start = max(0, match_with_reference.target_span.start - self.WITHOUT_REF_SEARCH_RADIUS)
            mwr_end = min(source_text_len, match_with_reference.target_span.end + self.WITHOUT_REF_SEARCH_RADIUS)

            new_dist = sys.maxsize

            if mwr_start <= sq.quote.start <= match_with_reference.target_span.start:
                new_dist = match_with_reference.target_span.start - sq.quote.end
            elif match_with_reference.target_span.end <= sq.quote.start <= mwr_end:
                new_dist = sq.quote.start - match_with_reference.target_span.end

            if new_dist < best_dist:
                best_dist = new_dist
                mwr_best = match_with_reference

        start = 0
        end = source_text_len
        page_known_pos = -1

        if mwr_best:
            if page_size > 0:
                start = max(0, mwr_best.source_span.start - page_size)
                end = min(source_text_len, mwr_best.source_span.end + page_size)
                page_known_pos = mwr_best.source_span.start + ((mwr_best.source_span.end - mwr_best.source_span.start) // 2)

        return start, end, page_known_pos

    def __search_single_word(self, quote, source_text, search_space_start, search_space_end, page_known_pos):
        source_search_space = source_text[search_space_start:search_space_end]
        re_matches = self.__strict_match(quote.text, source_search_space)
        strict_matches_count = len(re_matches)

        if strict_matches_count == 0:
            fuzzy_candidates = self.__fuzzy_match(quote.text, search_space_start, search_space_end)

            if len(fuzzy_candidates) == 1:
                return fuzzy_candidates[0][0], fuzzy_candidates[0][1]
            elif len(fuzzy_candidates) > 1:
                smallest_dist = sys.maxsize
                best_match_start_pos = 0
                best_match_end_pos = 0

                for fc in fuzzy_candidates:
                    # TODO: Is start ideal? Maybe compare start and end
                    m_start = fc[0]
                    diff = abs(page_known_pos - m_start)
                    if diff < smallest_dist:
                        smallest_dist = diff
                        best_match_start_pos = m_start
                        best_match_end_pos = fc[1]

                return best_match_start_pos, best_match_end_pos

        elif strict_matches_count == 1:
            re_match = re_matches[0]

            if re_match:
                return re_match.start() + search_space_start, re_match.end() + search_space_start

        elif page_known_pos > -1:
            smallest_dist = sys.maxsize
            best_match_start_pos = -1
            best_match_end_pos = -1

            for m in re_matches:
                # TODO: Is start ideal? Maybe compare start and end
                m_start = m.start() + search_space_start
                diff = abs(page_known_pos - m_start)
                if diff < smallest_dist:
                    smallest_dist = diff
                    best_match_start_pos = m_start
                    best_match_end_pos = m.end() + search_space_start

            return best_match_start_pos, best_match_end_pos

        return -1, -1

    def __search_multi_word(self, short_matches, sq, range_start, range_end, source_text):
        search_space = source_text[range_start:range_end]
        re_matches = self.__strict_match(sq.quote.text, search_space)

        if len(re_matches) > 1:
            return -1, -1

        if len(re_matches) == 1:
            return re_matches[0].start() + range_start, re_matches[0].end() + range_start
        elif len(re_matches) == 0:
            re_matches = self.__strict_match(sq.quote.text, source_text)
            if len(re_matches) > 1:
                return -1, -1

            if len(re_matches) == 1:
                return re_matches[0].start(), re_matches[0].end()

        candidates = []

        for short_match in short_matches:
            overlap_start = max(short_match.target_span.start, sq.quote.start)
            overlap_end = min(short_match.target_span.end, sq.quote.end)
            overlap_length = overlap_end - overlap_start
            quote_length = sq.quote.end - sq.quote.start
            percentage = overlap_length / quote_length

            if percentage >= 0.7:
                candidates.append(short_match)

        candidates_count = len(candidates)

        if candidates_count == 0:
            return -1, -1
        elif candidates_count == 1:
            return candidates[0].source_span.start, candidates[0].source_span.end
        else:
            filtered_candidates = []

            for c in candidates:
                if c.source_span.start >= range_start and c.source_span.end <= range_end:
                    filtered_candidates.append(c)

            if len(filtered_candidates) == 1:
                return filtered_candidates[0].source_span.start, filtered_candidates[0].source_span.end

        return -1, -1
