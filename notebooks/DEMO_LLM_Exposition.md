# SIRIUS Demo LLM Exposition

This project contains a notebook demonstrating the use of natural language processing (LLM) tools for analyzing and moderating testimonials. It relies on libraries such as langchain, langchain-mistralai, and datasets.

## Features

### 1. About

- Project presentation and useful links

### 2. Dependencies

- Configuration of API keys for MistralAI and Hugging Face.
- Installation of dependencies via a requirements.txt file.

### 3. Data Loading

- Use of the datasets library to load a dataset of testimonials.
- Conversion of data into a Pandas DataFrame for manipulation.

### 4. Verbatim Analysis

- Extraction and display of testimonials marked as "GEM" (nuggets).
- Analysis of testimonials to identify positive and negative points.

### 5. LLM Tools

- Use of ChatMistralAI to generate summaries and responses based on prompts.
- Implementation of functions to:
- Expose themes addressed in testimonials.
- Classify testimonials by relevance.
- Correct spelling and grammar errors.
- Anonymize testimonials by replacing proper names.

### 6. Results

- Generation of summaries and analyses of testimonials.
- Display of corrections and anonymizations performed.

## Usage

1. Open the notebook in a compatible environment (e.g., Google Colab).
2. Configure your API keys in the environment:
```bash
os.environ['SIRIUS_MISTRAL_API_KEY'] = "your_mistral_api_key"
os.environ['HF_TOKEN'] = "your_huggingface_api_key"
```
3. Run the cells in order to load the data, analyze the testimonials, and generate results.

## Model Information

- Model: Mistral Large
- Publication date: november 2024
- Paper: [mistral-large-2407](https://mistral.ai/news/mistral-large-2407)

## License

This project is licensed under the [GNU AGPL License](https://www.gnu.org/licenses/agpl-3.0.fr.html#license-text).

## Author

Do HUYNH ([@huynhdoo](https://github.com/huynhdoo))