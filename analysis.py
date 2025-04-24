
# imports and package downloads
import re
import nltk
import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from langdetect import detect
from langcodes import Language

# nltk package downloads
nltk.download('stopwords')

# list of valid stopwords language options
STOPWORDS_LANGUAGES = ['albanian', 'arabic', 'azerbaijani', 'basque', 'belarusian', 'bengali',
                       'catalan', 'chinese', 'danish', 'dutch', 'english', 'finnish', 'french',
                       'german', 'greek', 'hebrew', 'hinglish', 'hungarian', 'indonesian', 'italian',
                       'kazakh', 'nepali', 'norwegian', 'portuguese', 'romanian', 'russian', 'slovene',
                       'spanish', 'swedish', 'tajik', 'tamil', 'turkish']


def top_n_words_in_novel(url, num_words, lang=None):
    # request url and encode it
    response = requests.get(url)
    response.encoding = 'utf-8'

    # extract html and create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    full_text = soup.get_text()

    # pattern to extract text between START and END markers
    pattern = re.compile(
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*"
        r"(.*?)"
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        re.DOTALL
    )

    # extract text between START and END markers
    match = pattern.search(full_text)
    if match:
        novel_text = match.group(2)
    else:
        print("⚠️ Could not find standard START/END markers. Using full text as fallback.")
        novel_text = full_text

    # Detect language if not provided
    if lang is None:
        detected_lang = detect(novel_text)
        detected_lang = Language(detected_lang).language_name().lower()
        if detected_lang in STOPWORDS_LANGUAGES:
            lang = detected_lang
            print(f"🔍 Detected language: {lang}")
        else:
            print("⚠️ Detected language is not supported. Using default 'english'.")
            lang = 'english'

    # tokenize text
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(novel_text)

    # convert tokens to lowercase and remove stop words
    tokens = [token.lower() for token in tokens]
    stop_words = set(stopwords.words(lang))
    words_no_stop = [
        token for token in tokens if token not in stop_words and len(token) > 1]

    # count and print the n most common words
    counter = Counter(words_no_stop)
    return counter.most_common(num_words)


def novel_metadata(url):
    # request url and encode it
    response = requests.get(url)
    response.encoding = 'utf-8'

    # extract html and create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    # Try to extract metadata section before START marker
    start_match = re.search(
        r"(The Project Gutenberg eBook of.*?)(?=\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK)",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if start_match:
        metadata_text = start_match.group(1)
    else:
        print("⚠️ Couldn't find metadata section, scanning full text.")
        metadata_text = text

    # Flexible regex patterns for metadata extraction
    patterns = {
        "title": r"Title\s*:\s*(.*)",
        "author": r"(Author|Compiler)\s*:\s*(.*)",
        "release_date": r"Release\s*date\s*:\s*(.*)",
        "updated": r"Most\s*recently\s*updated\s*:\s*(.*)",
        "language": r"Language\s*:\s*(.*)",
        "credits": r"Credits\s*:\s*(.*)",
        "original_publication": r"Original\s+(Publication|Date)\s*:\s*(.*)",
    }

    # Fallback defaults
    defaults = {
        "title": "Unknown Title",
        "author": "Unknown Author",
        "release_date": "Unknown Release Date",
        "updated": "Not Updated",
        "language": "Unknown Language",
        "credits": "No Credits Listed",
        "original_publication": "No Original Publication Info",
    }

    metadata = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, metadata_text, re.IGNORECASE)
        if match:
            metadata[key] = match.groups()[-1].strip()
        else:
            metadata[key] = defaults.get(key, "N/A")

    return metadata


# Example usage
# if __name__ == "__main__":
#     url = "https://gutenberg.org/cache/epub/2701/pg2701-images.html"
#     num_words = 10
#     results_top_n = top_n_words_in_novel(url, num_words)
#     metadata = novel_metadata(
#         "https://gutenberg.org/cache/epub/75830/pg75830-images.html")

#     # Display novel metadata
#     print("Novel Metadata:")
#     for key, value in metadata.items():
#         print(f"{key}: {value}")
#     print("\n")

#     # Display top N words
#     print(f"Top {num_words} words in the novel:")
#     for word, count in results_top_n:
#         print(f"{word}: {count}")
