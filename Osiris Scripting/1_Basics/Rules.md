# Rules in Osiris

Rules are the heart of Osiris scripting. A rule consists of conditions that, when met, trigger specific actions.

## Rule Structure

Rules in Osiris have two parts:

1. One or more conditions

   - This part begins with `IF`
   - This part is **evaluated** whenever the rule is **triggered**
   - Each condition is on its own line
   - Each condition is separated by the line `AND`

2. One or more actions
   - This part begins with `THEN`
   - This part is **executed** when all of the conditions are met
   - Each action is on its own line
   - Each action ends with `;`

The basic structure of a rule is:

```
IF
TriggerCondition
[AND
TriggerCondition | ExtraCondition]
[AND
TriggerCondition | ExtraCondition
..]
THEN
Action1;
[Action2;
..]
```

## Types of Conditions

There are two categories of conditions in Osiris:

1. A **trigger condition** will trigger the rule for evaluation as soon as it becomes true.
2. An **extra condition** will never trigger an evaluation.

No matter what triggers the rule, every single condition (triggers _and_ extras) must all be true when a rule is evaluated for it to execute its actions.

### Trigger Conditions

Trigger conditions are what cause a rule to be evaluated. There are two main types:

#### 1. Osiris Events

Events notify Osiris that something has happened in the game. For example:

- A character died
- An item was picked up
- A dialog started

**Important**: An event can only be used as the **first** trigger condition. Putting it anywhere else will result in a compilation error.

Example:

```
IF
CharacterDied(_Character) // Event as the first trigger condition
AND
DB_IsPlayer(_Character)
THEN
DB_PlayerDied(1);
```

#### 2. Database Triggers

A rule can be triggered when a new database fact is added. Database fact trigger conditions can appear anywhere in a rule's conditions.

Example:

```
IF
DB_IsPlayer(_Character) // Triggered when a character is added to this database
AND
CharacterGetLevel(_Character, _Level)
THEN
DB_PlayerLevel(_Character, _Level);
```

You can also check for database facts being removed by using the `NOT` operator, but only if it's not the first condition:

```
IF
DB_SomeOtherCondition(1)
AND
NOT DB_IsPlayer(_Character) // Triggers when this fact is removed
THEN
DB_PlayerLeft(_Character);
```

### Extra Conditions

Extra conditions are additional checks that don't trigger the rule but must be true for the rule to execute its actions:

#### 1. Osiris Queries

Queries ask the game engine about aspects of the current game state:

```
IF
DB_IsPlayer(_Character)
AND
CharacterIsDead(_Character, 1) // Query: is the character dead?
THEN
DB_DeadPlayer(_Character);
```

#### 2. User Queries

You can define your own queries and use them in conditions:

```
IF
DB_IsPlayer(_Character)
AND
QRY_IsInCombat(_Character) // User-defined query
THEN
DB_PlayerInCombat(_Character);
```

#### 3. Comparisons

You can compare values using operators like `==`, `!=`, `<`, `<=`, `>`, and `>=`:

```
IF
DB_PlayerLevel(_Character, _Level)
AND
_Level >= 5 // Comparison
THEN
DB_HighLevelPlayer(_Character);
```

## What Cannot Be Used As Conditions

It's important to understand what **cannot** be used as a condition in rules:

1. **Procedures (PROC)**: Procedures cannot be used as conditions in rules. They are only meant to be called as actions after the `THEN` keyword. This is a common mistake:

   ```
   // INCORRECT - Will generate a compilation error
   IF
   PROC_SelectRandomStartOrigin() // Error: Procedure cannot be used as a condition
   THEN
   DoSomething();
   ```

2. **Osiris Calls**: Game engine calls are actions, not conditions:
   ```
   // INCORRECT - Will generate a compilation error
   IF
   CharacterHeal(_Character, 10) // Error: Call cannot be used as a condition
   THEN
   DB_HealedCharacter(_Character);
   ```

To check conditions related to a procedure's functionality, consider:

1. Creating a query (QRY) to encapsulate the condition check
2. Using database entries to track states that the procedure would have checked
3. Using existing Osiris queries to check the relevant game state

## Rule Evaluation and Variables

When a rule is triggered for evaluation, Osiris will assign values to variables based on the database conditions. If there are multiple facts that can be assigned to a variable, Osiris will evaluate the rule for each possible value.

For example, if we have:

```
IF
DB_Players(_Character)
THEN
CharacterGiveExperience(_Character, 1000);
```

If there are four player characters in the database, this rule will execute once for each character.

When using multiple database conditions with variables, the rule will be evaluated for every possible combination of values. This can lead to exponential growth in the number of evaluations, which is something to be aware of for performance reasons.

## Actions

Actions are the statements that execute when all conditions of a rule are fulfilled:

### 1. Osiris Calls

```
IF
DB_IsPlayer(_Character)
AND
CharacterIsDead(_Character, 1)
THEN
CharacterResurrect(_Character); // Call to the game engine
```

### 2. Procedure Calls

```
IF
DB_IsPlayer(_Character)
AND
CharacterIsDead(_Character, 1)
THEN
PROC_ResurrectAndHeal(_Character); // Call to user-defined procedure
```

### 3. Database Operations

```
IF
DB_IsPlayer(_Character)
AND
CharacterIsDead(_Character, 1)
THEN
DB_PlayerDied(_Character); // Add a database fact
NOT DB_AlivePlayer(_Character); // Remove a database fact
```

## Rule Optimization

To optimize rule performance, consider these practices:

1. **Filter Early**: Put conditions that filter the most values at the beginning of your rule to reduce the number of evaluations.

2. **Avoid Unnecessary Variable Combinations**: Be cautious when using multiple variables from databases, as this can lead to combinatorial explosion.

3. **Use Constants When Possible**: If you only care about specific values, use constants instead of variables:

   ```
   // Less efficient - evaluates for all players
   IF
   DB_Players(_Character)
   AND
   _Character == S_Player_Wyll_c774d764-4a17-48dc-b470-32ace9ce447d
   THEN
   Action1;

   // More efficient - only triggers for Wyll
   IF
   DB_Players(S_Player_Wyll_c774d764-4a17-48dc-b470-32ace9ce447d)
   THEN
   Action1;
   ```

## Common Mistakes and Their Solutions

### 1. Using a Procedure as a Condition

**Problem:**

```
// INCORRECT
IF
PROC_SelectRandomStartOrigin()
AND
DB_RandomizeStartOrigin(1, 0)
THEN
PROC_SetAsStartOrigin(_Character);
```

**Solution:**
Instead of trying to intercept a procedure call, inspect the code to see if there's a database value you can set that the procedure will check, or create a query to encapsulate the condition:

```
// CORRECT
// In INIT section:
DB_PredefinedStartOrigin(_DesiredCharacter);

// The existing procedure will then use this value:
// PROC
// PROC_SelectRandomStartOrigin()
// AND
// DB_PredefinedStartOrigin(_Origin)
// THEN
// PROC_SetAsStartOrigin(_Origin);
```

### 2. Confusing Queries and Procedures

**Problem:**

```
// INCORRECT
IF
DB_IsPlayer(_Character)
AND
PROC_IsInDanger(_Character) // Error: Using a procedure as a condition
THEN
CharacterStatusText(_Character, "In Danger!");
```

**Solution:**
Create a query instead of a procedure for condition checking:

```
// CORRECT
QRY
QRY_IsInDanger((CHARACTERGUID)_Character)
AND
CharacterHasStatus(_Character, "BURNING", 1)
THEN
DB_NOOP(1);

// Then use it in your rule
IF
DB_IsPlayer(_Character)
AND
QRY_IsInDanger(_Character)
THEN
CharacterStatusText(_Character, "In Danger!");
```

## Rule Evaluation

A few important things to understand about rule evaluation:

1. **Multiple Rules**: You can have multiple rules that check on the same trigger conditions. They will all be executed when the conditions are satisfied.

2. **Rule Order**: Rules are executed in the order they appear in the story (alphabetically by goal name).

3. **One-Time Execution**: Rules only trigger when their conditions become true, not continuously while they are true.

4. **No OR Conditions**: Osiris rule conditions can only be combined with AND, not OR. Use user-defined queries to implement OR-conditions.

## Using the Story Editor

When working with the Story Editor, remember:

1. The editor has three separate panes for INIT, KB, and EXIT sections.
2. In the KB pane, rules must follow the proper syntax with IF and THEN sections.
3. Procedures defined in other goals are not directly visible in the editor, so you can't see their implementation.
4. The editor will check syntax but cannot detect all logical errors.

## Next Steps

Continue to the [Variables](../2_Intermediate/Variables.md) section to learn how to use variables to make your rules more flexible.
