from data_access.base_funcs import (
    create_record,
    read_records,
    delete_record,
    tuples_to_dict,
)


def create_transcript(media_path, transcription):
    return create_record(
        "transcripts", ["media_path", "transcription"], [media_path, transcription]
    )


def get_all_transcripts():
    return tuples_to_dict(
        ["id", "media_path", "transcription"], read_records("transcripts")
    )


def get_transcript_by_id(transcript_id):
    return next(
        iter(
            tuples_to_dict(
                ["id", "media_path", "transcription"],
                read_records("transcripts", f"id = {transcript_id}"),
            )
        )
    )


def delete_transcript_by_id(transcript_id):
    return delete_record("transcripts", f"id = {transcript_id}")
