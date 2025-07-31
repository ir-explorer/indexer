# IR explorer Indexer

Index datasets from [ir-datasets](https://ir-datasets.com/) directly into [ir-explorer](https://github.com/ir-explorer/ir-explorer).

The script is easiest run using [uv](https://docs.astral.sh/uv/).

## Usage

```bash
$ uv run main.py -h
usage: main.py [-h] [--batch_size BATCH_SIZE] [--language LANGUAGE]
               [--min_relevance MIN_RELEVANCE] [--add_corpus] [--hostname HOSTNAME]
               [--port PORT] [--document_text_attr DOCUMENT_TEXT_ATTR]
               [--document_title_attr DOCUMENT_TITLE_ATTR]
               [--query_text_attr QUERY_TEXT_ATTR]
               [--query_description_attr QUERY_DESCRIPTION_ATTR]
               DATASET_ID DATASET_NAME CORPUS_NAME

positional arguments:
  DATASET_ID            Dataset identifier for ir-datasets.
  DATASET_NAME          Name of dataset in ir-explorer.
  CORPUS_NAME           Name of corpus in ir-explorer.

options:
  -h, --help            show this help message and exit
  --batch_size BATCH_SIZE
                        How many items to add at once.
  --language LANGUAGE   Corpus language.
  --min_relevance MIN_RELEVANCE
                        Minimum relevance score for the dataset.
  --add_corpus          Whether to add the documents.
  --hostname HOSTNAME   Backend hostname.
  --port PORT           Backend port.
  --document_text_attr DOCUMENT_TEXT_ATTR
                        Attribute name to use for getting the document text.
  --document_title_attr DOCUMENT_TITLE_ATTR
                        Attribute name to use for getting the document title.
  --query_text_attr QUERY_TEXT_ATTR
                        Attribute name to use for getting the query text.
  --query_description_attr QUERY_DESCRIPTION_ATTR
                        Attribute name to use for getting the query description.
```

## Example

Indexing [`msmarco-document-v2`](https://ir-datasets.com/msmarco-document-v2.html) along the [`train` dataset](https://ir-datasets.com/msmarco-document-v2.html#msmarco-document-v2/train):

```bash
uv run main.py msmarco-document-v2/train train msmarco-document-v2 --add_corpus --document_text_attr body --batch_size 128
```

Indexing the [`trec-dl-19` dataset](https://ir-datasets.com/msmarco-document-v2.html#msmarco-document-v2/trec-dl-2019) afterwards:

```bash
uv run main.py msmarco-document-v2/trec-dl-2019 trec-dl-19 msmarco-document-v2 --batch_size 512
```
