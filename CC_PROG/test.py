import math, statistics, pandas as pd, numpy as np


def main() -> None:
    """
    Calculates the final grade based on individual test and assignment scores for two semester terms.
    The grades considered include theory tests, mini quizzes, lab tests, and lab assignments.
    Each grade is individually weighted and the final cumulative grade is derived by summing the weighted scores.

    :return: None
    """
    theory_test1_s1: float = 6.
    theory_test2_s1: float = 4.7
    theory_mini_quiz_s1: float = 6.

    lab_test1_s1: float = 5.
    lab_test2_s1: float = 6.
    lab_asiignment_s1: float = 6.

    theory_test1_s2: float = 6.
    theory_test2_s2: float = 5.
    theory_mini_quiz_s2: float = 6.

    lab_test1_s2: float = 4.3
    lab_test2_s2: float = 4.56
    lab_asiignment_s2: float = 3.

    grouped: np.ndarray = np.array((theory_test1_s1, theory_test2_s1, theory_mini_quiz_s1,
                                    lab_test1_s1, lab_test2_s1, lab_asiignment_s1,
                                    theory_test1_s2, theory_test2_s2, theory_mini_quiz_s2,
                                    lab_test1_s2, lab_test2_s2, lab_asiignment_s2))
    # print(grouped)

    mask: np.ndarray = np.array(((.35, .45, .20) * 4))
    # print(mask)

    final_grade: np.ndarray = np.sum(grouped * mask) / 4
    # print(grouped * mask)

    print(f'''All 4 >= grades: {all((True if grade >= 4. else False for grade in grouped))}
FINAL GRADE = {final_grade: .4}''')


if __name__ == '__main__':
    main()
