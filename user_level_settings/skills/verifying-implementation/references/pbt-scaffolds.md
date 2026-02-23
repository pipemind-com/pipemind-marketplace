# Property-Based Testing Scaffolds

Ready-made scaffold templates for the `/verifying-implementation` skill. Use as a deterministic starting point — adapt imports, strategies, and assertions to the function-under-test.

## Python (hypothesis)

```python
import hypothesis
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Import the function-under-test
from module import function_under_test

# Define custom strategies for domain types
# domain_strategy = st.builds(DomainType, field=st.integers(min_value=0))

@settings(max_examples=200, deadline=None)
@given(
    # Choose strategies matching the function signature:
    # st.integers(), st.floats(allow_nan=False), st.text(),
    # st.lists(st.integers(), min_size=0, max_size=100),
    # st.dictionaries(st.text(min_size=1), st.integers()),
    x=st.integers(),
)
def test_property_name(x):
    """Property: describe the invariant being tested."""
    result = function_under_test(x)

    # Assert invariants — properties that must ALWAYS hold:
    # assert len(result) == len(input)       # length preservation
    # assert result == sorted(result)         # ordering
    # assert sum(result) == 0                 # conservation
    # assert isinstance(result, expected_type) # type stability
    assert result is not None


if __name__ == "__main__":
    test_property_name()
    print("All property tests passed.")
```

## JavaScript / TypeScript (fast-check)

```javascript
const fc = require("fast-check");

// Import the function-under-test
// const { functionUnderTest } = require('./module');

// Define custom arbitraries for domain types
// const domainArb = fc.record({ field: fc.integer({ min: 0 }) });

describe("functionUnderTest properties", () => {
  it("property: describe the invariant being tested", () => {
    fc.assert(
      fc.property(
        // Choose arbitraries matching the function signature:
        // fc.integer(), fc.float(), fc.string(),
        // fc.array(fc.integer(), { minLength: 0, maxLength: 100 }),
        // fc.dictionary(fc.string(), fc.integer()),
        fc.integer(),
        (x) => {
          const result = functionUnderTest(x);

          // Assert invariants — properties that must ALWAYS hold:
          // expect(result).toHaveLength(input.length);  // length preservation
          // expect(result).toEqual([...result].sort()); // ordering
          // expect(result.reduce((a, b) => a + b, 0)).toBe(0); // conservation
          expect(result).toBeDefined();
        }
      ),
      { numRuns: 200 }
    );
  });
});
```

## Rust (proptest)

```rust
use proptest::prelude::*;

// Import the function-under-test
// use crate::module::function_under_test;

// Define custom strategies for domain types
// fn domain_strategy() -> impl Strategy<Value = DomainType> {
//     (0..100i32).prop_map(|v| DomainType::new(v))
// }

proptest! {
    #![proptest_config(ProptestConfig::with_cases(200))]

    #[test]
    fn test_property_name(
        // Choose strategies matching the function signature:
        // x in any::<i32>(),
        // s in "\\PC*",  // arbitrary strings
        // v in prop::collection::vec(any::<i32>(), 0..100),
        x in any::<i32>(),
    ) {
        let result = function_under_test(x);

        // Assert invariants — properties that must ALWAYS hold:
        // prop_assert_eq!(result.len(), input.len());  // length preservation
        // prop_assert!(result.windows(2).all(|w| w[0] <= w[1])); // ordering
        // prop_assert_eq!(result.iter().sum::<i32>(), 0); // conservation
        prop_assert!(result.is_some());
    }
}
```

## Common Invariant Patterns

When analyzing the function-under-test, look for these property categories:

- **Round-trip**: `decode(encode(x)) == x` — serialization, parsing, compression
- **Idempotence**: `f(f(x)) == f(x)` — formatting, normalization, deduplication
- **Monotonicity**: `x <= y => f(x) <= f(y)` — sorting, ranking, pricing
- **Conservation**: `sum(output) == sum(input)` — financial transactions, splitting
- **Invariant preservation**: `valid(x) => valid(f(x))` — state machines, type transformations
- **Commutativity**: `f(a, b) == f(b, a)` — merging, set operations
- **No crash**: function doesn't throw/panic on any valid input — robustness baseline
