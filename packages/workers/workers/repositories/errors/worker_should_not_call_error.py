class WorkerShouldNotCallMethodError(Exception):
    def __init__(self, method_name: str):
        super().__init__(f"Worker should not call method '{method_name}'")
