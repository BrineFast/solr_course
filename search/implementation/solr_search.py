from argparse import ArgumentParser
from typing import NoReturn

from transliterate import translit
import ssl
import pysolr
import json
import string
import nltk
from nltk.corpus import wordnet as wn
from wiki_ru_wordnet import WikiWordnet

from search.implementation.utils.auto_correction_filter import AutoCorrectionFilter

solr = pysolr.Solr("http://127.0.0.1:8983/solr/text_search_core", timeout=100)

def clean_up(clean: bool) -> NoReturn:
    if clean:
        solr.delete(q="*:*")


def upload_docs(upload: bool) -> NoReturn:
    if upload:
        with open("data/solr_data.json") as f:
            data: dict = json.loads(f.read())
            for i in range(0, len(data)):
                data[i]["id"] = i + 1
                data[i]["text"] = data[i]["text"].replace("\n", " ").replace("\t", " ").strip()
                print(data[i])
                solr.add(data[i], overwrite=True)

def make_dict(make: bool) -> NoReturn:
    if make:
        all_words: set = set()
        punctuation: str = string.punctuation + "«»…—–­©0123456789#№"
        with open("data/solr_data.json") as f:
            data: dict = json.loads(f.read())
            for i in range(0, len(data)):
                if data[i]["text"] is not None and data[i]["author"] is not None and data[i]["topic"] is not None:
                    all_words.update(data[i]["text"].translate(data[i]["text"].maketrans(punctuation, " "*len(punctuation))).lower().split()
                                     + data[i]["topic"].translate(data[i]["topic"].maketrans(punctuation, " "*len(punctuation))).lower().split()
                                     + data[i]["author"].translate(data[i]["author"].maketrans(punctuation, " "*len(punctuation))).lower().split())
                print(f"{i} -> {len(data)}")

            with open("data/dictionary.txt", mode="w") as f2:
                f2.writelines([f"{i}\n" for i in all_words])

def make_synonyms(make: bool) -> NoReturn:
    if make:
        with open("data/dictionary.txt") as f:
            try:
                _create_unverified_https_context: object = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context: object = _create_unverified_https_context
            nltk.download("all")
            rwn: WikiWordnet = WikiWordnet()
            while True:
                initial_word: str = f.readline().replace("\n", "")
                if not initial_word:
                    break
                synonyms: set = set()
                ru_synonyms: list = rwn.get_synsets(initial_word).append(translit(initial_word, "ru"))
                if ru_synonyms:
                    for synonym in ru_synonyms[0].get_words():
                        if synonym.lemma() != initial_word:
                            synonyms.add(synonym.lemma())
                en_synonyms: list = wn.synsets(initial_word).append(translit(initial_word, "en"))
                for synonym in en_synonyms:
                    if synonym.name().split(".")[0] != initial_word:
                        synonyms.add(synonym.name().split(".")[0])
                if synonyms:
                    accordance: str = f"{initial_word} => "
                    for i in synonyms:
                            accordance = accordance + f"{i},"
                    accordance: str = accordance[:-1]
                    print(accordance)
                    with open("data/synonyms.txt", mode="a") as f2:
                        f2.write(accordance + "\n")

def make_request(make: bool) -> NoReturn:
    if make:
        query: str = input("Solr request (tip: 'field': 'value'): ")
        corrected_query: str = AutoCorrectionFilter().correct(query)
        print(solr.search(corrected_query))

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--clean_up", type=bool, default=False)
    parser.add_argument("--upload_docs", type=bool, default=False)
    parser.add_argument("--make_dict", type=bool, default=False)
    parser.add_argument("--make_syn", type=bool, default=False)
    parser.add_argument("--make_req", type=str, default=False)
    arguments = parser.parse_args()
    clean_up(arguments.clean)
    upload_docs(arguments.upload_docs)
    make_dict(arguments.make_dict)
    make_synonyms(arguments.make_syn)
    make_request(arguments.make_request)
