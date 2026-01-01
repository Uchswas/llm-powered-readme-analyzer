import json

import pandas as pd

SECTIONS = [
    "Introduction/Model Description",
    "Usage/How to Use/Where to Use",
    "Model Limitations",
    "Evaluation/Performance/Results",
    "Training Info",
    "Citation/References",
    "License",
    "Contributions and Acknowledgement"
]

INVALID_TOKENS = [
    "<|endoftext|>",
    "<|startoftext|>",
    "<|assistant|>",
    "<|user|>",
    "<|system|>",
    "<|newline|>",
    "<|padding|>",
    "<|mask|>",
    "\u0000",
    "\u2028",
    "\u2029",
    "\r",
    "\t",
    "<|im_start|>",
    "<|im_end|>"
]


def clean_invalid_tokens(text):
    if not isinstance(text, str):
        return text
    for token in INVALID_TOKENS:
        text = text.replace(token, "")
    return text.strip()


def create_jsonl_data(df):
    jsonl_data = []

    for _, row in df.iterrows():
        readme_text = clean_invalid_tokens(str(row['Full Readme Text']))

        system_message = {
            "role": "system",
            "content": (
                "You are an intelligent system that analyzes README files "
                "from Hugging Face models. Your task is to extract and "
                "classify 8 key components from the README content provided "
                "below. Identify whether each component is present or absent "
                "and provide the content of each present component."
            )
        }

        user_message = {
            "role": "user",
            "content": f"README Content:\n---\n{readme_text}\n---"
        }

        completion_parts = []
        present_sections = []
        absent_sections = []

        for section in SECTIONS:
            if pd.notnull(row[section]):
                content = clean_invalid_tokens(str(row[section]))
                completion_parts.append(
                    f"Status of {section}: PRESENT\n\n  Content related to "
                    f"{section} identified in the README: {content}"
                )
                present_sections.append(section)
            else:
                completion_parts.append(f"Status of {section}: ABSENT")
                absent_sections.append(section)

        completion_parts = (
            "\n".join(completion_parts) +
            "\n\n\nList of Present Sections: " + ", ".join(present_sections) +
            "\n\n\nList of Absent Sections: " + ", ".join(absent_sections)
        )

        assistant_message = {
            "role": "assistant",
            "content": completion_parts
        }

        jsonl_data.append({
            "messages": [system_message, user_message, assistant_message]
        })

    return jsonl_data


def main():
    file_path = 'final_categorized_data.xlsx'
    df = pd.read_excel(file_path)

    jsonl_data = create_jsonl_data(df)

    output_path = 'readme_sections_with_chat_format.jsonl'
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in jsonl_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    print(f"Chat-formatted dataset saved to {output_path}")


if __name__ == '__main__':
    main()
