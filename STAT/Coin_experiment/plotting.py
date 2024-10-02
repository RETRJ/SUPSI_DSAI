import matplotlib.pyplot as plt, data_generator, pandas as pd, numpy as np
from scipy.interpolate import make_interp_spline


def create_coin_dict() -> dict[int: int]:
    """
    Reads coin data from a CSV file and creates a dictionary with coin values as keys
    and their corresponding counts as values. Missing coin values in the sequence will
    have a count of zero.

    :return: A dictionary where keys are coin values and values are their counts.
    """
    data: pd.DataFrame = pd.read_csv('samples_calc.csv')
    res: dict[int: int] = dict()
    for item in data.iterrows():
        res[int(item[1].iloc[0])] = res.get(int(item[1].iloc[0]), 0) + 1
    sorted_res: dict[int: int] = dict(sorted(res.items()))
    for item in range(list(sorted_res.keys())[0], list(sorted_res.keys())[-1]):
        sorted_res[item] = sorted_res.get(item, 0)
    return dict(sorted(sorted_res.items()))


def create_mean_list() -> list[float]:
    """
    Creates a list of mean values, where each mean is calculated incrementally as new data is
    added from a CSV file.

    :return: A list of mean values calculated incrementally.
    :rtype: list of float
    """

    def add_to_mean(mean: float, size: int, value: float) -> float:
        """
        :param mean: The current mean value of the list.
        :type mean: float
        :param size: The current size of the list.
        :type size: int
        :param value: The new value to be added to the list.
        :type value: float
        :return: The updated mean value after adding the new value.
        :rtype: float
        """
        return (mean * size + value) / (size + 1)

    data: pd.DataFrame = pd.read_csv('samples_calc.csv')
    current_mean: float = 0
    current_size: int = 0
    res: list[float] = list()
    for item in data.iterrows():
        current_mean = add_to_mean(current_mean, current_size, item[1].iloc[3])
        current_size += 1
        res.append(current_mean)
    return res


def draw_plot(n: int, s_s: int):
    """
    :param n: The number of samples to generate.
    :param s_s: The size of each sample.
    :return: None
    """
    data_generator.generator_worker(n, s_s)

    mean_list: list[float] = create_mean_list()
    data_dict: dict[int: int] = create_coin_dict()

    # plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

    ax1.bar(range(len(data_dict)), data_dict.values())

    x, y = np.array(range(len(data_dict.values()))), np.array(list(data_dict.values()))
    smoothed_list = make_interp_spline(x, y)
    X_ = np.linspace(x.min(), x.max(), 50 * (x.max() - x.min() + 1))
    Y_ = smoothed_list(X_)

    ax1.plot(X_, Y_, color='purple')
    print(list(data_dict.values()), max(list(data_dict.values())))
    ax1.set(ylim=(0, max(list(data_dict.values())) * 1.2))

    plt.sca(ax1)
    plt.xticks(range(len(data_dict)), data_dict.keys())
    plt.xlabel('Max streak')
    plt.ylabel('Amount')
    plt.title(f'Statistics for {n} samples of size {s_s}')

    ax2.plot(list(range(len(mean_list))), mean_list)
    # ax2.set(ylim=(0, 1))
    plt.sca(ax2)
    plt.xlabel('Amount of samples')
    plt.ylabel('Heads/Tails ratio')
    fig.tight_layout()
    plt.show()


def main() -> None:
    draw_plot(200, 20)


if __name__ == '__main__':
    main()
