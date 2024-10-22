import pandas as pd
from datasets.common.loading import get_abs_path
from datasets.common.dataset import Dataset

# https://www.kaggle.com/heeraldedhia/groceries-dataset

def load_data():
    # Load the dataset
    file_path = get_abs_path(__file__, 'Groceries_dataset.csv')
    data = pd.read_csv(file_path)

    # Display the first few rows of the dataset to ensure it's loaded correctly
    print('Data [Groceries-dataset] loaded successfully')
    # print(data.head())

    return data

def std():
    data = load_data()
    # Group the items bought by each member on each date
    transactions = data.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).values.tolist()
    ds = Dataset("Groceries", transactions)

    return ds


if __name__ == '__main__':
    # print(__file__)
    ds = std()
    ds1 = ds.resample_by_transactions(32)
    ds1.print_basics()
    ds1.save('Groceries_dataset_tx_100.json')

    ds2 = ds.resample_by_unique_items(50)
    ds2.print_basics()
    ds2.save('Groceries_dataset_ui_20.json')
