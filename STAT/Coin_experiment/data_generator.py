import numpy as np, time, csv


def generate_n_coins(n: int) -> np.ndarray:
    """
    :param n: Number of coins to generate. Represents the size of the array.
    :return: A numpy array containing n elements, where each element is either 0 or 1, representing a coin flip result.
    """
    return np.random.randint(0, 2, size=(n,))


def find_biggest_streak(sample: np.ndarray) -> tuple[int, int]:
    """
    :param sample: A numpy array consisting of binary values where 1 represents heads and 0 represents tails.
    :return: A tuple containing the maximum streaks of heads and tails respectively.
    """
    # 1 - heads
    # 0 - tails
    max_streak_h: int = -1
    max_streak_t: int = -1
    streak: int = 0

    prev_toss: int = -1
    for toss in sample:
        if toss == prev_toss:
            streak += 1
        else:
            if prev_toss == 1:
                max_streak_h = max(max_streak_h, streak)
            else:
                max_streak_t = max(max_streak_t, streak)
            streak = 0
        prev_toss = toss
    if prev_toss == 1:
        max_streak_h = max(max_streak_h, streak)
    else:
        max_streak_t = max(max_streak_t, streak)

    return max_streak_h, max_streak_t


def count_heads_and_tails(sample: np.ndarray) -> tuple[int, int]:
    """
    :param sample: A numpy array containing binary values representing heads (1) and tails (0).
    :return: A tuple containing the count of heads (1) and tails (0) in the given sample.
    """
    uniq, count = np.unique(sample, return_counts=True)
    result = dict(zip(uniq, count))
    return result.get(1, 0), result.get(0, 0)


def generator_worker(n: int, sample_size: int = 100, sleep_time_ns: int = 0):
    """
    :param n: Number of samples to generate.
    :param sample_size: Size of each sample, default is 100.
    :param sleep_time_ns: Time to sleep between generating samples in nanoseconds, default is 0.
    :return: None
    """
    with open('samples.csv', 'w') as samples_csv, open('samples_calc.csv', 'w') as samples_calc_csv:
        samples_csv_reader = csv.writer(samples_csv, delimiter=',', lineterminator='\n')
        samples_calc_csv_reader = csv.writer(samples_calc_csv, delimiter=',', lineterminator='\n')
        first_col = []
        for i in range(n):
            first_col.append(f'toss_{i}')
        samples_csv_reader.writerow(first_col)
        first_col = ['streak', 'heads', 'tails', 'mean']
        samples_calc_csv_reader.writerow(first_col)

        for _ in range(n):
            sample = generate_n_coins(sample_size)
            samples_csv_reader.writerow(sample)

            samples_calc_csv_reader.writerow(
                tuple([max(find_biggest_streak(sample))] + list(count_heads_and_tails(sample)) + [sample.mean()]))
            time.sleep(sleep_time_ns / 1000)
