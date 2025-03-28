# Rules in Osiris

Rules are the heart of Osiris scripting. A rule consists of conditions that, when met, trigger specific actions.

## Rule Structure

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

Rules are evaluated whenever one of the trigger conditions becomes fulfilled. If all trigger and extra conditions are fulfilled at that point, the actions of the rule are executed.

## Trigger Conditions

Trigger conditions are what cause a rule to be evaluated. There are two main types:

### 1. Osiris Events

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

### 2. Database Triggers

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

## Extra Conditions

Extra conditions are additional checks that don't trigger the rule but must be true for the rule to execute its actions:

### 1. Osiris Queries

Queries ask the game engine about aspects of the current game state:

```
IF
DB_IsPlayer(_Character)
AND
CharacterIsDead(_Character, 1) // Query: is the character dead?
THEN
DB_DeadPlayer(_Character);
```

### 2. User Queries

You can define your own queries (see [Subroutines](Subroutines.md)) and use them in conditions:

```
IF
DB_IsPlayer(_Character)
AND
QRY_IsInCombat(_Character) // User-defined query
THEN
DB_PlayerInCombat(_Character);
```

### 3. Comparisons

You can compare values using operators like `==`, `!=`, `<`, `<=`, `>`, and `>=`:

```
IF
DB_PlayerLevel(_Character, _Level)
AND
_Level >= 5 // Comparison
THEN
DB_HighLevelPlayer(_Character);
```

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

## Rule Evaluation

A few important things to understand about rule evaluation:

1. **Multiple Rules**: You can have multiple rules that check on the same trigger conditions. They will all be executed when the conditions are satisfied.

2. **Rule Order**: Rules are executed in the order they appear in the story (alphabetically by goal name).

3. **One-Time Execution**: Rules only trigger when their conditions become true, not continuously while they are true.

4. **No OR Conditions**: Osiris rule conditions can only be combined with AND, not OR. Use user-defined queries to implement OR-conditions.

## Examples

### Event-Triggered Rule

```
IF
CharacterDied(_Character) // Event trigger
AND
DB_IsPlayer(_Character) // Database check
THEN
DB_PlayerDied(_Character);
PlaySound(_Character, "Death");
```

### Database-Triggered Rule

```
IF
DB_PlayerJoinedParty(_Character) // Database trigger
AND
CharacterGetLevel(_Character, _Level) // Query
AND
_Level < 3 // Comparison
THEN
CharacterLevelUpTo(_Character, 3); // Action
```

### Multiple Rules for Same Trigger

```
// First rule
IF
DB_QuestCompleted("MainQuest")
THEN
DB_GameFinished(1);

// Second rule - also triggers on the same condition
IF
DB_QuestCompleted("MainQuest")
THEN
PlayEndCredits();
```

## Next Steps

Continue to the [Variables](Variables.md) section to learn how to use variables to make your rules more flexible.
