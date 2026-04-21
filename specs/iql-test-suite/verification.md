# Verification Plan: IQL Test Suite

## 1. Automated Tests
The main verification method will be running the newly created test suite.

### Backend (Pytest)
```bash
# Run all IQL tests
pytest packages/inference_query_language/tests -v

# Run only tokenizer tests
pytest packages/inference_query_language/tests/tokenizer -v

# Run fuzzing tests (might take longer)
pytest packages/inference_query_language/tests/fuzzing -v
```

### Coverage Report
```bash
pytest packages/inference_query_language/tests --cov=iql --cov-report=term-missing
```

## 2. Code Snippets for Testing

### Example Tokenizer Test
```python
def test_tokenizer_handles_unclosed_string():
    query = 'SELECT * FROM "unclosed_model'
    tokenizer = QueryTokenizer(query)
    with pytest.raises(IqlTokenizationError):
        tokenizer.tokenize()
```

### Example Executor Test
```python
def test_executor_executes_top_n(mock_compiler, mock_reggressions):
    query = "SELECT * FROM my_model SEARCH TOP 5"
    result = mock_compiler.compile(query, ["my_model"])
    executor = QueryExecutor(result.plan, mock_reggressions)
    output = executor.execute()
    assert len(output.results) == 5
```

## 3. Manual Checklist
- [ ] Verify that `pytest` is installed in the `uv` environment.
- [ ] Ensure that errors in the `Analyzer` (e.g., model not found) produce a `CompilerResult` with `is_success = False`.
- [ ] check that `PREDICT` function correctly appends a `prediction` column to the output dataframe.
