import pandas as pd
from datasets.common.loading import get_abs_path
from datasets.common.dataset import Dataset

# https://www.kaggle.com/datasets/marian447/retail-store-sales-transactions/data

def load_data():
    # Load the dataset
    file_path = get_abs_path(__file__, 'scanner_data.csv')

    data = pd.read_csv(file_path)

    # Display the first few rows of the dataset to ensure it's loaded correctly
    print('Data [Retail Store] loaded successfully')
    print(data.head())

    return data

def std():
    data = load_data()
    # Group the items bought by each member on each date
    transactions = data.groupby(['Date', 'Customer_ID', 'Transaction_ID'])['SKU'].apply(list).values.tolist()
    ds = Dataset("Retail Store", transactions)

    return ds


if __name__ == '__main__':
    # print(__file__)
    ds = std()
    ds.print_basics()
    # ds1 = ds.resample_by_transactions(32)
    # ds1.print_basics()
    # ds1.save('Groceries_dataset_tx_100.json')
    #
    # ds2 = ds.resample_by_unique_items(50)
    # ds2.print_basics()
    # ds2.save('Groceries_dataset_ui_20.json')
