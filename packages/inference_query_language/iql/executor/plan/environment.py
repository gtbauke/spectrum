from enum import StrEnum


class EntryType(StrEnum):
    VARIABLE = "variable"
    FUNCTION = "function"


class EnvironmentEntry:
    def __init__(self, name: str, value: object, entry_type: EntryType):
        self.name = name
        self.value = value
        self.entry_type = entry_type


class Environment:
    def __init__(self):
        self._variables: dict[str, EnvironmentEntry] = {}

    def set_variable(self, name: str, value: object, entry_type: EntryType = EntryType.VARIABLE):
        self._variables[name] = EnvironmentEntry(name, value, entry_type)

    def get_variable(self, name: str) -> EnvironmentEntry:
        if name not in self._variables:
            raise KeyError(f"Variable '{name}' not found in environment.")

        return self._variables[name]

    def has_variable(self, name: str) -> bool:
        return name in self._variables
