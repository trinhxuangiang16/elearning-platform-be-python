import math
import re
import heapq
import unicodedata
from collections import defaultdict


def normalize_vietnamese_text(text):
    if not text:
        return ""
    text_str = str(text)
    text_str = text_str.replace("đ", "d").replace("Đ", "d")
    decomposed = unicodedata.normalize("NFD", text_str)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    lowered = stripped.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def tokenize_text(text):
    normalized = normalize_vietnamese_text(text)
    if not normalized:
        return []
    return [token for token in normalized.split(" ") if token]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.tokens = set()


class PrefixTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, token):
        node = self.root
        for ch in token:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.tokens.add(token)

    def search_prefix(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return set()
            node = node.children[ch]
        return set(node.tokens)


def bounded_levenshtein_distance(word1, word2, max_dist=2):
    len1 = len(word1)
    len2 = len(word2)
    if abs(len1 - len2) > max_dist:
        return max_dist + 1

    prev_row = list(range(len2 + 1))
    for i in range(1, len1 + 1):
        curr_row = [i] + [0] * len2
        min_in_row = curr_row[0]
        for j in range(1, len2 + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            deletion = prev_row[j] + 1
            insertion = curr_row[j - 1] + 1
            substitution = prev_row[j - 1] + cost
            val = min(deletion, insertion, substitution)
            curr_row[j] = val
            if val < min_in_row:
                min_in_row = val
        if min_in_row > max_dist:
            return max_dist + 1
        prev_row = curr_row

    return prev_row[len2]


class InMemoryCourseSearchEngine:
    def __init__(self):
        self.inverted_index = defaultdict(set)
        self.trie = PrefixTrie()
        self.vocabulary = set()
        self.doc_token_weights = {}
        self.doc_lengths = {}
        self.avg_doc_length = 1.0
        self.total_docs = 0
        self.is_built = False

    def build_index(self, courses_data):
        self.inverted_index = defaultdict(set)
        self.trie = PrefixTrie()
        self.vocabulary = set()
        self.doc_token_weights = {}
        self.doc_lengths = {}

        total_length = 0
        self.total_docs = len(courses_data)

        for item in courses_data:
            course_id = item["ma_khoa_hoc"]
            token_scores = defaultdict(float)
            doc_len = 0

            fields_with_weights = [
                (item.get("ten_khoa_hoc", ""), 3.0),
                (item.get("ten_danh_muc", ""), 2.5),
                (item.get("ma_khoa_hoc", ""), 2.5),
                (item.get("sections_text", ""), 2.0),
                (item.get("lessons_text", ""), 2.0),
                (item.get("mo_ta", ""), 1.0),
            ]

            for field_text, weight in fields_with_weights:
                tokens = tokenize_text(field_text)
                for token in tokens:
                    token_scores[token] += weight
                    doc_len += 1
                    self.inverted_index[token].add(course_id)
                    self.vocabulary.add(token)
                    self.trie.insert(token)

            self.doc_token_weights[course_id] = dict(token_scores)
            self.doc_lengths[course_id] = max(doc_len, 1)
            total_length += max(doc_len, 1)

        if self.total_docs > 0:
            self.avg_doc_length = total_length / self.total_docs
        else:
            self.avg_doc_length = 1.0

        self.is_built = True

    def rebuild_from_db(self):
        from core.models import Course
        courses = Course.objects.select_related("category", "creator").prefetch_related("sections__lessons").all()
        courses_data = []
        for c in courses:
            sec_titles = []
            les_titles = []
            for sec in c.sections.all():
                sec_titles.append(sec.ten_chuong)
                for les in sec.lessons.all():
                    les_titles.append(les.ten_bai_hoc)
            courses_data.append({
                "ma_khoa_hoc": c.ma_khoa_hoc,
                "ten_khoa_hoc": c.ten_khoa_hoc,
                "ten_danh_muc": c.category.ten_danh_muc if c.category else "",
                "mo_ta": c.mo_ta or "",
                "sections_text": " ".join(sec_titles),
                "lessons_text": " ".join(les_titles),
            })
        self.build_index(courses_data)

    def ensure_built(self):
        if not self.is_built:
            self.rebuild_from_db()

    def _compute_idf(self, token):
        doc_freq = len(self.inverted_index.get(token, set()))
        if doc_freq == 0:
            return 0.0
        return math.log(1.0 + (self.total_docs - doc_freq + 0.5) / (doc_freq + 0.5))

    def search(self, query_str, top_k=50):
        self.ensure_built()
        query_tokens = tokenize_text(query_str)
        if not query_tokens:
            return []

        k1 = 1.5
        b = 0.75
        course_scores = defaultdict(float)

        for q_token in query_tokens:
            matched_tokens = []

            if q_token in self.inverted_index:
                matched_tokens.append((q_token, 1.0))

            prefix_matches = self.trie.search_prefix(q_token)
            for p_token in prefix_matches:
                if p_token != q_token:
                    matched_tokens.append((p_token, 0.85))

            if not matched_tokens and len(q_token) >= 3:
                for vocab_token in self.vocabulary:
                    if abs(len(vocab_token) - len(q_token)) <= 2:
                        dist = bounded_levenshtein_distance(q_token, vocab_token, max_dist=2)
                        if dist <= 2:
                            penalty = 0.7 if dist == 1 else 0.5
                            matched_tokens.append((vocab_token, penalty))

            for matched_token, match_multiplier in matched_tokens:
                idf = self._compute_idf(matched_token)
                candidate_docs = self.inverted_index.get(matched_token, set())
                for doc_id in candidate_docs:
                    tf = self.doc_token_weights.get(doc_id, {}).get(matched_token, 0.0)
                    doc_len = self.doc_lengths.get(doc_id, 1)
                    numerator = tf * (k1 + 1.0)
                    denominator = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_length))
                    bm25_score = idf * (numerator / denominator) * match_multiplier
                    course_scores[doc_id] += bm25_score

        if not course_scores:
            return []

        ranked = heapq.nlargest(top_k, course_scores.items(), key=lambda item: item[1])
        return [course_id for course_id, _ in ranked]


search_engine_instance = InMemoryCourseSearchEngine()

