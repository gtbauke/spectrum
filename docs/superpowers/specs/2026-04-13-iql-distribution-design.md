# IQL Pattern Distribution Analysis Design

## Goal
Add pattern distribution analysis capabilities to the Inference Query Language (IQL), allowing users to find common sub-expressions within a set of models.

## Background
The `rEGGression` library already supports a `distribution` method that extracts common patterns from an e-graph. This design exposes that functionality through the IQL interface.

## Proposed Syntax
The `SELECT` clause as been extended to support a `DISTRIBUTION` mode:

```sql
SELECT [TOP <sample_size>] DISTRIBUTION pattern, frequency
FROM models/<run_id>
[WHERE <pattern_filters>]
[AT LEAST <min_frequency>]
[LIMIT <max_patterns>]
```

### Parameters Mapping
- **`TOP <N>`**: Maps to `fromTop`. Sets the number of models to sample from the e-graph (sorted by the `ORDER BY` criteria, default: fitness).
- **`DISTRIBUTION`**: Mode flag. Changes the execution context from model selection to pattern extraction.
- **`pattern, frequency`**: Restricted columns for distribution mode.
- **`WHERE <conditions>`**: Maps to `filters`. Filters the extracted patterns (e.g., `size < 10`).
- **`AT LEAST <N>`**: Maps to `atLeast`. The minimum number of occurrences for a pattern to be returned.
- **`LIMIT <N>`**: Maps to `limitedAt`. The maximum number of patterns to return in the result set.

## Architectural Changes

### 1. Tokenizer (`iql.tokenizer`)
- Add `DISTRIBUTION`, `AT`, `LEAST`, and `LIMIT` to `TokenKind`.
- Update keyword matching in `TokenKind.keyword_or_identifier`.

### 2. AST (`iql.parser.ast`)
- Update `SelectClauseAstNode` to include:
    - `is_distribution: bool`
    - `at_least: Optional[IntegerLiteralAstNode]`
    - `limit: Optional[IntegerLiteralAstNode]`
- Create `AtLeastAstNode` and `LimitAstNode` if needed for structural clarity, or integrate directly into the select node.

### 3. Parser (`iql.parser.parselets`)
- Update `SelectClauseParselet` to:
    - Recognize the `DISTRIBUTION` keyword.
    - Parse `pattern, frequency` as required identifiers when in distribution mode.
    - Parse optional `AT LEAST <N>` clause.
    - Parse optional `LIMIT <N>` clause.

### 4. Executor (`iql.executor`)
- Update `QueryExecutor.execute` to:
    - Detect the distribution mode.
    - Extract and validate parameters (`sample_size`, `at_least`, `limit`, `filters`).
    - Call `self._active_reggression.distribution(...)`.
    - Transform the resulting DataFrame into `InferenceResult` objects with `expression` (aliased to pattern) and `frequency`.

## Performance Considerations
Pattern distribution analysis can be computationally expensive on large e-graphs. The use of `TOP <N>` (fromTop) and `AT LEAST <N>` is critical for maintaining responsive query times.

## Verification Plan
1. **Unit Tests**: Add tests to `packages/inference_query_language/tests` covering the new grammar and parser logic.
2. **Integration Tests**: Update `packages/workers/tests/verify_inference_pipeline.py` to include a distribution query case and verify broker events are triggered correctly with the new result schema.
