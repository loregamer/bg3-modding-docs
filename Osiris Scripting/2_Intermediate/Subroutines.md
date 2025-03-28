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
- **Most importantly: Queries can be used as conditions in rules**

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
- **Critical limitation: Procedures can ONLY be used as actions after the THEN statement in rules, never as conditions**

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
PROC_HealIfInjured(_Character); // CORRECT: Procedure used as an action
```

### Incorrect Usage of Procedures

```
// INCORRECT - Will generate a compilation error
IF
PROC_HealIfInjured(_Character) // Error: Procedure cannot be used as a condition
THEN
DB_PlayerHealed(_Character);
```

## Working with Existing Procedures

When working with existing procedures in the game code, remember these important points:

1. **You cannot override a procedure's implementation directly** - Osiris will combine all procedure definitions with the same name.

2. **You cannot intercept a procedure call by using it as a condition** - Procedures can never be used as conditions.

3. **The right way to modify behavior:**
   - Look for database entries the procedure checks and modify those
   - Create new procedures with different names that implement your desired behavior
   - In some cases, you may need to modify the calling rule instead

### Example: Modifying a Game Procedure's Behavior

Let's say there's an existing procedure in the game for selecting a default origin character:

```
// Original game code (you can't modify this directly)
PROC
PROC_SelectRandomStartOrigin()
AND
NOT DB_PredefinedStartOrigin(_)
AND
NOT DB_RandomizeStartOrigin(1)
THEN
PROC_SetAsStartOrigin((CHARACTER)S_Player_Astarion_c7c13742-bacd-460a-8f65-f864fe41f255);

PROC
PROC_SelectRandomStartOrigin()
AND
DB_PredefinedStartOrigin(_Origin)
THEN
NOT DB_PredefinedStartOrigin(_Origin);
PROC_SetAsStartOrigin(_Origin);
```

Instead of trying to override the procedure itself or use it in a condition, you can:

```
// In your mod's INIT section:
DB_PredefinedStartOrigin((CHARACTER)S_Player_DarkUrge_c66bc36f-7cb0-41fa-92f0-6d81d7d17ba3);
```

This allows you to change the behavior without modifying the procedure directly.

## Query vs. Procedure: When to Use Which

### Use Queries When:

- You need to check for one of several conditions (OR functionality)
- You want to encapsulate complex condition checks
- You need to return a result that other rules will check
- **You want to use the subroutine as a condition in rules**

### Use Procedures When:

- You have a set of actions that need to be performed in multiple places
- You want to execute actions conditionally
- You need to organize your code into logical, reusable units
- **You are calling the subroutine as an action after THEN in rules**

## Subroutine Scope and Availability

- Subroutines are only available when the goal that defines them is active
- Once a goal is completed, its subroutines are no longer available
- Make sure the goals containing your subroutines are active when you need to call them

## Common Mistakes to Avoid

1. **Using a procedure as a condition in a rule:**

   ```
   // INCORRECT - Will cause a compilation error
   IF
   PROC_DoSomething(_Character)
   THEN
   DB_SomethingDone(_Character);
   ```

2. **Trying to define a procedure with the same name but different behavior:**
   Remember that all procedure definitions with the same name will be executed when called.

3. **Forgetting that a query needs at least one action:**
   Always include at least a `DB_NOOP(1);` action in your queries.

4. **Using a query as an action:**
   ```
   // INCORRECT - Queries are not meant to be called as actions
   IF
   DB_SomeCondition(_Character)
   THEN
   QRY_SomeQuery(_Character); // Error: Inappropriate use of a query
   ```

## Debugging Tips

To debug subroutines:

1. Add `DebugBreak("Message")` calls in your subroutines to print messages to the console.
2. Use database entries to track subroutine execution:

   ```
   PROC
   PROC_MyProcedure(_Param)
   THEN
   DB_ProcedureCalled("MyProcedure", _Param);
   ```

3. For complex issues, consider using the Story Editor's debugging tools.

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
