<overview>
A seam is a place where you can alter behavior without editing the code under test. Finding seams is essential for writing isolated characterization tests.
</overview>

<why_seams_matter>
Legacy code often has:
- Hard-coded dependencies (direct API calls, file paths)
- Global state
- Tightly coupled components

Without seams, you can't test in isolation. You'd need real databases, real APIs, real file systems - making tests slow, flaky, and incomplete.
</why_seams_matter>

<seam_types>

<seam name="object_seam">
**Object Seam**: Replace an object with a test double

```python
# Production code
class OrderProcessor:
    def __init__(self, payment_gateway):  # <-- SEAM
        self.gateway = payment_gateway

# Test code
class FakeGateway:
    def charge(self, amount):
        return {"status": "success", "id": "fake-123"}

def test_order_processing():
    processor = OrderProcessor(FakeGateway())  # Inject fake
    result = processor.process(order)
    assert result["payment_id"] == "fake-123"
```

**How to find:** Look for `__init__` parameters, class attributes set at construction
</seam>

<seam name="link_seam">
**Link Seam**: Replace at import/link time

```python
# Production code
import requests

def fetch_data(url):
    return requests.get(url).json()  # <-- SEAM at import

# Test code
def test_fetch_data(mocker):
    mock_get = mocker.patch('module.requests.get')
    mock_get.return_value.json.return_value = {"data": "fake"}

    result = fetch_data("http://example.com")
    assert result == {"data": "fake"}
```

**How to find:** Look for `import` statements, especially for I/O libraries (requests, os, open)
</seam>

<seam name="preprocessor_seam">
**Preprocessor/Config Seam**: Control behavior via configuration

```python
# Production code
import os

DEBUG = os.environ.get("DEBUG", False)  # <-- SEAM

def log_sensitive(data):
    if DEBUG:
        print(f"DEBUG: {data}")
    # In production, never print sensitive data
```

**How to find:** Look for environment variables, config files, feature flags
</seam>

</seam_types>

<common_patterns>

<pattern name="file_io">
**File I/O Seam**

```python
# Hard to test
def process_config():
    with open("/etc/myapp/config.json") as f:  # Hard-coded path
        return json.load(f)

# Better - path as parameter (object seam)
def process_config(config_path="/etc/myapp/config.json"):
    with open(config_path) as f:
        return json.load(f)

# Test
def test_process_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"key": "value"}')
    result = process_config(str(config_file))
    assert result == {"key": "value"}
```
</pattern>

<pattern name="api_calls">
**API Call Seam**

```python
# Hard to test
def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test with link seam
def test_get_user(mocker):
    mocker.patch('module.requests.get').return_value.json.return_value = {
        "id": 123, "name": "Test User"
    }
    result = get_user(123)
    assert result["name"] == "Test User"
```
</pattern>

<pattern name="datetime">
**Time/Date Seam**

```python
# Hard to test
def is_expired(expiry_date):
    return datetime.now() > expiry_date  # Non-deterministic

# Better - inject time source
def is_expired(expiry_date, now=None):
    now = now or datetime.now()
    return now > expiry_date

# Test
def test_is_expired():
    fixed_time = datetime(2024, 1, 15)
    expiry = datetime(2024, 1, 10)
    assert is_expired(expiry, now=fixed_time) == True
```
</pattern>

<pattern name="database">
**Database Seam**

```python
# Hard to test - direct connection
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

# Better - repository pattern (object seam)
class UserRepository:
    def get(self, user_id):
        # Real database logic
        pass

def get_user(user_id, repo=None):
    repo = repo or UserRepository()
    return repo.get(user_id)

# Test
class FakeRepo:
    def get(self, user_id):
        return {"id": user_id, "name": "Fake User"}

def test_get_user():
    result = get_user(123, repo=FakeRepo())
    assert result["name"] == "Fake User"
```
</pattern>

</common_patterns>

<finding_seams_checklist>

When analyzing code for seams, look for:

- [ ] Constructor parameters that accept dependencies
- [ ] Import statements for external libraries
- [ ] Environment variable reads
- [ ] Configuration file reads
- [ ] Direct file I/O operations
- [ ] Network calls (HTTP, database, etc.)
- [ ] System calls (time, random, process)
- [ ] Global variables accessed
- [ ] Singleton patterns

For each found, ask: "Can I replace this with a test double?"

</finding_seams_checklist>

<when_no_seams_exist>

If code has no seams (everything hard-coded):

1. **Characterize at higher level** - Test the whole module with integration tests
2. **Extract seams as part of refactoring** - But characterize first!
3. **Use link seams** - Mock at import level (less clean but works)

The goal is to characterize BEFORE creating seams. Don't refactor to add seams without characterization.

</when_no_seams_exist>
