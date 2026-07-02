## Data Download Script

This folder includes `download_github_zip.py`, a helper script to:

- Download one or more dataset links
- Convert GitHub `blob` URLs to direct download URLs
- Extract `.zip` files into this `data/` directory
- Delete the downloaded `.zip` file after successful extraction

### Prerequisite

- Python 3

### Usage

From the project root (`VASTKnowledgeGraphVisualization`), run:

```bash
python3 data/download_github_zip.py <url1> [url2 ...]
```

### Example (single link)

```bash
python3 data/download_github_zip.py \
  https://github.com/vast-challenge/2025-data/blob/main/MC1_release.zip
```

### Example (multiple links)

```bash
python3 data/download_github_zip.py \
  https://github.com/vast-challenge/2025-data/blob/main/MC1_release.zip \
  https://github.com/vast-challenge/2025-data/blob/main/DC_release.zip
```

### Optional flags

- `--dry-run`: show what will be downloaded without downloading
- `--output-dir <path>`: save and extract into another directory

Example:

```bash
python3 data/download_github_zip.py \
  --dry-run \
  https://github.com/vast-challenge/2025-data/blob/main/MC1_release.zip
```

## Dataset Creation script

`create_datasets.py` creates two additional Knowledge Graphs which can be used to try out the application:

- `genre_influence.json` relationships between songs and albums from the [VAST 2025 MC1](https://vast-challenge.github.io/2025/MC1.html) dataset, organized by musical genre.
- `asoiaf_interaction.json` undirected interaction graph of characters from JRR Martin's _A Song of Ice and Fire_ series, based from data from [https://github.com/mathbeveridge/asoiaf](https://github.com/mathbeveridge/asoiaf) by [Andrew Beveridge](https://github.com/mathbeveridge) released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Prerequisites

- Python 3
- Networkx

We recommend running `./dev.sh` the first time in order to create the python environment and activating the python environment.
From the project root (`VASTKnowledgeGraphVisualization`), run:

```
./dev.sh
source api/venv/bin/activate
```

### Usage

From the project root (`VASTKnowledgeGraphVisualization`), run:

```
python3 data/create_datasets.py
```

You will find the datasets in the `data` directory.

### Optional flags

- `--output-dir <path>`: save the datasets into another directory.

## Team

Contributions to this folder, from the git history:

- **Salvo Rinzivillo** — the download script and this guide.
- **Giulia Fabiani** — the dataset creation script and this guide.
