import os
from pathlib import Path
import requests

# assign directory
directory = Path("backend/static/sign_language_media")

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file_name = f.split("\\")[-1]
        transcript = f.split("\\")[-1].split(".")[0]
        data = {
            "transcription": transcript,
            "media_path": ("static/" + "sign_language_media/" + file_name),
        }
        requests.post(
            "http://127.0.0.1:2020/api/book_contents/add_transcription", json=data
        )
