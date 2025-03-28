# Variables in Osiris

Variables in Osiris allow you to work with values in a more flexible way, without needing to know the exact values at the time you write your code.

## Variable Basics

In Osiris, variables:

- Always start with an underscore (`_`)
- Do not need to be declared before use
- Are automatically typed based on their first use
- Have a scope limited to a single rule, procedure, or query

## Variable Declaration and Assignment

Unlike traditional programming languages, you don't explicitly declare variables in Osiris. Instead, they are implicitly declared when they first appear in a condition.

```
IF
DB_IsPlayer(_Player) // _Player is implicitly declared and assigned
AND
CharacterGetLevel(_Player, _Level) // _Level is declared and assigned the result
THEN
DB_PlayerLevel(_Player, _Level);
```

## Variable Scope

Variables only exist within the rule, procedure, or query where they are used:

```
IF
DB_IsPlayer(_Player)
THEN
DB_PlayerFound(_Player);

IF
DB_PlayerFound(_AnotherPlayer) // This is a different _AnotherPlayer variable
THEN
// Do something else
```

The `_Player` variable in the first rule is completely separate from the `_AnotherPlayer` variable in the second rule, even if they might contain the same value.

## Variable Types

Variables take on the type of the value they're first associated with:

```
IF
DB_NumberList(_Number) // _Number is an INTEGER
AND
DB_StringList(_Text) // _Text is a STRING
THEN
// _Number and _Text are now typed variables
```

## Input and Output Parameters

Variables can be used in different ways depending on how they're used in conditions:

### Input Parameters

When a variable already has a value assigned and is used to filter a database:

```
DB_Players("John", 10);
DB_Players("Jane", 5);

IF
_Name = "John" // _Name is assigned "John"
AND
DB_Players(_Name, _Level) // _Name is an input parameter
THEN
// This will only match the first entry
// _Level will be 10
```

### Output Parameters

When a variable doesn't have a value yet and is used to receive values from a database:

```
DB_Players("John", 10);
DB_Players("Jane", 5);

IF
DB_Players(_Name, _Level) // Both are output parameters
THEN
// This will iterate over all entries
// First iteration: _Name = "John", _Level = 10
// Second iteration: _Name = "Jane", _Level = 5
```

## Variable Uses

### Iterating Database Contents

One powerful use of variables is to iterate through all values in a database:

```
IF
DB_Players(_Player, _Level)
THEN
// This rule will execute once for each entry in DB_Players
// Each time with different values in _Player and _Level
```

### Looking Up Facts (Associative Arrays)

You can use variables to look up specific entries in a database:

```
IF
DB_WantToFind(_Name) // For example, _Name = "John"
AND
DB_Players(_Name, _Level) // Find the entry with the matching name
THEN
// _Level will contain the level of the player with name _Name
```

### Passing Values Between Rules

You can use databases to pass values between rules:

```
IF
CharacterCreated(_Character)
THEN
DB_NewCharacter(_Character);

IF
DB_NewCharacter(_Character)
AND
CharacterGetLevel(_Character, _Level)
THEN
// Process the new character with its level
```

## Best Practices

1. **Meaningful Names**: Use descriptive variable names to make your code more readable (e.g., `_Player` instead of `_P`).

2. **Prefix Consistency**: Always start variable names with an underscore to distinguish them from constants and database names.

3. **Type Awareness**: Be mindful of the types of your variables, especially when working with queries that expect specific types.

4. **Minimize Variable Count**: Try to reuse variables when possible to keep your code clean and understandable.

5. **Variable Initialization**: When using a variable as an input parameter, make sure it has been assigned a value earlier in the same rule.

## Next Steps

Continue to the [Subroutines](Subroutines.md) section to learn how to create your own queries and procedures in Osiris.
