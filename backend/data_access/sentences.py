from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    execute_query,
    tuples_to_dict,
)


def create_sentence(nth_sentence, sentence, book_id):
    return next(
        iter(
            tuples_to_dict(
                ["id", "nth_sentence", "sentence", "book_id"],
                create_record(
                    "sentences",
                    ["nth_sentence", "sentence", "book_id"],
                    [nth_sentence, sentence, book_id],
                ),
            )
        ),
        None,
    )


def get_all_sentences():
    return tuples_to_dict(
        ["id", "nth_sentence", "sentence", "book_id"], read_records("sentences")
    )


def delete_sentence_by_id(sentence_id):
    return delete_record("sentences", f"id = {sentence_id}")


def get_sentences_by_book_id(book_id):
    # Query to fetch sentences ordered by nth_sentence
    sentences = read_records(
        "sentences", f"book_id = {book_id} ORDER BY nth_sentence ASC"
    )
    return tuples_to_dict(["id", "nth_sentence", "sentence", "transcript"], sentences)
