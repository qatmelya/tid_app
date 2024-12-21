from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    execute_query,
    tuples_to_dict,
)


def create_sentence_transcription(sentence_id, transcript_id, nth_transcription):
    return create_record(
        "sentence_transcriptions",
        ["sentence_id", "transcript_id", "nth_transcription"],
        [sentence_id, transcript_id, nth_transcription],
    )


def get_all_sentence_transcriptions():
    return tuples_to_dict(
        ["id", "sentence_id", "transcript_id", "nth_transcription"],
        read_records("sentence_transcriptions"),
    )


def get_sentence_transcription_by_sentence_id(sentence_id):
    # Query to fetch sentences ordered by nth_sentence
    return tuples_to_dict(
        ["id", "sentence_id", "transcript_id", "nth_transcription"],
        read_records(
            "sentence_transcriptions",
            f"sentence_id = {sentence_id} ORDER BY nth_transcription ASC",
        ),
    )


def delete_sentence_transcription_by_id(st_id):
    return delete_record("sentence_transcriptions", f"id = {st_id}")
