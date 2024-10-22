import random

import numpy as np
from scipy.stats import skewnorm
from datasets.common.dataset import Dataset

def generate_item_names(n):
    """
    Generate a list of n unique item names.
    If n <= 26, the items will be A, B, C, ..., Z.
    If n > 26, the items will be AA, AB, AC, ..., etc.
    """
    items = []
    for i in range(n):
        name = ""
        while i >= 0:
            name = chr(65 + (i % 26)) + name
            i = i // 26 - 1
        items.append(name)
    return items

def gen(n_uniq_items, n_transactions, longest_transaction_len, scale=2.0):
    """
    Generate dummy transactions where the distribution of transaction lengths follows an exponential distribution.

    Args:
    - n_uniq_items: Number of unique items.
    - n_transactions: Number of transactions to generate.
    - longest_transaction_len: Maximum length of a transaction.
    - scale: The lambda (rate parameter) for the exponential distribution. Smaller values make shorter transactions more common.

    Returns:
    - A list of transactions, each represented as a list of items.
    """
    # Generate unique item names (e.g., "A", "B", ..., "AA", "AB", ... for more than 26 items)
    items = generate_item_names(n_uniq_items)

    # Generate transactions
    transactions = []

    for _ in range(n_transactions):
        # Use the exponential distribution to determine the transaction length
        transaction_len = int(np.random.exponential(scale=scale))

        # Ensure the transaction length stays within [1, longest_transaction_len]
        transaction_len = max(1, transaction_len)  # At least 1 item in every transaction
        transaction_len = min(transaction_len, longest_transaction_len)

        # Randomly select items for this transaction
        transaction = random.sample(items, transaction_len)
        transactions.append(transaction)

    return Dataset("Dummy", transactions)


if __name__ == '__main__':
    dummy_ds = gen(10, 5, 5, -10)
    dummy_ds.print_basics()