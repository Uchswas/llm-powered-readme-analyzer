import csv
import json
import time
from datetime import datetime

import requests
import yaml


class HuggingFaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://huggingface.co'
        self.interval = 1

    def set_interval(self, interval):
        self.interval = interval

    def get_all_models(self, max_results=1000):
        models = []
        next_page_url = f"/api/models?limit={max_results}"
        total_count = 0

        while next_page_url:
            print(f"Processing URL: {next_page_url}")

            response = requests.get(self.base_url + next_page_url)
            response_dict = json.loads(response.content)

            if not response_dict:
                break

            models.extend(response_dict)
            total_count += len(response_dict)
            print(f"Retrieved {total_count} models")

            next_link = response.links.get("next", {})
            next_page_url = (
                next_link.get("url", "").replace(self.base_url, "")
                if next_link
                else None
            )

            time.sleep(self.interval)

        return models


def save_to_json(hf_api):
    model_list = hf_api.get_all_models()
    model_detail_dict = {}
    count = 0

    for model in model_list:
        model_id = model['modelId']
        try:
            model_info = hf_api.get_model_info_by_id(model_id)
            model_detail_dict[model_id] = model_info
        except Exception as e:
            print(f'Error with model {model_id}: {e}')
            model_detail_dict[model_id] = {'error': str(e)}
        time.sleep(hf_api.interval)

        count += 1
        print('.', end='')

        if count % 100 == 0:
            print(f'Processed {count} models')

    with open('model_detail_dict_all.json', 'w', encoding='utf-8') as f:
        json.dump(model_detail_dict, f, indent=4)

    return model_detail_dict


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)

        writer.writerow(['Model ID', 'Other Details'])

        for model in data:
            model_id = model['modelId']
            other_details = json.dumps(model, ensure_ascii=False)
            writer.writerow([model_id, other_details])


if __name__ == '__main__':
    config_path = 'f:/hf-readme/data collection/config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print(config)
    print(type(config))

    api_key = config["huggingface_key"]
    print(api_key)

    hf_api = HuggingFaceAPI(api_key)

    all_models = hf_api.get_all_models()

    current_date = datetime.now().strftime("%Y-%m-%d")
    file_count = len(all_models)
    json_file_name = f'{current_date}_all_huggingface_models_{file_count}.json'
    csv_file_name = f'{current_date}_all_huggingface_models_{file_count}.csv'

    output_path = f'f:/hf-readme/data collection/{json_file_name}'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_models, f, indent=4)
    print(f"Model list saved to JSON file: {output_path}")

    csv_output_path = f'f:/hf-readme/data collection/{csv_file_name}'
    json_to_csv(output_path, csv_output_path)
    print(f"Model list saved to CSV file: {csv_output_path}")
