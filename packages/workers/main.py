import sys


def main():
    worker_type = sys.argv[1] if len(sys.argv) > 1 else None

    if not worker_type:
        print("Please specify a worker type (e.g., 'dataset', 'training')")
        exit(1)

    print(f"Starting worker of type: {worker_type}")


if __name__ == "__main__":
    main()
