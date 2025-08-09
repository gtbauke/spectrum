import pandas as pd
import numpy as np

from argparse import ArgumentParser
from datetime import datetime


def random_range(start: float, end: float, num_samples: int) -> pd.Series:
    """
    Generates a Series of random floats within the specified range.

    Parameters:
    - start (float): The lower bound of the range.
    - end (float): The upper bound of the range.
    - num_samples (int): Number of samples to generate.

    Returns:
    - pd.Series: A Series containing random floats.
    """
    return pd.Series(np.random.uniform(start, end, num_samples))


def generate_random_dataset(num_variables: int = 2, num_samples: int = 100, low: float = 0, high: float = 100) -> pd.DataFrame:
    """
    Generates a random dataset with specified number of variables and samples.

    Parameters:
    - num_variables (int): Number of variables in the dataset.
    - num_samples (int): Number of samples in the dataset.

    Returns:
    - pd.DataFrame: A DataFrame containing the random dataset.
    """
    independent_vars = [f'var_{i}' for i in range(num_variables - 1)]
    dependent_var = 'target'

    data = {var: pd.Series(random_range(low, high, num_samples))
            for var in independent_vars}
    data[dependent_var] = pd.Series(random_range(low, high, num_samples))

    dataset = pd.DataFrame(data)
    return dataset


def save_dataset_to_csv(dataset: pd.DataFrame, file_path: str):
    """
    Saves the dataset to a CSV file.

    Parameters:
    - dataset (pd.DataFrame): The dataset to save.
    - file_path (str): The path where the CSV file will be saved.
    """
    dataset.to_csv(file_path, index=False)
    print(f"Dataset saved to {file_path}")


def main():
    parser = ArgumentParser(
        description="Generate a random dataset and save it to a CSV file."
    )

    parser.add_argument(
        "--num_variables",
        type=int,
        default=2,
        help="Number of independent variables in the dataset (default: 2)."
    )

    parser.add_argument(
        "--num_samples",
        type=int,
        default=100,
        help="Number of samples in the dataset (default: 100)."
    )

    parser.add_argument(
        "--low",
        type=float,
        default=0,
        help="Lower bound for the random values (default: 0)."
    )

    parser.add_argument(
        "--high",
        type=float,
        default=100,
        help="Upper bound for the random values (default: 100)."
    )

    parser.add_argument(
        "--output",
        type=str,
        default=f"{datetime.today().timestamp()}.csv",
        help="Output file path for the generated dataset (default: {TIMESTAMP}.csv)."
    )

    args = parser.parse_args()
    dataset = generate_random_dataset(
        num_variables=args.num_variables,
        num_samples=args.num_samples,
        low=args.low,
        high=args.high
    )

    save_dataset_to_csv(dataset, args.output)


if __name__ == "__main__":
    main()
