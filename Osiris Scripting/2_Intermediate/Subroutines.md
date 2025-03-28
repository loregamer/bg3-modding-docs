# Subroutines in Osiris

Osiris has two types of subroutines: queries and procedures. These allow you to organize your code for reuse and readability.

## Queries (QRY)

Queries are used to check conditions and can be used to implement OR-conditions (which aren't natively supported in Osiris rules). A query succeeds if any of its definitions' conditions are fulfilled.

### Query Syntax

```
QRY
QRY_MyPrefix_QueryName((TYPE1)_Param1[, (TYPE2)_Param2...])
[AND
ExtraCondition1
...]
THEN
Action1;
[Action2;
...]
```

### Query Features

- Queries can have multiple definitions with the same name and parameter count
- If any of these definitions succeeds, the query is considered successful
- This allows you to implement OR-like behavior
- Only the first definition needs to specify parameter types

### Example: Simple Query

```
QRY
QRY_IsInDanger((CHARACTERGUID)_Character)
AND
CharacterHasStatus(_Character, "BURNING", 1)
THEN
DB_NOOP(1);

QRY
QRY_IsInDanger(_Character)
AND
CharacterHasStatus(_Character, "POISONED", 1)
THEN
DB_NOOP(1);
```

This query checks if a character is in danger by looking for either the "BURNING" or "POISONED" status. If either condition is true, the query succeeds.

### Using Queries in Rules

```
IF
CharacterCreated(_Character)
AND
QRY_IsInDanger(_Character)
THEN
CharacterStatusText(_Character, "In Danger!");
```

### DB_NOOP Convention

In the examples above, you may notice `DB_NOOP(1)` in the THEN section. This is a common convention in Osiris:

- Queries need to have at least one action
- When a query only needs to check conditions, we use `DB_NOOP(1)` as a "do nothing" action
- `DB_NOOP` is just a conventional name; it's not a special built-in feature

## Procedures (PROC)

Procedures are collections of actions that can be called from multiple places. They can also include conditional checks.

### Procedure Syntax

```
PROC
PROC_MyPrefix_ProcName((TYPE1)_Param1[, (TYPE2)_Param2...])
[AND
ExtraCondition1
...]
THEN
Action1;
[Action2;
...]
```

### Procedure Features

- Procedures can have multiple definitions with the same name and parameter count
- When a procedure is called, ALL matching definitions are executed
- Only the first definition needs to specify parameter types
- Procedures can include condition checks, allowing for conditional execution

### Example: Conditional Procedure

```
PROC
PROC_HealIfInjured((CHARACTERGUID)_Character)
AND
CharacterGetHitpointsPercentage(_Character, _HP)
AND
_HP < 100
THEN
CharacterHeal(_Character, 100);

PROC
PROC_HealIfInjured(_Character)
THEN
CharacterStatusText(_Character, "Healed!");
```

This procedure has two definitions:
1. The first only executes if the character's HP is below 100%, healing them
2. The second always executes, showing a status message

When called, both definitions are evaluated and potentially executed.

### Using Procedures in Rules

```
IF
CharacterCreated(_Character)
THEN
PROC_HealIfInjured(_Character);
```

## Query vs. Procedure: When to Use Which

### Use Queries When:

- You need to check for one of several conditions (OR functionality)
- You want to encapsulate complex condition checks
- You need to return a result that other rules will check

### Use Procedures When:

- You have a set of actions that need to be performed in multiple places
- You want to execute actions conditionally
- You need to organize your code into logical, reusable units

## Subroutine Scope and Availability

- Subroutines are only available when the goal that defines them is active
- Once a goal is completed, its subroutines are no longer available
- Make sure the goals containing your subroutines are active when you need to call them

## Best Practices

1. **Naming Conventions**: 
   - Always prefix queries with `QRY_` and procedures with `PROC_`
   - Include a mod-specific prefix to avoid naming conflicts

2. **Modularity**:
   - Break complex logic into smaller, reusable subroutines
   - Create specialized queries for commonly checked conditions

3. **Type Specification**:
   - Always specify parameter types in the first definition of a subroutine
   - Be consistent with parameter naming across all definitions

4. **Documentation**:
   - Add comments to explain what your subroutines do
   - Document the expected parameter types and any side effects

## Next Steps

Continue to the [Program Execution](Program_Execution.md) section to learn how Osiris programs are executed.
