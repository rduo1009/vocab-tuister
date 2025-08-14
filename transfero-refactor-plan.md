# Transfero Refactoring Plan

## 1. My Understanding of the Task

My task is to refactor the inflection logic within the `src/core/transfero` directory. I will modify `_adjective_inflection.py`, `_adverb_inflection.py`, `_noun_inflection.py`, and `_verb_inflection.py`. Each of these files contains its own distinct `_inflect_lemma` helper function that needs to be refactored.

The goal is to change this internal helper function in each file. Its return type will be changed to `tuple[str, ...]`, where the first item in the tuple is the primary or 'main' inflection. The public-facing functions, such as `find_main_adverb_inflection` and `find_adverb_inflections`, will be preserved but updated to use the new logic from the refactored `_inflect_lemma`.

## 2. Detailed Plan

### Phase 1: Analysis

1. **Read Target Files**: I will begin by reading the following files to understand their current structure and logic:
   - `src/core/transfero/_adjective_inflection.py`
   - `src/core/transfero/_adverb_inflection.py`
   - `src/core/transfero/_noun_inflection.py`
   - `src/core/transfero/_verb_inflection.py`

### Phase 2: Refactoring

I will refactor each module sequentially. For each module, I will perform the following steps:

1. **Refactor `_inflect_lemma` function**:

   - Modify the function to compute all possible inflections for a given lemma.
   - The function will be updated to return a `tuple[str, ...]`. The first element of this tuple will be the main inflection, and the subsequent elements will be the other inflections.

1. **Update `find_main_*_inflection`**:

   - This function will be simplified to call the refactored `_inflect_lemma`.
   - It will return only the first element of the tuple returned by `_inflect_lemma`.

1. **Update `find_*_inflections`**:

   - This function will also be simplified to call the refactored `_inflect_lemma`.
   - It will return the entire tuple of inflections converted to a set.

### Phase 3: Verification

1. **Run Tests**: After refactoring all the modules, I will run the project's test suite to ensure that the changes have not introduced any regressions. Based on the `AGENTS.md` file, I will use the following command:
   ```bash
   poetry run pytest -m 'not manual and not integration'
   ```
1. **Review Changes**: I will review the changes to ensure they align with the plan and coding conventions.
