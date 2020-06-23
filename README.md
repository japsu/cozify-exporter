# Cozify exporter for Prometheus

Reads values from Cozify API. Outputs them in a format suitable for Prometheus scraping.

TODO: Other metrics than temperature.

## Getting started

### First time setup

Create virtualenv and install deps:

    python3 -m venv venv
    source venv/bin/activate
    pip install -U pip setuptools wheel
    pip install -r requirements.txt

Authenticate to Cozify:

    python3 -c 'from cozify import cloud; cloud.authenticate()'

### Running the exporter

Start the server:

    python3 cozify_exporter.py

Listens on port 5000 by default. Verify that you can access http://localhost:5000/metrics, then configure your Prometheus instance to scrape it.
