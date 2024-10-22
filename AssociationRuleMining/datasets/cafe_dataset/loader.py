import pandas as pd
from AssociationRuleMining.datasets.common.loading import get_abs_path
from AssociationRuleMining.datasets.common.dataset import Dataset

# https://www.kaggle.com/datasets/ahmedalorage/cafe-datasets
# This dataset is not recommended, as it does not have any transaction with more than one item

def load_data():
    # Load the dataset
    file_path = get_abs_path(__file__, 'DM-case1- Cafe.csv')

    data = pd.read_csv(file_path, delimiter=";")

    # Display the first few rows of the dataset to ensure it's loaded correctly
    print('Data [Cafe] loaded successfully')
    print(data.head())

    return data

def std():
    data = load_data()
    # Group the items bought by each member on each date
    transactions = data.groupby(['transaction_id'])['product_id'].apply(list).values.tolist()
    ds = Dataset("Cafe", transactions)

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
