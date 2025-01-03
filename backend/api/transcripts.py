from data_access import transcripts
from flask import jsonify


def get_all_transcripts():
    return transcripts.get_all_transcripts(), 200


def get_by_transcript_string(transcript_string):
    transcription = transcripts.get_transcript_by_string(transcript_string)
    return jsonify(transcription), 200
