from preprocess import sanitize, remove_duplicates
import os

sanitized_text = sanitize(text)
processed = remove_duplicates(sanitized_text)

from bardapi import Bard
bard = Bard(token='dAhkQZkfY-kfkFSG1FuWDQW5PFqXVbjrkRZjyuUGeiomh8sNdPAlbj0O0pXJMRkXHDph6g.', timeout=30)
prompt = "Summarize this email in 3 sentences: " + processed
resp = bard.get_answer(prompt)
bard_resp = resp['content']
print(bard_resp)

# from langchain.chat_models import 

