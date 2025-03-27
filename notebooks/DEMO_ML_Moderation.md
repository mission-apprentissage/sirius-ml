# SIRIUS DEMO ML Moderation

This project is part of the SIRIUS initiative, focusing on the moderation of verbatim comments. It provides tools for processing, encoding, and analyzing textual data using machine learning models.

## Features

- **Moderation Rules**:
  - Pending: Verbatim awaiting processing.
  - VALIDATED: Can be exposed.
  - TO_FIX: Needs adjustments due to sensitive or inappropriate content.
  - ALERT: Highlights critical situations for internal use.
  - REJECTED: Invalid comments that will not be exposed.
  - GEM: Particularly interesting comments (positive or negative).

- **Alert Rules**:
  - Detects insults.
  - Identifies personal data.

- **Correction Rules**:
  - Fixes spelling and grammar errors.
  - Replaces names with personal pronouns.

## Dataset Processing

The project includes a `Datas` class for handling datasets:
- **Read**: Fetches data from an API.
- **Prepare**: Formats and cleans the dataset.
- **Encode**: Generates embeddings using a SentenceTransformer model.
- **Save**: Exports the dataset to Hugging Face Hub.
- **Load**: Imports datasets from Hugging Face Hub.

## Usage

1. Set environment variables:
- SIRIUS_DB_API: API endpoint for fetching data.
- SIRIUS_HF_TOKEN: Hugging Face token for dataset operations.
- table: Name of the database table (e.g., verbatims).
- repo: Hugging Face repository for storing datasets.

2. Run the notebook to:
- Load and prepare the dataset.
- Encode text data using a pre-trained model.
- Export the processed dataset.
- Visualize moderation statistics using the provided plotting tools.

## Model Information

- Model: CamemBERT(a)-v2
- Publication date: November 2024
- Paper: [arXiv:2411.08868](https://arxiv.org/abs/2411.08868)

## License

This project is licensed under the [GNU AGPL License](https://www.gnu.org/licenses/agpl-3.0.fr.html#license-text).

## Author

Do HUYNH ([@huynhdoo](https://github.com/huynhdoo))