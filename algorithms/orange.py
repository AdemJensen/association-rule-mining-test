import time

from orangecontrib.associate.fpgrowth import *  # For association rule mining

def orange(dataset, min_support=0.1, min_confidence=0.05):
    start_time = time.time()
    # Find frequent itemsets (min_support = 0.01 means at least 1% of transactions must contain the itemset)
    itemsets = dict(frequent_itemsets(dataset.orange(), min_support=min_support))
    # print(f"Found {len(itemsets)} frequent itemsets, took {time.time() - start_time:.2f} seconds")

    # Generate association rules (min_confidence = 0.5)
    start_time = time.time()
    rules = list(association_rules(itemsets, min_confidence=min_confidence))
    # print(f"Found {len(rules)} association rules, took {time.time() - start_time:.2f} seconds")

    # Output the association rules
    # for r in rules:  # Display the rules
    #     # Decode item indices back to item names
    #     antecedent = [dataset.name_of(idx) for idx in r[0]]
    #     consequent = [dataset.name_of(idx) for idx in r[1]]
    #
    #     print(f"Rule: {antecedent} -> {consequent}, Support: {r[2]}, Confidence: {r[3]}")

    return rules