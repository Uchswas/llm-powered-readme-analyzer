import os

import pandas as pd


def find_readme_content(file_name, directory):
    file_name = file_name + '.md'
    file_path = os.path.join(directory, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "File not found"


def main():
    file_path = 'Paul processed_data.xlsx'
    data = pd.read_excel(file_path)

    directory_path = '../readme_files'

    data['Readmetext'] = data['Modelname'].apply(
        lambda x: find_readme_content(x, directory_path)
    )

    output_path = 'Processed_Paul_processed_data.xlsx'
    data.to_excel(output_path, index=False)

    print(f"Processed file saved to: {output_path}")


if __name__ == '__main__':
    main()
