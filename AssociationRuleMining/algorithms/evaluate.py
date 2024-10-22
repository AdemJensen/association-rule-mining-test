from ipywidgets import IntProgress, HTML, VBox
from IPython.display import display

from AssociationRuleMining.algorithms.orange import orange
from AssociationRuleMining.algorithms.brute_force import estimate_time
import time
import matplotlib.pyplot as plt

def eval_params(dataset, n_run_time=10, mode='support', min_val=0, max_val=1, other_val=0.05):
    # Create progress bar for running Orange on datasets
    run_progress = IntProgress(min=0, max=n_run_time, description='', bar_style='')
    run_label = HTML(value="Running Orange: 0% (0/{})".format(n_run_time))
    display(VBox([run_label, run_progress]))

    args = []
    run_times = []
    est_times = []
    # Run orange on different datasets
    for i in range(n_run_time):
        start_time = time.time()

        if mode == 'support':
            min_support = min_val + (max_val - min_val) * i / (n_run_time - 1)
            min_confidence = other_val
            args.append(min_support)
        else:
            min_confidence = min_val + (max_val - min_val) * i / (n_run_time - 1)
            min_support = other_val
            args.append(min_confidence)
        # Run orange with different parameters
        orange(dataset, min_support, min_confidence)

        run_time = (time.time() - start_time)
        run_times.append(run_time)
        est_times.append(estimate_time(dataset))

        # Update the outer progress bar and display percentage
        run_progress.value = i + 1
        percentage_outer = int((i + 1) / n_run_time * 100)
        run_label.value = f"Running Orange: {percentage_outer}% ({i + 1}/{n_run_time})"

    # Plotting the run times for both algorithms
    plt.figure(figsize=(4, 3))  # This makes the figure 1/4 of the default size (8x6)
    plt.plot(args, run_times, label='Orange')
    # plt.plot(args, est_times, label='Brute-Force')
    plt.legend()
    if mode == 'support':
        plt.xlabel(f'Min Support')
    else:
        plt.xlabel(f'Min Confidence')
    plt.ylabel('Run Time (seconds)')
    plt.title(f'Run Time across {mode} vals')
    plt.show()


def evaluate(datasets, n_run_time=10, mode='transactions', do_estimation=True, do_log=False):
    # Sort datasets by n_transactions
    if mode == 'transactions':
        datasets.sort(key=lambda x: len(x.transactions))
    else:
        datasets.sort(key=lambda x: len(x.unique_items))

    # Create progress bar for running Orange on datasets
    run_progress = IntProgress(min=0, max=len(datasets), description='', bar_style='')
    run_label = HTML(value="Running Orange: 0% (0/{})".format(len(datasets)))
    display(VBox([run_label, run_progress]))

    run_times = []
    est_times = []
    # Run orange on different datasets
    for i, dataset in enumerate(datasets):
        start_time = time.time()

        # Create inner progress bar for running Orange multiple times per dataset
        inner_progress = IntProgress(min=0, max=n_run_time, description='', bar_style='')
        inner_label = HTML(value="Inner Runs: 0% (0/{})".format(n_run_time))
        # display(VBox([inner_label, inner_progress]))

        for j in range(n_run_time):
            orange(dataset)
            inner_progress.value = j + 1

            # Update inner loop progress percentage
            percentage_inner = int((j + 1) / n_run_time * 100)
            inner_label.value = f"Inner Runs: {percentage_inner}% ({j + 1}/{n_run_time})"

        run_time = (time.time() - start_time) / n_run_time
        est_time = estimate_time(dataset)
        if do_log:
            run_time = round(run_time, 2)
            est_time = round(est_time, 2)
        run_times.append(run_time)
        est_times.append(est_time)

        # Update the outer progress bar and display percentage
        run_progress.value = i + 1
        percentage_outer = int((i + 1) / len(datasets) * 100)
        run_label.value = f"Running Orange: {percentage_outer}% ({i + 1}/{len(datasets)})"

    # Plotting the run times for both algorithms
    transaction_counts = [len(dataset.transactions) for dataset in datasets]
    uniq_items_counts = [len(dataset.unique_items) for dataset in datasets]
    plt.figure(figsize=(4, 3))  # This makes the figure 1/4 of the default size (8x6)
    plt.plot(transaction_counts if mode == "transactions" else uniq_items_counts, run_times, label='Orange')
    if do_estimation:
        plt.plot(transaction_counts if mode == "transactions" else uniq_items_counts, est_times, label='Brute-Force')
    plt.legend()
    plt.xlabel(f'Number of {"Transactions" if mode == "transactions" else "Unique Items"}')
    plt.ylabel('Average Run Time (seconds)')
    plt.title(f'Run Time across {"TX" if mode == "transactions" else "UI"} '
              f'({"n_UI" if mode == "transactions" else "n_TX"} = '
              f'{len(datasets[0].unique_items) if mode == "transactions" else len(datasets[0].transactions)})')
    plt.show()