import tempfile

from mnist import MNIST
from google.cloud import bigquery
from bigquery_utils import read_bigquery_schema_from_file

import pandas
import os
import click
import logging

label_dict = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot",
}


def build_records(images, labels, subset, offset_id=0):
    records = []
    for i, (image, label) in enumerate(zip(images, labels)):
        records.append(
            {
                "image_id": i + 1 + offset_id,
                "subset": subset,
                "class": label_dict[label],
                "pixels": image,
            }
        )
    return records


@click.command()
@click.option(
    "--dataset-name",
    default="fashion_mnist_dev",
    type=str,
    help="BigQuery dataset name",
)
@click.option(
    "--table-name", default="fashion_mnist", type=str, help="BigQuery table name"
)
@click.option(
    "--output-dir",
    type=str,
    help="The output directory to store json file to load to BigQuery",
)
def load_bigquery(dataset_name, table_name, output_dir):
    """Load fashion-mnist data to BigQuery"""
    mndata = MNIST("./resources/data")
    mndata.gz = True

    train_images, train_labels = mndata.load_training()
    test_images, test_labels = mndata.load_testing()

    train_records = build_records(train_images, train_labels, "train")
    test_records = build_records(
        test_images, test_labels, "test", offset_id=len(train_records)
    )

    dataframe = pandas.DataFrame(
        train_records + test_records,
        columns=[
            "image_id",
            "subset",
            "class",
            "pixels",
        ],
    )
    if output_dir is None:
        output_dir = tempfile.gettempdir()

    json_path = os.path.join(output_dir, "fashion_mnist.json")
    dataframe.to_json(json_path, orient="records", lines=True)
    schema_path = os.path.join(os.getcwd(), "resources/schema/fashion_mnist.json")
    job_config = bigquery.LoadJobConfig(
        schema=read_bigquery_schema_from_file(schema_path),
        write_disposition="WRITE_TRUNCATE",
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    client = bigquery.Client()
    table_id = f"{dataset_name}.{table_name}"
    with open(json_path, "rb") as json_file:
        job = client.load_table_from_file(json_file, table_id, job_config=job_config)
    job.result()


if __name__ == "__main__":
    load_bigquery()
