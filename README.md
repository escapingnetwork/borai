# BORAI: Boletín Oficial de la Republica Argentina Information Extractor

BORAI is a Python application that scrapes, processes, and summarizes web articles from Boletín Oficial de la Republica Argentina using Google Gemini Pro. It focuses on specific areas of interest such as "Resoluciones", "Leyes", "Decretos", and "Disposiciones". The processed information is then stored in a JSON file and published on X and Urbit.

* Urbit Hosted Blog

    https://borai.com.ar

* Urbit Group Invite

    https://tlon.network/lure/~dibref-labter/arbit

* X Account

    https://x.com/borargia


## Features

* **Web Scraping**: Scrapes web articles from Boletín Oficial de la Republica Argentina.
* **Data Processing**: Processes and summarizes the scraped data, focusing on "Resoluciones", "Leyes", "Decretos", and "Disposiciones" using Google Gemini Pro.
* **Data Storage**: Stores the processed information in a JSON file.
* **Data Publication**: Reads data from the JSON file, ranks and sorts the data, and then publishes it on X and Urbit.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/escapingnetwork/borai.git
```

You need to install the required Python packages:
```bash
pip install -r requeriments.txt
```

#### Environment Variables

The script requires the following environment variables:
```bash
URBIT_SHIP_URL
URBIT_SHIP_CODE
URBIT_SHIP
URBIT_DIARY
X_BEARER
X_API_KEY
X_API_KEY_SECRET
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
```

#### Usage

Run the script for scrapping with Python:
```bash
python resume/main.py

```

Run the script for publishing with Python:
```bash
python urbit/main.py

```

Run the script for publishing with Python:
```bash
python x/main.py

```

### Acknowledgments

This project is inspired by [Boletin AM](https://github.com/drkrillo/boletin-am). We appreciate the ideas and efforts put into that project, which served as a stepping stone for this one.