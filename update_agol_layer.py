name: Update AGOL Feature Layer

on:
  schedule:
    - cron: '*/5 * * * *'  # Run every 5 minutes
  workflow_dispatch:

jobs:
  update-agol-layer:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install arcgis

      - name: Update AGOL Feature Layer
        run: |
          python update_agol_layer.py
        env:
          AGOL_USERNAME: ${{ secrets.AGOL_USERNAME }}
          AGOL_PASSWORD: ${{ secrets.AGOL_PASSWORD }}
          AGOL_ITEM_ID: ${{ secrets.AGOL_ITEM_ID }}
