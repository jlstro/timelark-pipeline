# Timelark Data Pipeline

This very basic data pipeline built in Python is part of the Timelark project. It reads unstructured text from text files, extracts named entities using spaCy, queries the Aleph API to enrich these entities, and saves the enriched data to an SQLite database. From here it can be visualized.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)

## Prerequisites

- Python 3.x
- [spaCy](https://spacy.io/) and spaCy model (e.g., en_core_web_lg)
- [Dataset](https://dataset.readthedocs.io/en/latest/index.html) (sqlite wrapper)
- Aleph API access and API key (for example [OCCRP's Aleph](https://aleph.occrp.org/))
- [Confection](https://github.com/explosion/confection) (for configuration management)

## Installation

Clone this repository:

```bash
git clone <https://github.com/jlstro/timelark-pipeline.git>
cd timelark-pipeline
```

Create a virtual environment and nstall the required Python packages:

```bash
python3 -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
python3 -m pip install spacy confection dataset
```

Download and install the spaCy model (e.g., "en_core_web_lg"):

``` bash
python3 -m spacy download en_core_web_lg
```

## Configuration

1. Create a configuration file named `config.cfg` in the root directory of the repository. Define the paths to your database, text files, and other configuration values as needed. Refer to the [confection documentation](https://github.com/timelark/confection) for more information on writing the configuration.

Example `config.cfg`:

```ini
[paths]
db = "./db/data.db"
files = "./text_files"

[aleph]
host = "https://aleph.occrp.org"
collections = 25, 55, 90
```

Make sure you set your Aleph API key as an environment variable named ALEPH_API_KEY.

Running the Pipeline

Run the main script to start the pipeline:

```bash
python3 main.py
```

The pipeline will read text files from the specified directory, extract entities, enrich them using the API, and save the enriched data to the SQLite database.
