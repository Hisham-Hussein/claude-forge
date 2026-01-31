<overview>
Tools bridge agents (non-deterministic) and execution (deterministic). Good tool design is critical for reliable LLM applications.
</overview>

<principle name="single_responsibility">
<title>Single Responsibility</title>

One tool = one action. Don't combine unrelated operations.

<bad_example>
```python
# BAD: Tool does too much
def process_user(user_id: str, action: str) -> str:
    if action == "get": ...
    elif action == "update": ...
    elif action == "delete": ...
```
</bad_example>

<good_example>
```python
# GOOD: Separate tools
def get_user(user_id: str) -> dict: ...
def update_user(user_id: str, data: dict) -> dict: ...
def delete_user(user_id: str) -> bool: ...
```
</good_example>
</principle>

<principle name="clear_contracts">
<title>Clear Contracts</title>

Explicit input/output schemas. The agent should know exactly what it's getting.

<bad_example>
```python
# BAD: Ambiguous
def search(query): ...  # Returns... what?
```
</bad_example>

<good_example>
```python
# GOOD: Clear contract
def search_documents(
    query: str,
    max_results: int = 10,
    include_metadata: bool = False
) -> list[dict]:
    """
    Search documents by query.

    Args:
        query: Search terms
        max_results: Maximum results to return (1-100)
        include_metadata: Include document metadata in results

    Returns:
        List of {id, title, snippet, score, metadata?}
    """
```
</good_example>
</principle>

<principle name="fail_fast">
<title>Fail Fast</title>

Validate inputs before doing work. Don't let the agent waste tokens on doomed operations.

<example>
```python
def send_email(to: str, subject: str, body: str) -> dict:
    # Validate BEFORE doing anything
    if not is_valid_email(to):
        return {"error": "Invalid email format", "field": "to"}
    if not subject.strip():
        return {"error": "Subject cannot be empty", "field": "subject"}

    # Now proceed with sending
    ...
```
</example>
</principle>

<principle name="idempotency">
<title>Idempotency</title>

Same input should produce same result. Agents may retry on transient failures.

<bad_example>
```python
# BAD: Creates duplicate on retry
def create_user(email: str) -> dict:
    return db.insert({"email": email})
```
</bad_example>

<good_example>
```python
# GOOD: Idempotent
def create_user(email: str) -> dict:
    existing = db.find_one({"email": email})
    if existing:
        return {"user": existing, "created": False}
    new_user = db.insert({"email": email})
    return {"user": new_user, "created": True}
```
</good_example>
</principle>

<principle name="actionable_errors">
<title>Actionable Errors</title>

When tools fail, tell the agent what went wrong AND what to do about it.

<bad_example>
```python
# BAD: Cryptic
return {"error": "API_ERROR_500"}
```
</bad_example>

<good_example>
```python
# GOOD: Actionable
return {
    "error": "Rate limit exceeded",
    "retry_after": 60,
    "suggestion": "Wait 60 seconds before retrying, or use batch endpoint"
}
```
</good_example>
</principle>

<checklist>
**Tool Design Checklist:**

- [ ] Does one thing well (single responsibility)
- [ ] Input parameters are typed and documented
- [ ] Output schema is explicit and consistent
- [ ] Validates inputs before executing
- [ ] Returns actionable errors
- [ ] Idempotent where possible
</checklist>

<template>
**Tool Template:**

```python
def tool_name(
    required_param: str,
    optional_param: int = 10
) -> dict:
    """
    One-line description of what this tool does.

    Args:
        required_param: Description of parameter
        optional_param: Description with default behavior

    Returns:
        {
            "result": "...",
            "metadata": {...}
        }

    Errors:
        {
            "error": "Description of what went wrong",
            "suggestion": "How to fix or work around"
        }
    """
    # 1. Validate inputs
    if not required_param:
        return {"error": "required_param cannot be empty", "suggestion": "Provide a value"}

    # 2. Execute operation
    result = do_the_thing(required_param, optional_param)

    # 3. Return structured result
    return {"result": result, "metadata": {"param_used": optional_param}}
```
</template>
