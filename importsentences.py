import requests
import json

with open("smalltest.json", "r", encoding="utf-8") as fp:
    json_str = json.load(fp)
book_id = 3

for index, (sentence, files) in enumerate(json_str.items()):
    sentence_data = {
        "nth_sentence": str(index + 1),
        "book_id": str(book_id),
        "sentence": sentence,
    }
    created_sentence = requests.post(
        "http://127.0.0.1:2020/api/book_contents/add_sentence", json=sentence_data
    ).json()
    sentence_id = created_sentence["id"]
    for i, file in enumerate(files):
        transcript_id = requests.get(
            "http://127.0.0.1:2020/api/transcripts/get_by_transcript_string/"
            + file.split(".")[0]
        ).json()
        st_data = {
            "nth_transcription": i + 1,
            "sentence_id": sentence_id,
            "transcript_id": transcript_id["id"],
        }
        requests.post(
            "http://127.0.0.1:2020/api/book_contents/add_sentence_transcription",
            json=st_data,
        )
