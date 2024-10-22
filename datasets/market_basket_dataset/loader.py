import pandas as pd
from datasets.common.loading import get_abs_path
from datasets.common.dataset import Dataset

# https://www.kaggle.com/datasets/aslanahmedov/market-basket-analysis

def load_data():
    # Load the dataset
    file_path = get_abs_path(__file__, 'Assignment-1_Data.csv')

    dtypes = {
        'BillNo': str,
        'Itemname': str,
        'Quantity': int,
        'Date': str,  # Or use parse_dates
        'Price': str,  # We'll clean this up later
        'CustomerID': str,
        'Country': str
    }

    data = pd.read_csv(file_path, delimiter=";", dtype=dtypes)
    # Remove data lines with nil transaction id or item name
    data = data.dropna(subset=['BillNo', 'Itemname'])

    # Display the first few rows of the dataset to ensure it's loaded correctly
    print('Data [Market Basket] loaded successfully')
    print(data.head())

    return data

def std():
    data = load_data()
    # Group the items bought by each member on each date
    transactions = data.groupby(['BillNo'])['Itemname'].apply(list).values.tolist()
    ds = Dataset("Market Basket", transactions)

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
