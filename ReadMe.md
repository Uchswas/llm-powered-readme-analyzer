## LLM-Powered README Analyzer


![LLM](https://img.shields.io/badge/LLM-FINE--TUNING-10A37F?style=for-the-badge&logo=openai&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-4A90E2?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


A well-written README is crucial for open-source projects. It helps developers understand, use, and contribute to models. Poor documentation leads to confusion, lower adoption rates, and wasted time. However, many README files lack essential information or are poorly structured.

Our project addresses this problem by providing an automated solution to analyze and improve README quality. We built an **LLM-powered** web application that analyzes README files from Hugging Face models. We used quantitative analysis to identify 8 key documentation components. Then we fine-tuned GPT-4o with our custom dataset. **Our fine-tuned model** identifies which sections are present or absent in any README. This helps developers improve the quality of their documentation.

To create this system, we developed a complete **data pipeline**. We scraped over 1 million Hugging Face models using **multi-threaded web scraping**. We extracted and parsed README files using **BeautifulSoup**. We manually labeled 200 top READMEs. We transformed the data into **OpenAI's chat format** for fine-tuning. We then integrated the fine-tuned model in a **Flask web application**. The application provides **real-time README analysis** through a simple web interface.

> **Note**: More comprehensive details and results of our study can be found in [`Project_Documentation.pdf`](Project_Documentation.pdf).


### Project Structure

#### Data Collection
- **`metadata collection/crawl_model_metadata.py`**  
  Fetches model metadata from Hugging Face API (model IDs, downloads, likes, etc.)  
  *Why:* We need comprehensive metadata to identify and prioritize the most popular models for our analysis.

- **`metadata extraction/metadata extraction.py`**  
  Filters and sorts model metadata by downloads/likes, extracts the top 5% popular models, and converts to CSV format  
  *Why:* Focusing on top-performing models ensures we train on high-quality README examples that represent best practices.

- **`readme file collection/retrieve_model_readme.py`**  
  Multi-threaded web scraper to download README files from Hugging Face models using API authentication  
  *Why:* Multi-threading enables efficient parallel downloads of thousands of README files, significantly reducing collection time.

- **`readme file collection/format_readme_name_files.py`**  
  Utility script to rename and organize downloaded README files  
  *Why:* Standardized file naming ensures consistent processing and prevents conflicts when handling multiple models.

#### Data Processing
- **`analyzer/get_headers.py`**  
  Extracts headers and content from Markdown files using BeautifulSoup, exports structured data to Excel  
  *Why:* Breaks down READMEs into structured sections (headers + content) and exports to Excel with empty "Comment" columns. This format makes manual labeling efficient - labelers can see each section separately and assign categories (like "Usage", "Installation") in the Comment columns.

- **`analyzer/process_data.py`**  
  Processes Excel files containing labeled README sections, standardizes labels, and generates label counts  
  *Why:* Label standardization creates consistent categories across all READMEs, enabling reliable model training.

- **`analyzer/write_full_readme.py`**  
  Reads model names from Excel and retrieves corresponding full README text files  
  *Why:* After manual labeling, we need the complete original README text alongside the labeled sections. This combines the structured labels with full context, creating complete training examples that include both categorized sections and the entire README for comprehensive model training.

#### Model Training
- **`training_and_application/src/make_json_for_fine_tuning.py`**  
  Converts labeled Excel data into OpenAI chat-format JSONL for fine-tuning, includes token cleaning  
  *Why:* OpenAI's fine-tuning API requires a specific JSONL format with chat messages. Token cleaning prevents errors from reserved tokens.

- **`training_and_application/src/fine_tune_model.py`**  
  Uploads the JSONL training file to OpenAI and creates a fine-tuning job  
  *Why:* Automates the fine-tuning process, eliminating manual API calls and providing a reproducible training workflow.

#### Web Application
- **`training_and_application/web/app.py`**  
  Flask web application that serves the README analyzer interface and integrates with a fine-tuned GPT-4o model  
  *Why:* Provides an accessible interface for users to analyze READMEs without needing to run Python scripts or understand the underlying model.

- **`training_and_application/web/templates/`**  
  HTML templates for the web interface (index.html, result.html)  
  *Why:* Templates separate presentation from logic, making the UI easy to modify and maintain.


### How to Use

This section provides step-by-step instructions for fine-tuning the model and running the web application.

#### Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.x** - Required for running the application
- **pip** - Python package manager
- **OpenAI API Key** - Obtain from [OpenAI Platform](https://platform.openai.com/api-keys)

#### Fine-Tuning the Model

Follow these steps to fine-tune GPT-4o with your custom dataset:

1. **Clone the repository** and navigate to the training directory:
   ```bash
   git clone <repository-url>
   cd training_and_application
   ```

2. **Create a virtual environment** to isolate dependencies:
   ```bash
   python3 -m venv venv-readme-genai
   source venv-readme-genai/bin/activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

5. **Run the fine-tuning script**:
   ```bash
   cd src
   python3 fine_tune_model.py
   ```

   This will upload the training file and dispatch the fine-tuning job. **Save the `FINE_TUNE_MODEL_ID`** from the output for use in the web application.

#### Running the Application

To run the web application:

1. **Configure the model ID** in `.env`:
   - Add `FINE_TUNE_MODEL_ID=your_model_id` to your `.env` file
   - Alternatively, use the pre-trained model: `ft:gpt-4o-2024-08-06:personal::AUWHEdAd`

2. **Start the Flask server**:
   ```bash
   cd web
   python3 app.py
   ```

3. **Access the application**:
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Paste or upload a README file to analyze 



### Appendix

**Datasets and Resources:**

- [Training Data](https://github.com/YinanWusoymilk/hf-readme/blob/main/training_and_application/src/readme_sections_with_chat_format.jsonl) - JSONL file used for fine-tuning the model
- [Initial Dataset](https://github.com/YinanWusoymilk/hf-readme/tree/main/training_and_application/readme_files) - Dataset of top 5% README files from Hugging Face
- [Labeled Data](https://docs.google.com/spreadsheets/d/1wHXhcHM97zLgiJZsYCyEkP2HWW4-bZaoA7lVaknqVAA/edit?usp=sharing) - Manually labeled data for 200 top README files
- [Evaluation Data](https://docs.google.com/spreadsheets/d/1Yxpfca3pIkBKJzdOjNxDRFXs1xdVCCZsu_8odgHkkaM/edit?usp=sharing) - Data used for tool evaluation

