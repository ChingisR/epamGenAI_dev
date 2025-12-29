# Local GenAI RAG with Elasticsearch & Mistral

## Install Ollama

## Install Elasticsearch & Kibana (Docker)

## Setup the virtual Python environment

#### install pyenv

Modify the path so that pyenv is in the path variable

install dependencies for building python versions

## Write the data to Elasticsearch

## Check the data in Elasticsearch
1. go to kibana http://localhost:5601/app/management/data/index_management/indices and see the new index called calls
2. go to dev tools and try out this query `GET calls/_search?size=1` http://localhost:5601/app/dev_tools#/console/shell

## Query data from elasticsearch and create an output with Mistral
1. if everything is good then run the query.py file
2. try a few queries :)

## Install libraries to extract text from pdfs
pip install PyPDF2 pdfplumber PyMuPDF
