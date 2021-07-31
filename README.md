# fashion-mnist

CLI lets you load [fashion-mnist](https://github.com/zalandoresearch/fashion-mnist) to BigQuery.

## Usage

```bash
Usage: load_bigquery.py [OPTIONS]

  Load fashion-mnist data to BigQuery

Options:
  --input-dir TEXT     The directory containing fashion-mnist files
  --dataset-name TEXT  BigQuery dataset name
  --table-name TEXT    BigQuery table name
  --output-dir TEXT    The output directory to store json file to load to
                       BigQuery
  --help               Show this message and exit.
```

### Example

```bash
python load_bigquery.py --dataset-name=fashion_mnist_dev --table-name=fashion_mnist
```

## Schema

| Column             | Type               | Description
|--------------------|--------------------|--------------
| image_id           | INTEGER            | Auto generated id
| subset             | STRING             | Whether data is train or test
| class              | STRING             | Image label as describe [here](https://github.com/zalandoresearch/fashion-mnist#labels)
| pixels             | INTEGER (REPEATED) | List of image pixels
