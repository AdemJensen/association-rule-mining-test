# generate all possible itemsets then calculate support value
# if n items is given, 2^n itemsets are created
import time
from itertools import combinations

from scipy.optimize import brute


def gen_itemsets(datasets):
    item_list = []  # contain every item
    for transactions in datasets:
        for item in transactions:
            if item not in item_list:
                item_list.append(item)

    itemsets = []  # contain every possible itemset

    for i in range(1, len(item_list) + 1):
        comb = combinations(item_list, i)
        itemsets.extend(list(comb))

    return itemsets


# find how many times itemset exists in each transaction
def calculate_support(itemset, datasets):
    counter = 0
    for transaction in datasets:
        # Check if the itemset is a subset of the transaction
        result = all(elem in transaction for elem in itemset)
        if result:
            counter += 1
    support = counter / len(datasets)
    return support


# return a dictionary with itemset as keys and support as value
def gen_sup_list(itemsets, datasets, min_support=0.01):
    item_sup_dic = {}
    for itemset in itemsets:
        sup_val = calculate_support(itemset, datasets)
        if sup_val != 0:
            item_sup_dic.update({itemset: sup_val})
    d = dict((k, v) for k, v in item_sup_dic.items() if v >= min_support)
    return d


# Generate association rules based on frequent itemsets and minimum confidence
def gen_association_rules(frequent_itemsets, datasets, min_confidence=0.05):
    rules = []

    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue  # You can't generate rules from single-item itemsets

        # For each frequent itemset, generate all possible antecedent -> consequent rules
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                consequent = tuple(set(itemset) - set(antecedent))

                # Calculate support for the antecedent and the rule
                support_antecedent = calculate_support(antecedent, datasets)
                support_rule = frequent_itemsets[itemset]  # already calculated as support of itemset

                # Calculate confidence
                confidence = support_rule / support_antecedent

                # Add the rule if confidence is above the threshold
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, support_rule, confidence))

    # print(f"Generated {len(rules)} association rules")
    return rules


# Decode item indices into their names for displaying rules
def decode_rule(rule, datasets):
    antecedent = [datasets.name_of(idx) for idx in rule[0]]
    consequent = [datasets.name_of(idx) for idx in rule[1]]
    return antecedent, consequent, rule[2], rule[3]


# Complete procedure to get most frequent itemsets and association rules
def brute_force(datasets, min_support=0.01, min_confidence=0.05):
    start_time = time.time()
    transactions = datasets.orange()  # Use the custom orange() method to get transactions
    itemsets = gen_itemsets(transactions)

    # Generate frequent itemsets
    frequent_itemsets = gen_sup_list(itemsets, transactions, min_support=min_support)
    print(f"Found {len(frequent_itemsets)} frequent itemsets, took {time.time() - start_time:.2f} seconds")

    # Generate association rules
    start_time = time.time()
    association_rules = gen_association_rules(frequent_itemsets, transactions, min_confidence=min_confidence)
    print(f"Found {len(association_rules)} association rules, took {time.time() - start_time:.2f} seconds")

    return association_rules

time_coherent_1 = 4.917318813438344e-07
time_coherent_2 = 1.5227838708770355e-07

def estimate_time(datasets):
    m = len(datasets.transactions)
    n = len(datasets.unique_items)
    return 2 ** n * (time_coherent_1 + time_coherent_2 * m)

# Time Equation: time = 2^n * (C1 + C2 * m)
def calculate_time_est_coherent():
    import datasets.groceries_dataset.loader as groceries_dataset
    import numpy as np

    total_calc_time = 10
    sum_c1 = 0
    sum_c2 = 0

    dataset = groceries_dataset.std()
    for _ in range(total_calc_time):
        # Prepare the datasets
        ds1 = dataset.resample_by_unique_items(13)
        ds2 = dataset.resample_by_unique_items(16)
        run_times = 20

        start = time.time()
        for _ in range(run_times):
            brute_force(ds1)
        end = time.time()
        time1 = (end - start) / run_times
        n1 = len(ds1.unique_items)
        m1 = len(ds1.transactions)

        start = time.time()
        for _ in range(run_times):
            brute_force(ds2)
        end = time.time()
        time2 = (end - start) / run_times
        n2 = len(ds2.unique_items)
        m2 = len(ds2.transactions)

        # Solve the equation
        # We have two equations:
        # time1 = 2^n1 * (C1 + C2 * m1)
        # time2 = 2^n2 * (C1 + C2 * m2)

        # Solve the system of linear equations to find C1 and C2
        a = np.array([[2 ** n1, 2 ** n1 * m1], [2 ** n2, 2 ** n2 * m2]])  # Coefficient matrix
        b = np.array([time1, time2])  # Time vector

        # Solve for C1 and C2
        c1, c2 = np.linalg.solve(a, b)
        sum_c1 += c1
        sum_c2 += c2

    c1 = sum_c1 / total_calc_time
    c2 = sum_c2 / total_calc_time
    # Output C1 and C2 values
    print(f"C1 = {c1}, C2 = {c2}")

    return c1, c2


if __name__ == '__main__':
    C1, C2 = calculate_time_est_coherent()
    print(C1)
    print(C2)

    import datasets.groceries_dataset.loader as groceries_dataset
    dataset = groceries_dataset.std()
    ds1 = dataset.resample_by_unique_items(13)
    ds2 = dataset.resample_by_unique_items(16)
    print(estimate_time(ds1)) # 0.12
    print(estimate_time(ds2)) # 0.91



