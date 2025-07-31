from argparse import ArgumentParser
from itertools import batched

import ir_datasets
import requests
from tqdm import tqdm


def sanitize(s: str | None):
    """Remove 0x00 bytes from a string as Postgres cannot handle them.

    :param s: Input string.
    :return: Sanitized input string.
    """
    return None if s is None else s.replace("\x00", "")


def main():
    ap = ArgumentParser()
    ap.add_argument("DATASET_ID", type=str, help="Dataset identifier for ir-datasets.")
    ap.add_argument("DATASET_NAME", type=str, help="Name of dataset in ir-explorer.")
    ap.add_argument("CORPUS_NAME", type=str, help="Name of corpus in ir-explorer.")
    ap.add_argument(
        "--batch_size", type=int, default=2**8, help="How many items to add at once."
    )
    ap.add_argument("--language", default="English", help="Corpus language.")
    ap.add_argument(
        "--min_relevance",
        type=int,
        default=1,
        help="Minimum relevance score for the dataset.",
    )
    ap.add_argument(
        "--add_corpus", action="store_true", help="Whether to add the documents."
    )
    ap.add_argument("--hostname", default="localhost", help="Backend hostname.")
    ap.add_argument("--port", type=int, default=8103, help="Backend port.")
    ap.add_argument(
        "--document_text_attr",
        default="text",
        help="Attribute name to use for getting the document text.",
    )
    ap.add_argument(
        "--document_title_attr",
        default="title",
        help="Attribute name to use for getting the document title.",
    )
    ap.add_argument(
        "--query_text_attr",
        default="text",
        help="Attribute name to use for getting the query text.",
    )
    ap.add_argument(
        "--query_description_attr",
        default="description",
        help="Attribute name to use for getting the query description.",
    )
    args = ap.parse_args()

    backend_url = f"http://{args.hostname}:{args.port}"

    ds = ir_datasets.load(args.DATASET_ID)

    if args.add_corpus:
        requests.post(
            backend_url + "/create_corpus",
            json={"name": args.CORPUS_NAME, "language": args.language},
        )
        for batch in tqdm(
            batched(ds.docs_iter(), args.batch_size),
            total=int(ds.docs_count() / args.batch_size) + 1,
            desc="Adding documents",
        ):
            requests.post(
                backend_url + "/add_documents",
                json=[
                    {
                        "id": doc.doc_id,
                        "title": sanitize(getattr(doc, args.document_title_attr, None)),
                        "text": sanitize(getattr(doc, args.document_text_attr)),
                    }
                    for doc in batch
                ],
                params={"corpus_name": args.CORPUS_NAME},
            )

    requests.post(
        backend_url + "/create_dataset",
        json={
            "name": args.DATASET_NAME,
            "corpus_name": args.CORPUS_NAME,
            "min_relevance": args.min_relevance,
        },
    )

    for batch in tqdm(
        batched(ds.queries_iter(), args.batch_size),
        total=int(ds.queries_count() / args.batch_size) + 1,
        desc="Adding queries",
    ):
        requests.post(
            backend_url + "/add_queries",
            json=[
                {
                    "id": query.query_id,
                    "text": sanitize(getattr(query, args.query_text_attr)),
                    "description": sanitize(
                        getattr(query, args.query_description_attr, None)
                    ),
                }
                for query in batch
            ],
            params={"corpus_name": args.CORPUS_NAME, "dataset_name": args.DATASET_NAME},
        )

    for batch in tqdm(
        batched(ds.qrels_iter(), args.batch_size),
        total=int(ds.qrels_count() / args.batch_size) + 1,
        desc="Adding QRels",
    ):
        requests.post(
            backend_url + "/add_qrels",
            json=[
                {
                    "query_id": qrel.query_id,
                    "document_id": qrel.doc_id,
                    "relevance": qrel.relevance,
                }
                for qrel in batch
            ],
            params={"corpus_name": args.CORPUS_NAME, "dataset_name": args.DATASET_NAME},
        )


if __name__ == "__main__":
    main()
