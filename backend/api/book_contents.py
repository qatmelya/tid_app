from flask_injector import inject
from data_access.db_access import get_sentences_by_book_id, insert_into_sentences


@inject
def get_book_contents(book_id):
    sentences = get_sentences_by_book_id(book_id)
    sentences_response = []
    for sentence in sentences:
        sentences_response.append(
            {
                "nth_sentence": sentence[0],
                "sentence": sentence[1],
                "transcript": sentence[2],
            }
        )
    return sentences_response, 200


@inject
def add_sentence(sentence_payload):
    nth_sentence = sentence_payload["nth_sentence"]
    book_id = sentence_payload["book_id"]
    sentence = sentence_payload["sentence"]
    transcript = sentence_payload["transcript"]
    return insert_into_sentences(nth_sentence, book_id, sentence, transcript), 200
