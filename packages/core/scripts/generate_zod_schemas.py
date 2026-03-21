import subprocess
import sys
import os
import inspect
import importlib
import enum

from pathlib import Path
from typing import Any, get_args, get_origin, Union, Set, Dict

import pydantic
from pydantic_core import PydanticUndefined

# Add packages/core to path
scripts_dir = Path(__file__).resolve().parent
core_package_dir = scripts_dir.parent
sys.path.insert(0, str(core_package_dir))

try:
    from core.features.base import RootDomainModel
except ImportError as e:
    print(f"Error importing base models: {e}")
    sys.exit(1)

IGNORED_BASES = {'RootDomainModel', 'BaseMutableDomainModel',
                 'BaseImmutableDomainModel', 'BaseImmutableVersionedDomainModel'}


def get_all_modules(package_name="core.models"):
    models_dir = core_package_dir / "core" / "models"
    modules = []

    try:
        modules.append(importlib.import_module(package_name))
    except ImportError:
        pass

    for py_file in models_dir.rglob("*.py"):
        if py_file.name == "__init__.py" and py_file.parent == models_dir:
            continue

        rel_path = py_file.relative_to(core_package_dir)
        module_path = str(rel_path.with_suffix("")).replace(os.sep, ".")

        try:
            modules.append(importlib.import_module(module_path))
        except Exception as e:
            print(f"Skipping module {module_path}: {e}")

    return modules


def find_model_by_name(model_name: str) -> type[pydantic.BaseModel] | type[enum.Enum] | None:
    modules = get_all_modules()
    for module in modules:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, RootDomainModel) and obj.__name__ not in IGNORED_BASES:
                if obj.__name__ == model_name:
                    return obj
            elif issubclass(obj, enum.Enum):
                if obj.__name__ == model_name:
                    return obj
    return None


def is_optional_type(annotation: Any) -> tuple[bool, Any]:
    origin = get_origin(annotation)
    if origin is Union or str(origin) == "typing.Union" or type(annotation) is type(int | str):
        args = get_args(annotation)
        NoneType = type(None)
        if NoneType in args:
            non_none_args = tuple(a for a in args if a is not NoneType)
            if len(non_none_args) == 1:
                return True, non_none_args[0]
            else:
                return True, Union[non_none_args]
    return False, annotation


def get_dependencies_from_annotation(annotation: Any) -> Set[type[pydantic.BaseModel]]:
    dependencies = set()
    _, base_type = is_optional_type(annotation)
    origin = get_origin(base_type)
    args = get_args(base_type)

    if origin is list or origin is dict or getattr(base_type, '__name__', '') in ('list', 'dict'):
        for arg in args:
            dependencies.update(get_dependencies_from_annotation(arg))
    elif inspect.isclass(base_type):
        if issubclass(base_type, pydantic.BaseModel):
            if base_type.__name__ not in IGNORED_BASES:
                dependencies.add(base_type)
        elif issubclass(base_type, enum.Enum):
            dependencies.add(base_type)

    return dependencies


def walk_dependencies(model: Any, collected: Set[Any]):
    if model in collected or getattr(model, '__name__', '') in IGNORED_BASES:
        return

    collected.add(model)

    if issubclass(model, pydantic.BaseModel):
        for field_info in model.model_fields.values():
            deps = get_dependencies_from_annotation(field_info.annotation)
            for dep in deps:
                walk_dependencies(dep, collected)


def to_camel_case(s: str) -> str:
    parts = s.split('_') if '_' in s else [s]
    if len(parts) == 1:
        # Pydantic classes are PascalCase, so we just lowercase the first letter
        return s[0].lower() + s[1:]
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])


def map_type_to_zod(annotation: Any, required: bool, deps_collected: Set[str], field_name: str) -> str:
    is_optional, base_type = is_optional_type(annotation)

    # Base model fields are implicitly required because they are always present, even if they have default factories.
    ALWAYS_REQUIRED_FIELDS = {'id', 'created_at',
                              'updated_at', 'timestamp', 'version', 'is_latest'}
    if field_name in ALWAYS_REQUIRED_FIELDS:
        required = True
        is_optional = False

    origin = get_origin(base_type)
    args = get_args(base_type)

    type_name = getattr(base_type, '__name__', str(base_type))
    base_str = str(base_type).lower()
    annotation_str = str(annotation).lower()

    zod_type = "z.any()"
    modifiers = []

    if origin is list or type_name == 'list':
        if args:
            inner_type = map_type_to_zod(
                args[0], required=True, deps_collected=deps_collected, field_name=field_name)
            zod_type = f"z.array({inner_type})"
        else:
            zod_type = "z.array(z.any())"
    elif origin is dict or type_name == 'dict':
        zod_type = "z.record(z.string(), z.any())"
    elif 'emailstr' in annotation_str:
        zod_type = "z.email()"
    elif 'secretstr' in annotation_str:
        zod_type = "z.string()"
    elif 'uuid' in annotation_str:
        zod_type = "z.uuid()"
    elif 'str' in type_name.lower():
        zod_type = "z.string()"
    elif 'int' in type_name.lower():
        zod_type = "z.number().int()"
    elif 'float' in type_name.lower():
        zod_type = "z.number()"
    elif 'bool' in type_name.lower():
        zod_type = "z.boolean()"
    elif 'datetime' in type_name.lower() or 'datetime' in base_str:
        zod_type = "z.iso.datetime()"
    elif inspect.isclass(base_type):
        if issubclass(base_type, pydantic.BaseModel):
            deps_collected.add(base_type.__name__)
            zod_type = f"{to_camel_case(base_type.__name__)}Schema"
        elif issubclass(base_type, enum.Enum):
            deps_collected.add(base_type.__name__)
            zod_type = f"{to_camel_case(base_type.__name__)}Schema"

    if is_optional or not required:
        modifiers.append("nullable()")
        modifiers.append("optional()")

    if modifiers:
        return f"{zod_type}.{'.'.join(modifiers)}"
    return zod_type


def to_kebab_case(s: str) -> str:
    import re
    s = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s).lower()


def generate(target_model_name: str | None = None):
    collected_models: Set[Any] = set()

    if target_model_name:
        root_model = find_model_by_name(target_model_name)
        if not root_model:
            print(f"Error: Model '{target_model_name}' not found.")
            sys.exit(1)

        walk_dependencies(root_model, collected_models)
        print(
            f"Discovered {len(collected_models)} models in the dependency tree for '{target_model_name}':")
    else:
        modules = get_all_modules()
        for module in modules:
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, RootDomainModel) and obj.__name__ not in IGNORED_BASES:
                    walk_dependencies(obj, collected_models)
        print(
            f"Discovered {len(collected_models)} models across all domain objects:")

    for m in collected_models:
        print(f" - {m.__name__}")

    frontend_dir = scripts_dir.parent.parent / \
        "frontend" / "app" / "schemas" / "generated"
    frontend_dir.mkdir(parents=True, exist_ok=True)

    for model in collected_models:
        file_name = f"{to_kebab_case(model.__name__)}.schema.ts"
        out_path = frontend_dir / file_name

        is_enum = issubclass(model, enum.Enum)
        deps_collected = set()
        fields_ts = []

        if not is_enum:
            for field_name, field_info in model.model_fields.items():
                required = field_info.is_required()
                zod_type_str = map_type_to_zod(
                    field_info.annotation, required=required, deps_collected=deps_collected, field_name=field_name)
                fields_ts.append(f"  {field_name}: {zod_type_str},")

        # Write to file
        with open(out_path, 'w') as f:
            f.write('import { z } from "zod";\n')

            # Write imports for dependencies
            for dep in deps_collected:
                if dep != model.__name__:  # avoid self-import in case of direct cyclic link
                    dep_file = f"{to_kebab_case(dep)}.schema"
                    dep_schema_name = f"{to_camel_case(dep)}Schema"
                    f.write(
                        f'import {{ {dep_schema_name} }} from "./{dep_file}";\n')

            f.write('\n')

            camel_model_name = to_camel_case(model.__name__)

            if is_enum:
                enum_values = [f'"{e.value}"' for e in model]
                f.write(
                    f'export const {camel_model_name}Values = [{", ".join(enum_values)}] as const;\n')
                f.write(
                    f'export const {camel_model_name}Schema = z.enum({camel_model_name}Values);\n\n')
            else:
                f.write(
                    f'export const {camel_model_name}Schema = z.object({{\n')
                f.write('\n'.join(fields_ts))
                f.write('\n});\n\n')

            f.write(
                f'export type {model.__name__} = z.infer<typeof {camel_model_name}Schema>;\n')

        print(f"Generated {file_name}")

    run_biome(scripts_dir.parent.parent / "frontend")


def run_biome(frontend_dir: Path):
    print("\nRunning Biome JS linting and fixing...")
    try:
        subprocess.run(
            ["npx", "@biomejs/biome", "check", "--write", "app/schemas/generated"],
            cwd=frontend_dir,
            check=True
        )
        print("Biome JS successfully formatted the schemas.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Biome JS formatting failed with code {e.returncode}")
    except FileNotFoundError:
        print("Warning: npx or '@biomejs/biome' not found. Skipping formatting.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate Zod schemas from Pydantic domain models.")
    parser.add_argument("model_name", nargs="?", default=None,
                        help="Specific model name to generate (e.g. Dataset)")
    parser.add_argument(
        "--file", help="Path to a specific python file to generate schemas for models defined within it")

    args = parser.parse_args()

    if args.file:
        file_path = Path(args.file).resolve()
        print(f"Parsing file for models: {file_path}")
        try:
            rel_path = file_path.relative_to(core_package_dir)
            module_path = str(rel_path.with_suffix("")).replace(os.sep, ".")
            module = importlib.import_module(module_path)

            # Find classes in this exact module
            models_found = False
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure the class is defined in this module and not just imported
                if obj.__module__ == module_path:
                    if (issubclass(obj, RootDomainModel) and obj.__name__ not in IGNORED_BASES) or issubclass(obj, enum.Enum):
                        models_found = True
                        print(
                            f"Found model/enum '{obj.__name__}' in file, generating schemas...")
                        generate(obj.__name__)

            if not models_found:
                print("No valid BaseModels or Enums found in the provided file.")

        except ValueError:
            print(
                f"Error: The file {args.file} is not inside the core package directory.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading module from file: {e}")
            sys.exit(1)
    elif args.model_name:
        generate(args.model_name)
    else:
        generate()
