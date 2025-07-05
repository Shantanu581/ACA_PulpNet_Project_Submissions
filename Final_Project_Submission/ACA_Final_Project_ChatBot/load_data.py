import json
import os
from glob import glob

def load_all_articles(json_folder_path):
    all_docs = []
    json_files = glob(os.path.join(json_folder_path, "*.json"))
    for path in json_files:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for post in data:
                if isinstance(post.get("content"), list):
                    content = "\n".join(post["content"])
                else:
                    content = str(post.get("content", ""))
                doc = {
                    "title": post.get("title", "Untitled"),
                    "content": content
                }
                all_docs.append(doc)
    return all_docs
