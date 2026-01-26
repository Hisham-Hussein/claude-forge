<overview>
Agents fail differently than traditional software. Plan for errors, prevent loops, and add safety guardrails.
</overview>

<error_handling>
<error_categories>
| Error Type | Example | Response |
|------------|---------|----------|
| Tool failure | API timeout | Retry with backoff |
| Invalid tool call | Wrong parameters | Reprompt agent |
| Agent loop | Same action repeatedly | Max iterations, break |
| Context overflow | Too many tokens | Summarize, truncate |
| Rate limit | API quota exceeded | Wait, use fallback |
</error_categories>

<graceful_degradation>
When a tool fails, the agent should have options:

1. **Retry:** Transient error, try again
2. **Fallback tool:** Use alternative data source
3. **Partial result:** Return what succeeded
4. **Escalate:** Ask user for help or hand off to human
</graceful_degradation>

<loop_prevention>
Agents can get stuck. Prevent infinite loops:

```python
MAX_ITERATIONS = 10

for i in range(MAX_ITERATIONS):
    action = agent.decide()
    if action.type == "finish":
        break
    result = execute_tool(action)
    agent.observe(result)
else:
    # Max iterations reached
    log_failure("Agent loop detected", context={"last_action": action})
    return {"error": "Agent exceeded max iterations", "partial_result": ...}
```
</loop_prevention>

<retry_pattern>
```python
from time import sleep

def with_retry(fn, max_attempts=3, backoff=2):
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError as e:
            if attempt == max_attempts - 1:
                raise
            sleep(backoff ** attempt)
```
</retry_pattern>
</error_handling>

<safety_guardrails>
<input_validation>
Validate before the agent acts:

```python
def validate_agent_input(user_message: str) -> tuple[bool, str]:
    # Check for injection attempts
    if contains_prompt_injection(user_message):
        return False, "Invalid input detected"

    # Check for PII that shouldn't be processed
    if contains_sensitive_pii(user_message):
        return False, "Please don't include sensitive information"

    return True, ""
```
</input_validation>

<output_filtering>
Check agent outputs before returning to user:

```python
def filter_output(response: str) -> str:
    # Remove any leaked system prompts
    response = remove_system_prompt_leaks(response)

    # Check for harmful content
    if is_harmful(response):
        return "I can't help with that request."

    # Redact any PII in response
    response = redact_pii(response)

    return response
```
</output_filtering>

<scope_limiting>
Limit what tools the agent can access:

| Principle | Implementation |
|-----------|----------------|
| Least privilege | Only give tools needed for task |
| Read vs write | Separate read-only from mutation tools |
| Rate limiting | Cap tool calls per session |
| Audit logging | Log all tool invocations |
</scope_limiting>

<human_in_the_loop>
When to require human approval:

| Action Type | Approval Required |
|-------------|-------------------|
| Read data | No |
| Update user's own data | No |
| Delete data | Yes |
| External communication | Yes (send email, post) |
| Financial transactions | Yes |
| System configuration | Yes |
</human_in_the_loop>
</safety_guardrails>

<checklist>
**Reliability Checklist:**

- [ ] Tool failures have retry logic
- [ ] Invalid tool calls trigger reprompt
- [ ] Agent loop has max iteration limit
- [ ] Context overflow handled (summarize/truncate)
- [ ] Rate limits handled (wait/fallback)

**Safety Checklist:**

- [ ] Input validation for injection/PII
- [ ] Output filtering for harmful content
- [ ] Least privilege tool access
- [ ] Human-in-the-loop for destructive actions
- [ ] Audit logging enabled
</checklist>
