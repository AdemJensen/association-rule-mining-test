import json
import random

import numpy as np
from matplotlib import pyplot as plt

class Dataset:

    # transactions: list of lists, sublist is a list of items.
    def __init__(self, name, transactions):
        self.name = name
        self.transactions = transactions
        self.unique_items = sorted(set(item for transaction in transactions for item in transaction))

    # Save the dataset to a file (as JSON)
    def save(self, filename):
        data = {
            'transactions': self.transactions,
            'unique_items': self.unique_items
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        print(f"Dataset saved to {filename}")

    # Load a dataset from a file (class method)
    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        transactions = data['transactions']
        print(f"Dataset loaded from {filename}")
        return cls(data['name'], transactions)

    def resample_by_transactions(self, n_transactions):
        transactions_copy = self.transactions[:]
        random.shuffle(transactions_copy)
        selected_transactions = transactions_copy[:n_transactions]
        return Dataset(self.name, selected_transactions)

    def resample_by_unique_items(self, n_uniq_items):
        # Step 1: Aggregate transactions by their unique items
        groups = {}
        for transaction in self.transactions:
            transaction_items = frozenset(transaction)  # Use frozenset to ensure immutability and grouping
            if transaction_items not in groups:
                groups[transaction_items] = []
            groups[transaction_items].append(transaction)

        # Step 2: Shuffle the aggregated transactions
        group_list = list(groups.values())
        random.shuffle(group_list)

        # Step 3: Select transactions to match the required number of unique items
        selected_transactions = []
        selected_items = set()

        for transaction_item_group in group_list:
            # Add the transaction to selected transactions
            selected_transactions.extend(transaction_item_group)
            selected_items.update(transaction_item_group[0])

            # Stop once we have exactly n_uniq_items unique items
            if len(selected_items) >= n_uniq_items:
                break

        # If we couldn't find enough unique items, raise an exception
        if len(selected_items) < n_uniq_items:
            raise Exception("Failed to find a proper subset with the required unique items.")

        # Convert the selected set of items back to list form for the transactions
        final_transactions = [list(transaction) for transaction in selected_transactions]

        # Step 4: Create a new Dataset object with the selected transactions
        new_dataset = Dataset(self.name, final_transactions)
        return new_dataset

    def resample(self, n_transactions, n_uniq_items, n_transactions_variance=5, n_uniq_items_variance=5):
        # Step 1: Copy and shuffle transactions
        transactions_copy = self.transactions[:]
        random.shuffle(transactions_copy)

        # Initialize the stack for iterative DFS (store index, current_transactions, and current_items)
        stack = [(0, [], set())]

        selected_transactions = []
        while stack:
            idx, current_transactions, current_items = stack.pop()

            # Stop if the number of transactions exceeds n_transactions + variance
            if len(current_transactions) > n_transactions + n_transactions_variance:
                continue

            # Stop if the number of unique items exceeds n_uniq_items + variance
            if len(current_items) > n_uniq_items + n_uniq_items_variance:
                continue

            # Stop condition: If the target transaction count and unique item count are reached (within variance)
            if (n_transactions - n_transactions_variance <= len(current_transactions) <= n_transactions and
                    n_uniq_items - n_uniq_items_variance <= len(current_items) <= n_uniq_items):
                selected_transactions = current_transactions
                break

            # If we've processed all transactions, continue to the next iteration
            if idx >= len(transactions_copy):
                continue

            # Push the state where the current transaction is included
            next_transactions = current_transactions + [transactions_copy[idx]]
            next_items = current_items.union(transactions_copy[idx])
            stack.append((idx + 1, next_transactions, next_items))

            # Push the state where the current transaction is excluded
            stack.append((idx + 1, current_transactions, current_items))

        # If we haven't found a valid set of transactions, raise an exception
        if not selected_transactions:
            raise Exception("Failed to find a proper subset within the given variance.")

        # Step 4: Create a new Dataset object with the selected transactions
        new_dataset = Dataset(self.name, selected_transactions)
        return new_dataset

    def name_of(self, idx):
        return self.unique_items[idx]

    def orange(self):
        item_mapping = {item: idx for idx, item in enumerate(self.unique_items)}
        return [list(set(item_mapping[item] for item in transaction)) for transaction in self.transactions]

    def print_basics(self):
        print(f"Number of transactions: {len(self.transactions)}")
        print(f"Number of unique items: {len(self.unique_items)}")
        print(f"Average transaction length: {sum(len(t) for t in self.transactions) / len(self.transactions):.2f}")
        print(f"Average items per unique item: {len(self.transactions) / len(self.unique_items):.2f}")
        print(f"Max transaction length: {max(len(t) for t in self.transactions)}")
        print(f"Min transaction length: {min(len(t) for t in self.transactions)}")
        print("Graph of transaction length:")
        # Assuming 'self.transactions' contains the list of transactions
        transaction_lengths = [len(t) for t in self.transactions]

        # Create the histogram, with bins representing discrete transaction lengths
        plt.figure(figsize=(4, 3))
        plt.title(f'TX Len Distribution for {self.name}')
        plt.hist(transaction_lengths, bins=range(1, max(transaction_lengths) + 2), align='left', rwidth=0.8)

        # Set x-axis ticks to display only a subset, every 5 values, for example
        plt.xticks(np.arange(1, max(transaction_lengths) + 1, step=5))

        # Optionally, if you want to hide the x-axis ticks entirely for tight x-axis labels:
        # plt.xticks([])

        # Ensure that the y-axis starts at 0 to prevent scaling issues
        plt.ylim(bottom=0)

        # Label the axes
        plt.xlabel('Number of items')
        plt.ylabel('Number of transactions')