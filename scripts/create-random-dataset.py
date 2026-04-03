import pandas as pd
import numpy as np

from datetime import datetime


def main():
    num_features = int(input("Enter the number of features: "))
    num_rows = int(input("Enter the number of rows: "))

    columns = ["target"] + [f"feature{i}" for i in range(1, num_features + 1)]
    df = pd.DataFrame(columns=columns)

    for col in columns:
        df[col] = pd.Series(np.random.rand(num_rows))

    df.to_csv(
        f"examples/{datetime.now().timestamp()}_random_dataset".replace(".", "_") + ".csv", index=False)


main()
