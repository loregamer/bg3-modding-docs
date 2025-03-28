# Osiris Gotchas

When working with Osiris, there are some unexpected behaviors and limitations that can trip you up. This section covers common "gotchas" and how to avoid them.

## Understanding Result Sets

One of the most important concepts to understand in Osiris is how result sets work.

### What are Result Sets?

When you query a database in Osiris, it gives you all rows that match your query. This collection of matching rows is called a result set.

### How Result Sets are Combined

When you have multiple database queries in a rule condition, Osiris combines their result sets in a specific way:

1. It generates a result set for the first query
2. For each row in that result set, it generates a result set for the second query
3. It combines these sets and repeats for any subsequent queries

### Example of Result Set Explosion

Consider this example:

```
DB_A("a");
DB_A("b");

DB_B(1);
DB_B(2);

PROC
PROC_QueryDatabase()
AND
DB_A(_A)
AND
DB_B(_B)
THEN
DB_AB(_A, _B);
```

What happens?

1. Osiris gets the result set for `DB_A(_A)`: `[("a"), ("b")]`
2. For each row:
   - For "a", it gets the result set for `DB_B(_B)`: `[(1), (2)]`
   - So we get: `[("a", 1), ("a", 2)]`
   - For "b", it gets the result set for `DB_B(_B)`: `[(1), (2)]`
   - So we get: `[("b", 1), ("b", 2)]`
3. The combined result set is: `[("a", 1), ("a", 2), ("b", 1), ("b", 2)]`
4. The action is executed for each row

This can lead to a large number of combinations with multiple unconstrained queries!

### Optimization Strategies

To avoid result set explosion:

1. **Most Constrained First**: Put the most constrained queries first
2. **Early Filtering**: Filter as early as possible in the condition chain
3. **Break Up Complex Queries**: Use procedures to divide complex operations

```
// Instead of this (can explode in complexity)
PROC
PROC_ComplicatedQuery((CHARACTERGUID)_Player)
AND
DB_Characters(_Enemy1)
AND
DB_Characters(_Enemy2)
AND
CharacterIsEnemy(_Enemy1, _Player, 1)
AND
CharacterIsEnemy(_Enemy2, _Player, 1)
THEN
// ...

// Do this (more controlled)
PROC
PROC_Step1_FindEnemies((CHARACTERGUID)_Player)
AND
DB_Characters(_Enemy)
AND
CharacterIsEnemy(_Enemy, _Player, 1)
THEN
DB_TempEnemies(_Enemy);

PROC
PROC_Step2_ProcessEnemies(_Player)
AND
DB_TempEnemies(_Enemy1)
AND
DB_TempEnemies(_Enemy2)
AND
_Enemy1 != _Enemy2
THEN
// ...

PROC
PROC_Step3_Cleanup()
AND
DB_TempEnemies(_Enemy)
THEN
NOT DB_TempEnemies(_Enemy);
```

## Osiris Bug with User Queries in Rule Conditions

There is a known bug in Osiris regarding user queries in rule conditions that modify databases that are then checked in the same rule.

### The Bug

```
IF
DB_ThatTriggersRule1(_Char)
AND
QRY_ReturnAResult(_Char)
AND
DB_QueryResult(_Result) // This checks a database modified by the query
THEN
// This may crash or behave unexpectedly
```

### How to Avoid It

Move the query and result checking to a procedure:

```
// Instead of putting it directly in a rule
IF
DB_ThatTriggersRule1(_Char)
THEN
PROC_CheckQueryResults(_Char);

// Put it in a procedure
PROC
PROC_CheckQueryResults((CHARACTERGUID)_Char)
AND
QRY_ReturnAResult(_Char)
AND
DB_QueryResult(_Result)
THEN
// This is safe
```

## Type Mismatch Issues

A common source of errors is type mismatches, especially with GUIDs.

### First Occurrence Rule

Remember that the **first occurrence** of a database defines the types for all columns:

```
// This sets the type of the first column to GUIDSTRING
DB_Characters(MyCharacter_12345);

// Later, if you try to use it as CHARACTERGUID without a cast:
IF
DB_Characters(_Char)
AND
CharacterGetLevel(_Char, _Level) // ERROR: _Char is GUIDSTRING, not CHARACTERGUID
```

### Type Casting

Always use explicit type casts for GUID types:

```
DB_Characters((CHARACTERGUID)MyCharacter_12345);

// Or when using:
IF
DB_Characters(_Char)
THEN
CharacterGetLevel((CHARACTERGUID)_Char, _Level); // WORKS: _Char is cast to CHARACTERGUID
```

## Database Cleanup Issues

Not cleaning up databases can lead to:
- Larger save game files
- Performance degradation
- Unexpected behavior if old facts are matched later

### Best Practice

Always clean up temporary databases in the EXIT section of goals or at the end of procedures:

```
PROC
PROC_UsingTempDB()
THEN
DB_TempResult(1);
// ... use DB_TempResult ...
NOT DB_TempResult(1); // Clean up
```

## Frame Delay Issues

As explained in [Program Execution](Program_Execution.md), some game state changes don't take effect immediately.

### Dialog Flag Example

```
// In a dialog:
// 1. Set flag MYPRE_give_item
// 2. Immediately check flag MYPRE_gave_item (set by Osiris) - FAILS
// 3. Add an empty frame delay node
// 4. Check flag MYPRE_gave_item - WORKS
```

### Best Practice

Add frame delay nodes in dialogs when you need to check flags that are set by Osiris in response to other flags.

## Ordering Gotchas

### Alphabetical Goal Ordering

Remember that goals are initialized in alphabetical order by name:

```
// Goal: AAA_First (initializes first)
INIT
    DB_SomeDatabase(1);

// Goal: ZZZ_Last (initializes after AAA_First)
IF
DB_SomeDatabase(1) // This works because AAA_First initializes first
THEN
// ...
```

But:

```
// Goal: ZZZ_Last (initializes after AAA_First)
INIT
    PROC_FromFirstGoal(); // FAILS if PROC_FromFirstGoal is defined in AAA_First
                          // because ZZZ_Last INIT runs before AAA_First is active
```

### Rule Execution Order

Rules execute in the order they appear in story:

```
// Rule 1
IF
DB_TriggerFact(1)
THEN
DB_Result(1);

// Rule 2
IF
DB_TriggerFact(1)
AND
DB_Result(1) // This works because Rule 1 executes first and sets DB_Result(1)
THEN
// ...
```

But be careful with dependencies between rules in different goals, as their order depends on the alphabetical ordering of goal names.

## Next Steps

Continue to the [Osiris API Reference](API_Reference.md) section to learn about the available APIs for interacting with the game world.
