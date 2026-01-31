#!/bin/bash
#
# Run mutation testing with mutmut for characterization verification.
# Used in the VERIFY phase of characterization-first workflow.
#
# Usage:
#   ./run_mutation.sh <target_file.py> <test_file.py>
#
# Example:
#   ./run_mutation.sh execution/utils/validation.py tests/characterization/test_validation_char.py
#
# Requirements:
#   - mutmut installed (pip install mutmut)
#   - pytest installed
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <target_file.py> <test_file.py>"
    echo ""
    echo "Example:"
    echo "  $0 execution/utils/validation.py tests/characterization/test_validation_char.py"
    exit 1
fi

TARGET_FILE="$1"
TEST_FILE="$2"

# Validate files exist
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}Error: Target file not found: $TARGET_FILE${NC}"
    exit 1
fi

if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}Error: Test file not found: $TEST_FILE${NC}"
    exit 1
fi

# Check mutmut is installed
if ! command -v mutmut &> /dev/null; then
    echo -e "${YELLOW}mutmut not found. Installing...${NC}"
    pip install mutmut
fi

# Check pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest not found. Install with: pip install pytest${NC}"
    exit 1
fi

echo ""
echo "============================================================"
echo "  MUTATION TESTING: Characterization Coverage Verification"
echo "============================================================"
echo ""
echo "Target: $TARGET_FILE"
echo "Tests:  $TEST_FILE"
echo ""

# First, verify tests pass without mutations
echo -e "${YELLOW}Step 1: Verifying tests pass without mutations...${NC}"
if ! pytest "$TEST_FILE" -v --tb=short; then
    echo ""
    echo -e "${RED}ERROR: Tests fail without mutations!${NC}"
    echo "Fix failing tests before running mutation testing."
    exit 1
fi

echo ""
echo -e "${GREEN}Tests pass. Proceeding with mutation testing...${NC}"
echo ""

# Clear any previous mutation cache for this target
echo -e "${YELLOW}Step 2: Clearing previous mutation cache...${NC}"
rm -rf .mutmut-cache 2>/dev/null || true

# Run mutation testing
echo -e "${YELLOW}Step 3: Running mutation testing (this may take a while)...${NC}"
echo ""

mutmut run \
    --paths-to-mutate="$TARGET_FILE" \
    --tests-dir="$(dirname "$TEST_FILE")" \
    --runner="pytest -x $TEST_FILE --tb=no -q" \
    2>&1 | tee /tmp/mutmut_output.txt

echo ""
echo "============================================================"
echo "  MUTATION TESTING RESULTS"
echo "============================================================"
echo ""

# Show results summary
mutmut results

# Calculate mutation score
TOTAL=$(mutmut results 2>/dev/null | grep -E "^[0-9]+" | wc -l || echo "0")
KILLED=$(mutmut results 2>/dev/null | grep -E "killed" | wc -l || echo "0")
SURVIVED=$(mutmut results 2>/dev/null | grep -E "survived" | wc -l || echo "0")
TIMEOUT=$(mutmut results 2>/dev/null | grep -E "timeout" | wc -l || echo "0")

echo ""
echo "Summary:"
echo "  Total mutants:  $TOTAL"
echo "  Killed:         $KILLED"
echo "  Survived:       $SURVIVED"
echo "  Timeout:        $TIMEOUT"

if [ "$TOTAL" -gt 0 ]; then
    SCORE=$((KILLED * 100 / TOTAL))
    echo "  Mutation score: ${SCORE}%"
    echo ""

    if [ "$SCORE" -ge 90 ]; then
        echo -e "${GREEN}HIGH confidence - Safe to refactor${NC}"
    elif [ "$SCORE" -ge 70 ]; then
        echo -e "${YELLOW}MEDIUM confidence - Review survivors before refactoring${NC}"
    else
        echo -e "${RED}LOW confidence - More characterization tests needed${NC}"
    fi
fi

# If there are survivors, show them
if [ "$SURVIVED" -gt 0 ]; then
    echo ""
    echo "============================================================"
    echo "  SURVIVING MUTANTS (need investigation)"
    echo "============================================================"
    echo ""
    echo "Run 'mutmut show <id>' to see each surviving mutant."
    echo "For each survivor, decide:"
    echo "  - Missing test: Write a test to kill it"
    echo "  - Equivalent mutant: Document and accept"
    echo "  - Dead code: Consider removal in refactor"
    echo ""

    # Show first few survivors
    mutmut results 2>/dev/null | grep -E "survived" | head -10
fi

echo ""
echo "============================================================"
echo "  NEXT STEPS"
echo "============================================================"
echo ""
if [ "$SURVIVED" -gt 0 ]; then
    echo "1. Run: mutmut show <id>  for each surviving mutant"
    echo "2. Add tests to kill non-equivalent mutants"
    echo "3. Re-run this script until mutation score is acceptable"
    echo "4. Document any accepted equivalent mutants"
else
    echo "All mutants killed! Characterization is complete."
    echo "You may now proceed to refactoring."
fi
echo ""
