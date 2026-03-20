# Software Factory Run: {{ISSUE_ID}}

**Issue**: {{ISSUE_NUMBER}} - {{FEATURE_NAME}}
**Factory Run ID**: `factory-run-{{RUN_NUMBER}}`
**Date**: {{DATE}}
**Project**: {{PROJECT_NAME}}

---

## 🎯 The Seed (Entry Point)

### Problem Statement

{{DESCRIBE_THE_PROBLEM}}

### User Story

As a {{USER_TYPE}}
I want to {{DESIRED_ACTION}}
So that {{BENEFIT}}

### Current State

{{DESCRIBE_CURRENT_SITUATION}}
- Current behavior: {{WHAT_HAPPENS_NOW}}
- Pain points: {{WHAT_IS_BROKEN_OR_MISSING}}
- Files involved: {{LIST_RELEVANT_FILES}}

### Target State

{{DESCRIBE_DESIRED_OUTCOME}}
- Expected behavior: {{WHAT_SHOULD_HAPPEN}}
- Success looks like: {{CLEAR_DEFINITION_OF_DONE}}

---

## 📋 Validation Scenarios

### Scenario 1: {{SCENARIO_1_NAME}}
```
Given: {{INITIAL_CONDITION}}
When: {{ACTION_TAKEN}}
Then: {{EXPECTED_RESULT}}
```

### Scenario 2: {{SCENARIO_2_NAME}}
```
Given: {{INITIAL_CONDITION}}
When: {{ACTION_TAKEN}}
Then: {{EXPECTED_RESULT}}
```

### Scenario 3: {{SCENARIO_3_NAME}}
```
Given: {{INITIAL_CONDITION}}
When: {{ACTION_TAKEN}}
Then: {{EXPECTED_RESULT}}
```

{{ADD_MORE_SCENARIOS_AS_NEEDED}}

---

## 🔧 Implementation Requirements

### Technical Approach

{{DESCRIBE_IMPLEMENTATION_STRATEGY}}

**Option A**: {{APPROACH_1}}
- Pros: {{BENEFITS}}
- Cons: {{DRAWBACKS}}

**Option B**: {{APPROACH_2}}
- Pros: {{BENEFITS}}
- Cons: {{DRAWBACKS}}

**Recommendation**: {{CHOSEN_APPROACH}} because {{REASONING}}

### Files to Create/Modify

**Create**:
- `{{FILE_PATH_1}}` - {{PURPOSE}}
- `{{FILE_PATH_2}}` - {{PURPOSE}}

**Modify**:
- `{{FILE_PATH_3}}` - {{CHANGES_NEEDED}}
- `{{FILE_PATH_4}}` - {{CHANGES_NEEDED}}

### Dependencies

- {{LIBRARY_1}} - {{WHY_NEEDED}}
- {{LIBRARY_2}} - {{WHY_NEEDED}}

### Constraints

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}
- {{CONSTRAINT_3}}

---

## ✅ Success Criteria (Definition of Done)

### Technical Validation
- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}
- [ ] All scenarios passing (automated)
- [ ] No TypeScript/lint errors
- [ ] Build succeeds

### Quality Validation
- [ ] {{QUALITY_CHECK_1}}
- [ ] {{QUALITY_CHECK_2}}
- [ ] Visual quality maintained (if UI)
- [ ] Performance acceptable

### Code Quality
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Git commit with clear message
- [ ] Ready for deployment

---

## 🎬 Factory Execution Plan

### Phase 1: Prepare Scenarios
Create automated validation tests in `scenarios/`

### Phase 2: Agent Execution
Use Unified LLM Client to:
1. Read current implementation
2. {{STEP_2}}
3. {{STEP_3}}
4. Verify changes

### Phase 3: Validation Loop
1. Run scenarios
2. If failures → feed back to agent
3. Agent fixes issues
4. Re-run scenarios
5. Loop until all pass ✅

### Phase 4: Ship
1. Git commit
2. Create PR (or push to dev)
3. CI validates
4. Deploy
5. Close issue

---

**Estimated Time**:
- Traditional: {{MANUAL_ESTIMATE_HOURS}} hours
- Software Factory: {{FACTORY_ESTIMATE_MINUTES}} minutes

**Expected Speedup**: {{SPEEDUP_FACTOR}}x

---

**Template Version**: 1.0
**Last Updated**: March 2026
