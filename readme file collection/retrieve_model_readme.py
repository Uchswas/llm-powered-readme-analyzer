import json
import os
import threading
import time
from queue import Queue

import requests
import yaml


class HuggingFaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://huggingface.co'
        self.interval = 0.1

    def download_readme(self, model_id):
        readme_url = f"https://huggingface.co/{model_id}/raw/main/README.md"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(readme_url, headers=headers)

        if response.status_code == 200:
            safe_model_id = model_id.replace("/", "_")
            save_dir = 'f:/hf-readme/readme file collection/readme by likes'
            filename = os.path.join(save_dir, f'{safe_model_id}.md')
            os.makedirs(save_dir, exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            return True, filename
        else:
            return False, None


def load_existing_results(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}


def worker(api_key, model_queue, readme_results, lock, thread_id):
    hf_api = HuggingFaceAPI(api_key)

    while not model_queue.empty():
        model_id = model_queue.get()
        print(f"Thread {thread_id} is checking README for model: {model_id}")

        try:
            success, filename = hf_api.download_readme(model_id)
            if success:
                print(
                    f"Thread {thread_id} successfully downloaded README to {filename}"
                )
                with lock:
                    readme_results[model_id] = filename
            else:
                print(
                    f"Thread {thread_id} failed to download README for model: {model_id}"
                )
                with lock:
                    readme_results[model_id] = 'Failed to download'
        except Exception as e:
            print(
                f"Thread {thread_id} encountered an error with model {model_id}: {e}"
            )
            with lock:
                readme_results[model_id] = {'error': str(e)}
        finally:
            time.sleep(hf_api.interval)
            model_queue.task_done()


def main():
    config_path = 'f:/hf-readme/readme file collection/config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    model_queue = Queue()
    results_file = 'f:/hf-readme/readme file collection/readme_results_likes.json'
    readme_results = load_existing_results(results_file)
    lock = threading.Lock()

    model_list_path = (
        'f:/hf-readme/metadata extraction/popular_metadata_sorted_by_likes.json'
    )
    with open(model_list_path, 'r', encoding='utf-8') as f:
        model_list = json.load(f)

    start_index = 0
    end_index = 3000

    for model in model_list[start_index:end_index]:
        model_id = model.get('modelId')
        if model_id not in readme_results:
            model_queue.put(model_id)
        else:
            print(
                f"Model {model_id} README already downloaded or previously failed. "
                "Skipping."
            )

    threads = []
    for i, api_key in enumerate(config['huggingface_keys']):
        thread = threading.Thread(
            target=worker,
            args=(api_key, model_queue, readme_results, lock, i + 1)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(readme_results, f, indent=4)


if __name__ == '__main__':
    main()
