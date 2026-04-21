# IQL Extensibility and Compiler Pattern Refactoring Design 

## Abstract
Refactor the Inference Query Language (IQL) package to use a Compiler/Phased Execution Architecture. The goal is to easily support new `reggression` functions, select clause aliasing, arbitrary plotting commands, and mutation commands (e.g. `optimize()`).

## 1. Architectural Phases

The current monolithic `QueryExecutor` will be split into three discrete phases:

### Phase 1: Syntax Parsing (AST)
- Keep the current Pratt parser structure (`Parser` -> `BaseAstNode`).
- **Changes**: Add an `AsParselet` to generate `AliasAstNode(alias: Identifier, value: Expression)`. Replace ad-hoc tokens like `predict` logic with a generic `FunctionCallAstNode` supporting any identifier as a function name.

### Phase 2: Semantic Analysis (Logical Plan)
- **New Component**: The `QueryAnalyzer` receives an `AST` and outputs a strongly-typed `LogicalPlan`.
- Ensures constraints using a `FunctionRegistry` (validating that `predict`, `countPattern`, or `plot` exist and receive correct types/arities).
- Resolves aliases to ensure there are no collisions.
- Preserves `Span` locations to accurately report `SemanticError` locations to the UI (e.g., "Unknown function `plotZ` at Line 1, Col 4").

### Phase 3: Physical Execution
- **New Component**: Execution handlers (e.g., `SelectExecutor`).
- Executes the verified `LogicalPlan` directly against the `Reggression` object.
- Blind to IQL's text syntax. Purely executes logic and formats payload.

## 2. CommandResult and Output Models

Given that IQL is extending beyond tabular queries (simulations, plots, e-graph permutations), the execution and database layer must adapt to store varying types of outputs.

### Executor Payload
The Executor will output a Polymorphic `CommandResult` object instead of forcing everything into a DataFrame.
```python
class CommandResult(BaseModel):
    kind: Literal["TABULAR", "PLOT", "MUTATION"]
    # Payload format depends on the kind (e.g., list of rows, plotting metadata, success messages)
```

### Database Schema Updates
To save all types of results from IQL, the `InferenceRun` (or associated entities) must adapt:
- **Tabular Data:** Continue inserting tabular output into the `InferenceResult` (or heavily adapt it) to store multiple predictions (perhaps utilizing `JSONB` columns for variable lists of user-defined metrics/functions).
- **Plot and Artifacts:** To handle plots or large outputs from `IQL`, the database schema for `InferenceRun` needs a `JSONB` payload column (e.g., `execution_metadata` or `outputs_json`), or we must upload the generated plot to `FileStorage` and store the `S3 URL/Local Path` in the `InferenceRun` record.
- **Dynamic Columns:** Ensure `InferenceResult`'s schema (specifically the backend `prediction` fields) are no longer strictly singular. Since we can have `predict(test) as ptest, predict(train) as ptrain`, the result payloads need a JSONB map like `predictions: {"ptest": [...], "ptrain": [...]}` instead of a strict 1D array.

## 3. Data Flow Example

`SELECT predict(test_data) AS test_pred, countPattern() FROM my_model`

1. **Parser:** Builds `AST` containing a `SelectClause` identifying two columns.
2. **Analyzer:** Validates `predict` vs `FunctionRegistry`. Sees `countPattern` mapping directly to `reggression.countPattern`. Returns a `LogicalSelectPlan(columns=[Alias(test_pred), Alias(countPattern_1)])`.
3. **Execution:** The Engine pulls the dataset, runs `predict(test_data)`, fetches `countPattern`, stitches them together mapped under the respective aliases, and returns a `CommandResult(kind=TABULAR, payload=rows)`.
4. **Persistence:** The `Worker` writes tabular schema. If it generated a plot, it persists standard tabular metrics and attaches plot artifacts to File Storage.
