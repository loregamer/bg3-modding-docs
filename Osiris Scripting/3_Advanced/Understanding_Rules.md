# Understanding Osiris Rules

This guide provides an in-depth explanation of how Osiris evaluates and executes rules. While some topics are relatively simple, they're explained in technical detail to give you a solid understanding of the mechanics.

## Basic Definitions

Before diving deeper, let's review some fundamental terms:

- **Rule**: The smallest standalone piece of Osiris code. Each rule describes what to do in a certain situation and can be combined with other rules to achieve more complicated behaviors.
- **Fact**: A set of one or more values. Each value is also sometimes called a column, to use database terminology.
- **Database**: A container for zero or more unique facts. Facts can be added (also called **defined**) or removed from the database at any time.

## The Structure of an Osiris Rule

Every rule in Osiris has two parts:

1. **Conditions**
   * Begins with `IF`
   * Evaluated whenever the rule is triggered
   * Each condition is on its own line
   * Each condition is separated by the line `AND`

2. **Actions**
   * Begins with `THEN`
   * Executed when all conditions are met
   * Each action is on its own line
   * Each action ends with `;`

Example structure:
```
IF
Condition1
AND
Condition2
THEN
Action1;
Action2;
```

## Conditions in Detail

### Types of Conditions

There are two categories of conditions in Osiris:

1. **Trigger conditions**: Will trigger the rule for evaluation as soon as they become true
2. **Extra conditions**: Will never trigger an evaluation

No matter what triggers the rule, every single condition (triggers *and* extras) must be true when a rule is evaluated for it to execute its actions.

### Database Conditions

#### Constants

The simplest database condition uses constant values:

```
IF
DB_Letters("H") // Checks if "H" exists in DB_Letters
THEN
Action1;
```

This rule triggers when "H" is added to DB_Letters and executes if "H" is in the database.

#### Inverting with NOT

You can require a database to *not* contain a fact using `NOT`:

```
IF
DB_Letters("H")
AND
NOT DB_Letters("I") // Requires "I" to NOT be in DB_Letters
THEN
Action1;
```

Note: `NOT` cannot be used as the first condition of a rule.

#### Using Variables

Instead of constants, you can use undeclared variables:

```
IF
DB_Letters(_Letter) // Matches ANY letter in the database
THEN
Action1;
```

When using an undeclared variable in a database condition:
- Osiris attempts to assign it a value from a fact in the database
- If multiple facts match, the rule is evaluated separately for each match
- The variable keeps its assigned value for the rest of the rule

![Variable Assignment Diagram](https://example.com/variable_assignment.png)

#### Facts with Multiple Values

For databases with facts containing multiple values:

```
IF
DB_Letters(_Letter, _Value) // Matches any fact with two values
THEN
Action1;
```

You can mix variables and constants:

```
IF
DB_Letters(_Letter, 16) // Matches facts where the second value is 16
THEN
Action1;
```

You can also use unbound variables with just an underscore (`_`) when you don't need a value:

```
IF
DB_Letters(_, 16) // Matches any fact where the second value is 16
THEN
Action1;
```

### Combined Database Conditions

When you have multiple database conditions with variables, Osiris evaluates every possible combination:

```
IF
DB_Letters(_Letter)
AND
DB_Numbers(_Number)
THEN
Action1;
```

If DB_Letters has 2 facts and DB_Numbers has 2 facts, the rule is evaluated 4 times (2×2).

![Combinations Diagram](https://example.com/combinations.png)

#### Advanced Example - Self-Combinations

Rules can have combinations from the same database:

```
IF
DB_Letters(_New)
AND
DB_Letters(_Old)
AND
_New != _Old
THEN
NOT DB_Letters(_Old);
```

This rule ensures the database only keeps the most recently added fact by removing all others.

### Events

Events are trigger conditions that must be the first condition in a rule. They respond to game occurrences:

```
IF
AddedTo(_Object, _Character, _)
THEN
Action1;
```

Events provide parameters with information about what happened. In the above example:
- `_Object`: The object added
- `_Character`: Who received the object
- `_`: Unbound variable for the add type (we don't need it)

Events trigger every rule that uses them when they occur in the game.

### Queries

Queries are extra conditions that get information about the game state:

```
IF
DB_Players(_Player)
AND
GetHitpoints(_Player, _HP) // Query to get player's hitpoints
THEN
Action1;
```

Queries have:
- **In-parameters**: Values you provide to the query
- **Out-parameters**: Values returned by the query

You can use out-parameters in three ways:
1. Assign to an undeclared variable: `GetHitpoints(_Player, _HP)`
2. Require a specific value: `GetHitpoints(_Player, 0)` (only true if HP is 0)
3. Use an unbound variable: `GetHitpoints(_Player, _)`

#### Custom Queries

You can define your own queries:

```
QRY
QRY_CustomQuery((INTEGER)_Number)
AND
Condition1
THEN
DB_NOOP(1);
```

Use them in rules:

```
IF
Condition1
AND
QRY_CustomQuery(2)
THEN
Action1;
```

### Comparisons

Comparisons require two values to have a certain relationship:

```
IF
DB_PlayerLevel(_Player, _Level)
AND
_Level >= 5 // Comparison
THEN
Action1;
```

Comparison operators:
- `==`: Equality
- `!=`: Inequality
- `<`: Less than
- `<=`: Less than or equal
- `>`: Greater than
- `>=`: Greater than or equal

## Actions in Detail

### Database Actions

Adding a fact to a database:

```
IF
Condition1
THEN
DB_Letters("H"); // Adds "H" to DB_Letters
```

Removing a fact from a database:

```
IF
Condition1
THEN
NOT DB_Letters("H"); // Removes "H" from DB_Letters
```

### Calls

Calls change the game state:

```
IF
LongRestFinished()
AND
DB_Players(_Player)
THEN
AddGold(_Player, 50); // Gives 50 gold to the player
```

Some calls have overloaded versions with fewer parameters:

```
Equip(_Character, _Item) // Basic version
Equip(_Character, _Item, 0, 0, 1) // Full version with all parameters
```

### Procedures

Procedures combine multiple actions:

```
PROC
PROC_ProcedureName((Type1)Parameter1)
AND
Condition1
THEN
Action1;
Action2;
```

Call them like functions:

```
IF
Condition1
THEN
PROC_ProcedureName(Value1);
```

## Performance Considerations

To optimize rule performance:

1. **Filter Early**: Put conditions that filter the most values at the beginning of your rule.

2. **Avoid Unnecessary Variable Combinations**: Be careful with multiple database variables.

3. **Use Constants When Possible**: If you only care about specific values, use constants instead of variables:

   ```
   // Less efficient
   IF
   DB_Players(_First)
   AND
   _First == S_Player_Wyll_c774d764-4a17-48dc-b470-32ace9ce447d
   THEN
   Action1;
   
   // More efficient
   IF
   DB_Players(S_Player_Wyll_c774d764-4a17-48dc-b470-32ace9ce447d)
   THEN
   Action1;
   ```

The difference in efficiency can be significant, especially with multiple combined variables:

![Efficiency Comparison](https://example.com/efficiency.png)

## Limiting Rule Execution

To limit a rule to execute only once, use the `QRY_OnlyOnce` query:

```
IF
DB_Players(_Player)
AND
Condition1
AND
QRY_OnlyOnce("UniqueString") // Only evaluates to true once
THEN
Action1;
```

`QRY_OnlyOnce` should generally be the last condition to ensure all other conditions are met first.

To reset this check, use `QRY_OnlyOnce_Reset` in another rule:

```
IF
LongRestFinished()
THEN
QRY_OnlyOnce_Reset("UniqueString");
```

## Summary

Understanding how Osiris evaluates rules is crucial for creating efficient and effective scripts. The key concepts to remember are:

1. Rules are triggered by events or database changes
2. Variables split rule evaluation for each possible value
3. Multiple variables create combinations of evaluations
4. All conditions must be true for actions to execute
5. Consider performance when writing complex rules

By mastering these mechanics, you'll be able to create sophisticated behaviors while maintaining good performance.
