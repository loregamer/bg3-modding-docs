# Osiris Queries

Queries are functions that retrieve information about the current game state or perform calculations. They are used in the condition section of Osiris rules to check conditions or get values.

## Using Queries

Queries are used as conditions between `IF` and `THEN` in rules. They require input parameters that specify what to check, and they return output parameters with the results.

Example:
```
IF
DB_Players(_Player)
AND
CharacterGetHitpoints(_Player, _HP) // Query with input and output
AND
_HP < 50
THEN
Action1;
```

## Query Parameters

Each query has two types of parameters:

1. **In-Parameters**: Values you provide to the query (marked with `[in]`)
2. **Out-Parameters**: Values returned by the query (marked with `[out]`)

For example, the `GetHitpoints` query has parameters:
```
GetHitpoints([in](GUIDSTRING)_Entity, [out](INTEGER)_HP)
```

You can use out-parameters in three ways:

1. **Assign to a Variable**: `GetHitpoints(_Player, _HP)` - Assigns the result to `_HP`
2. **Match a Specific Value**: `GetHitpoints(_Player, 0)` - Only true if HP equals 0
3. **Ignore the Result**: `GetHitpoints(_Player, _)` - Don't care about the result

You can find the details for queries in the official list:
- [Mod.io Osiris Queries](https://mod.io/g/baldursgate3/r/osiris-queries)
- [GitHub Osiris Queries](https://github.com/LaughingLeader/BG3ModdingTools/blob/master/generated/Osi.lua)

## Query Success vs Results

It's important to distinguish between query **success** and the **results** it returns:

- A query **succeeds** if it can return a valid result, regardless of what that result is
- The **result** is the value returned by the query

For example, if you check whether a character has a status with:
```
HasActiveStatus(_Character, "BURNING", _Result)
```

The query succeeds and sets `_Result` to either 1 (true) or 0 (false).

However, if you write:
```
HasActiveStatus(_Character, "BURNING", 1)
```

The query will only evaluate to true if the character has the BURNING status.

## Action Queries

Some queries perform operations instead of just retrieving information:

- **String Operations**: Concatenate, GetPosition, etc.
- **Mathematical Operations**: IntegerSum, IntegerProduct, etc.
- **Random Generation**: GetRandomBetween, etc.

Example of a math operation query:
```
IF
DB_Counter(_Value)
AND
IntegerSum(_Value, 1, _NewValue) // Adds 1 to _Value
THEN
NOT DB_Counter(_Value);
DB_Counter(_NewValue);
```

## Custom Queries (QRY)

You can define your own queries with the QRY syntax:

```
QRY
QRY_IsVulnerable((CHARACTERGUID)_Character)
AND
HasActiveStatus(_Character, "STUNNED", 1)
THEN
DB_NOOP(1);
```

Custom queries:
- Evaluate to true if all their conditions are met
- Can be used with `NOT` to invert the result
- Should use `DB_NOOP(1);` as the action if they don't need to perform any actual action
- Can include multiple conditions combined with AND

## Common Queries in BG3

Here are some commonly used queries in Baldur's Gate 3:

### Character-Related Queries

| Query | Description | Parameters |
|-------|-------------|------------|
| `CharacterGetLevel` | Gets a character's level | `[in](CHARACTERGUID)_Character, [out](INTEGER)_Level` |
| `CharacterGetHitpoints` | Gets a character's current HP | `[in](CHARACTERGUID)_Character, [out](INTEGER)_HP` |
| `CharacterGetMaxHitpoints` | Gets a character's maximum HP | `[in](CHARACTERGUID)_Character, [out](INTEGER)_MaxHP` |
| `CharacterGetHitpointsPercentage` | Gets HP as percentage | `[in](CHARACTERGUID)_Character, [out](INTEGER)_HPPercentage` |
| `CharacterGetStat` | Gets a character's stat value | `[in](CHARACTERGUID)_Character, [in](STRING)_StatName, [out](INTEGER)_Value` |
| `CharacterGetAbility` | Gets ability score value | `[in](CHARACTERGUID)_Character, [in](STRING)_Ability, [out](INTEGER)_Value` |
| `CharacterIsDead` | Checks if character is dead | `[in](CHARACTERGUID)_Character, [out](INTEGER)_IsDead` |
| `HasActiveStatus` | Checks for active status | `[in](GUIDSTRING)_Object, [in](STRING)_Status, [out](INTEGER)_HasStatus` |

### Position and Distance Queries

| Query | Description | Parameters |
|-------|-------------|------------|
| `GetPosition` | Gets position as string | `[in](GUIDSTRING)_Object, [out](STRING)_Position` |
| `GetDistanceTo` | Gets distance between objects | `[in](GUIDSTRING)_Object1, [in](GUIDSTRING)_Object2, [out](REAL)_Distance` |
| `GetX` | Gets X coordinate from position | `[in](STRING)_Position, [out](REAL)_X` |
| `GetY` | Gets Y coordinate from position | `[in](STRING)_Position, [out](REAL)_Y` |
| `GetZ` | Gets Z coordinate from position | `[in](STRING)_Position, [out](REAL)_Z` |

### Item-Related Queries

| Query | Description | Parameters |
|-------|-------------|------------|
| `IsInInventory` | Checks if item is in inventory | `[in](ITEMGUID)_Item, [out](INTEGER)_IsInInventory` |
| `GetItemOwner` | Gets owner of an item | `[in](ITEMGUID)_Item, [out](CHARACTERGUID)_Owner` |
| `GetTemplate` | Gets object's template | `[in](GUIDSTRING)_Object, [out](STRING)_Template` |
| `GetGold` | Gets character's gold amount | `[in](CHARACTERGUID)_Character, [out](INTEGER)_GoldAmount` |

### String and Math Queries

| Query | Description | Parameters |
|-------|-------------|------------|
| `Concatenate` | Combines strings | `[in](STRING)_String1, [in](STRING)_String2, [out](STRING)_Result` |
| `StringContains` | Checks if string contains substring | `[in](STRING)_String, [in](STRING)_SubString, [out](INTEGER)_Contains` |
| `IntegerSum` | Adds integers | `[in](INTEGER)_Value1, [in](INTEGER)_Value2, [out](INTEGER)_Sum` |
| `IntegerSubtract` | Subtracts integers | `[in](INTEGER)_Value1, [in](INTEGER)_Value2, [out](INTEGER)_Difference` |
| `IntegerProduct` | Multiplies integers | `[in](INTEGER)_Value1, [in](INTEGER)_Value2, [out](INTEGER)_Product` |
| `IntegerDivide` | Divides integers | `[in](INTEGER)_Value1, [in](INTEGER)_Value2, [out](INTEGER)_Quotient` |
| `GetRandomBetween` | Gets random integer in range | `[in](INTEGER)_Min, [in](INTEGER)_Max, [out](INTEGER)_Random` |

### Special Queries

| Query | Description | Parameters |
|-------|-------------|------------|
| `QRY_OnlyOnce` | Only returns true once per string | `[in](STRING)_UniqueString` |
| `QRY_OnlyOnce_Reset` | Resets OnlyOnce for a string | `[in](STRING)_UniqueString` |
| `IsTagged` | Checks if object has tag | `[in](GUIDSTRING)_Object, [in](STRING)_Tag, [out](INTEGER)_HasTag` |
| `IsInCombat` | Checks if character is in combat | `[in](CHARACTERGUID)_Character, [out](INTEGER)_IsInCombat` |

## Best Practices

1. **Efficient Variable Use**: When possible, directly check for the value you want rather than assigning and then comparing.

   ```
   // Less efficient
   IF
   CharacterGetHitpoints(_Player, _HP)
   AND
   _HP == 0
   THEN
   Action1;
   
   // More efficient
   IF
   CharacterGetHitpoints(_Player, 0)
   THEN
   Action1;
   ```

2. **Query Order**: Put queries that filter out more cases earlier in your rule.

3. **Error Handling**: Some queries may fail if given invalid inputs. Be defensive with your conditions.

4. **Custom Queries for Reusability**: Create custom queries for complex conditions that you use in multiple rules.

5. **QRY_OnlyOnce for Limited Execution**: Use `QRY_OnlyOnce` to ensure a rule only executes once.

## Example Usage

### Creating a Complex Condition

```
QRY
QRY_IsValidTarget((CHARACTERGUID)_Character)
AND
CharacterIsDead(_Character, 0) // Not dead
AND
IsInCombat(_Character, 1) // In combat
AND
HasActiveStatus(_Character, "CHARMED", 0) // Not charmed
THEN
DB_NOOP(1);

// Using the custom query
IF
DB_Players(_Player)
AND
QRY_IsValidTarget(_Player)
THEN
Action1;
```

### Calculating and Storing a Value

```
IF
CharacterGetHitpoints(_Player, _CurrentHP)
AND
CharacterGetMaxHitpoints(_Player, _MaxHP)
AND
IntegerProduct(_CurrentHP, 100, _HPTimes100)
AND
IntegerDivide(_HPTimes100, _MaxHP, _Percentage)
THEN
DB_PlayerHealthPercentage(_Player, _Percentage);
```

Queries are powerful tools for accessing game state information and making decisions based on it. By combining different queries, you can create complex conditions for your rules.
