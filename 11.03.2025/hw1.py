"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List, Dict
import string
from collections import defaultdict
from typing import List, Dict


def get_longest_diverse_words(file_path: str) -> List[str]:
    word_stats = []
    current_word = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char.isalpha() or char == "'":
                    current_word.append(char)
                else:
                    if current_word:
                        word = ''.join(current_word)
                        unique_chars = len(set(word.lower()))
                        word_stats.append((word, unique_chars, len(word)))
                        current_word = []
    
    if current_word:
        word = ''.join(current_word)
        unique_chars = len(set(word.lower()))
        word_stats.append((word, unique_chars, len(word)))
    
    # Sort by unique chars (desc), then length (desc), then alphabetical
    word_stats.sort(key=lambda x: (-x[1], -x[2], x[0]))
    
    # Get top 10 words, avoiding duplicates
    seen = set()
    result = []
    for word, _, _ in word_stats:
        if word not in seen:
            seen.add(word)
            result.append(word)
            if len(result) == 10:
                break
    return result


def get_rarest_char(file_path: str) -> str:
    char_counts = defaultdict(int)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                char_counts[char] += 1
    
    if not char_counts:
        return ''
    
    return min(char_counts.items(), key=lambda x: x[1])[0]


def count_punctuation_chars(file_path: str) -> int:
    punct_chars = set(string.punctuation)
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char in punct_chars:
                    count += 1
    return count


def count_non_ascii_chars(file_path: str) -> int:
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if not char.isascii():
                    count += 1
    return count


def get_most_common_non_ascii_char(file_path: str) -> str:
    non_ascii_counts = defaultdict(int)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if not char.isascii():
                    non_ascii_counts[char] += 1
    
    if not non_ascii_counts:
        return ''
    
    return max(non_ascii_counts.items(), key=lambda x: x[1])[0]


if __name__ == "__main__":
    filename = "data.txt"
    print(get_longest_diverse_words(filename))
    print(get_rarest_char(filename))
    print(count_punctuation_chars(filename))
    print(count_non_ascii_chars(filename))
    print(get_most_common_non_ascii_char(filename))