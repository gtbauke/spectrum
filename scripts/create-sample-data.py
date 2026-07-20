import argparse
import numpy as np
import pandas as pd
import os


def generate_gravity_data(num_samples: int, noise_level: float, output_file: str):
    """
    Generates noisy data for Newton's Law of Gravitation: F = G * (m1 * m2) / r^2
    """
    np.random.seed(42)

    # Generate random inputs
    m1 = np.random.uniform(1, 10, num_samples)
    m2 = np.random.uniform(1, 10, num_samples)
    r = np.random.uniform(1, 5, num_samples)

    # Calculate Ground Truth
    force = (m1 * m2) / (r**2)

    # Add Gaussian Noise (relative to signal magnitude)
    noise = np.random.normal(0, noise_level, num_samples) * force
    force_noisy = force + noise

    # Create DataFrame
    df = pd.DataFrame({
        'm1': m1,
        'm2': m2,
        'r': r,
        'force': force_noisy
    })

    # Save to file
    df.to_csv(output_file, index=False)
    print(
        f"Successfully generated {num_samples} samples with noise level {noise_level} into '{output_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic gravity dataset for symbolic regression.")
    parser.add_argument("--samples", type=int, default=200,
                        help="Number of data points to generate")
    parser.add_argument("--noise", type=float, default=0.05,
                        help="Noise level as a fraction of signal (e.g., 0.05 = 5%)")
    parser.add_argument("--output", type=str,
                        default="gravity_data.csv", help="Output CSV filename")

    args = parser.parse_args()

    generate_gravity_data(args.samples, args.noise, args.output)
