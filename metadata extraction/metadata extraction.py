import csv
import json


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)

        writer.writerow(['Model ID', 'Downloads', 'Likes', 'Other Details'])

        for model in data:
            model_id = model['modelId']
            downloads = model['downloads']
            likes = model['likes']
            other_details = json.dumps(
                {
                    key: value
                    for key, value in model.items()
                    if key not in ['modelId', 'downloads', 'likes']
                },
                ensure_ascii=False
            )
            writer.writerow([model_id, downloads, likes, other_details])


def main():
    file_path = (
        'F:/hf-readme/metadata collection/2024-10-13_all_huggingface_models_'
        '1049590.json'
    )
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    filtered_data = [entry for entry in data if entry['likes'] >= 2]

    sorted_by_downloads = sorted(
        filtered_data, key=lambda x: x['downloads'], reverse=True
    )

    sorted_by_likes = sorted(
        filtered_data, key=lambda x: x['likes'], reverse=True
    )

    downloads_sorted_file = (
        'f:/hf-readme/metadata extraction/metadata_sorted_by_downloads.json'
    )
    likes_sorted_file = (
        'f:/hf-readme/metadata extraction/metadata_sorted_by_likes.json'
    )

    with open(downloads_sorted_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_by_downloads, file, indent=4)

    with open(likes_sorted_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_by_likes, file, indent=4)

    print(f"Files saved:\n1. {downloads_sorted_file}\n2. {likes_sorted_file}")

    top_5_percent = int(len(sorted_by_downloads) * 0.05)
    popular_downloads = sorted_by_downloads[:top_5_percent]
    popular_likes = sorted_by_likes[:top_5_percent]

    popular_downloads_file = (
        'f:/hf-readme/metadata extraction/'
        'popular_metadata_sorted_by_downloads.json'
    )
    popular_likes_file = (
        'f:/hf-readme/metadata extraction/popular_metadata_sorted_by_likes.json'
    )

    with open(popular_downloads_file, 'w', encoding='utf-8') as file:
        json.dump(popular_downloads, file, indent=4)

    with open(popular_likes_file, 'w', encoding='utf-8') as file:
        json.dump(popular_likes, file, indent=4)

    print(
        f"Files saved:\n1. {popular_downloads_file}\n2. {popular_likes_file}"
    )

    json_to_csv(
        downloads_sorted_file,
        'f:/hf-readme/metadata extraction/metadata_sorted_by_downloads.csv'
    )
    json_to_csv(
        likes_sorted_file,
        'f:/hf-readme/metadata extraction/metadata_sorted_by_likes.csv'
    )

    json_to_csv(
        popular_downloads_file,
        'f:/hf-readme/metadata extraction/'
        'popular_metadata_sorted_by_downloads.csv'
    )
    json_to_csv(
        popular_likes_file,
        'f:/hf-readme/metadata extraction/popular_metadata_sorted_by_likes.csv'
    )


if __name__ == '__main__':
    main()
