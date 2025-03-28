# Osiris Design Patterns

This section covers common design patterns that are useful when programming in Osiris. These patterns solve recurring problems and help structure your code more effectively.

## Program Initialization

There are several ways to initialize Osiris code, each with their own use cases. A safe and common pattern is:

1. Make global helper functionality goals top-level, activated as soon as Osiris initializes
2. Create one goal per level that completes when the level starts
3. Create subgoals for specific quests within each level

### Direct Dependencies

If you call procedures from your INIT code, ensure they're defined in goals that are already initialized:

```
// Goal: _AAA_Helper (initializes first due to alphabetical order)
PROC
PROC_InitializeGame()
THEN
// Setup code

// Goal: ZZZ_MainQuest (initializes after _AAA_Helper)
INIT
    PROC_InitializeGame(); // Safe, because _AAA_Helper initializes first
```

### Indirect Dependencies

Be careful when your code depends on database facts from other goals:

```
// In your goal
INIT
    DB_ShovelArea(_Trigger, _Reward, _DirtMound);

// In Shared mod's __GLO_Shovel goal
IF
DB_ShovelArea((TRIGGERGUID)_Trigger, (STRING)_Reward, (ITEMGUID)_DirtMound)
THEN
// Setup code
```

This only works if the `__GLO_Shovel` goal has already been initialized when your goal defines `DB_ShovelArea`.

## Doing Something Once

### Goal-Based Initialization

Use subgoals for one-time initialization. When the parent goal completes, the subgoal initializes and runs its INIT section:

```
// Parent goal
IF
RegionStarted(_Level)
THEN
GoalCompleted; // Initializes all subgoals

// Subgoal
INIT
    // One-time initialization code
```

### Breaking off a Loop

Often you need to iterate a database to find an entry that meets certain conditions, but only want to process the first match:

```
PROC
PROC_FindFirstChicken()
AND
DB_Chickens(_Chicken, _Dialog, _Ad, 0, _Trigger)
AND
CharacterIsDead((CHARACTERGUID)_Chicken, 0)
AND
NOT DB_DoneOnce(1)
THEN
DB_DoneOnce(1);
// Process the first living chicken

// Important: Reset the flag for next call
PROC
PROC_FindFirstChicken()
THEN
NOT DB_DoneOnce(1);
```

The `NOT DB_DoneOnce(1)` check must be the last condition in the sequence to ensure it properly stops iteration.

### QueryOnlyOnce

The Shared mod provides a useful helper query for executing something only once:

```
IF
SomeEvent(_Param)
AND
QueryOnlyOnce("UniqueID_ForThisEvent")
THEN
// This will only execute once per game for this specific UniqueID
```

The query only succeeds if it hasn't been called with that unique ID before.

## Trigger On Deleting a Database Fact

You can't directly trigger on a database fact being deleted, but you can use a helper database:

```
// When a fact is added
IF
DB_EnableCrime(_Player, _Crime)
THEN
DB_CrimeEnabled(_Player, _Crime);
EnableCrime(_Player, _Crime);

// When a fact is removed
IF
DB_CrimeEnabled(_Player, _Crime)
AND
NOT DB_EnableCrime(_Player, _Crime)
THEN
NOT DB_CrimeEnabled(_Player, _Crime);
DisableCrime(_Player, _Crime);
```

## Check Whether a Database Is Empty

To check if a database has no entries:

```
IF
SomeEvent(_Param)
AND
NOT DB_Check(_, _)
THEN
// This will only execute if DB_Check is empty
```

You can't specify variable names in this case, as they would have nothing to bind to.

## Factoring Out Checks to Queries

Queries are excellent for separating search logic from processing:

```
// Query to find the first matching item
QRY
QRY_FindFirstItem()
AND
DB_Items(_Item, _Owner)
AND
ItemGetStat(_Item, "Value", _Value)
AND
_Value > 100
AND
NOT DB_FoundExpensiveItem(_)
THEN
DB_FoundExpensiveItem(_Item);

// Procedure to process the results
PROC
PROC_ProcessExpensiveItems()
AND
QRY_FindFirstItem()
AND
DB_FoundExpensiveItem(_Item)
THEN
NOT DB_FoundExpensiveItem(_Item);
// Process the expensive item
```

This pattern is useful when you need to look up several independent things and want to keep the search logic separate from the processing logic.

## Implementing OR Conditions

Since Osiris only supports AND in rule conditions, use queries to implement OR logic:

```
QRY
QRY_IsVulnerable((CHARACTERGUID)_Char)
AND
HasActiveStatus(_Char, "STUNNED", 1)
THEN
DB_NOOP(1);

QRY
QRY_IsVulnerable(_Char)
AND
HasActiveStatus(_Char, "KNOCKED_DOWN", 1)
THEN
DB_NOOP(1);

IF
CharacterDamaged(_Char, _)
AND
QRY_IsVulnerable(_Char)
THEN
// This executes if the character is EITHER stunned OR knocked down
```

## Advanced Database Usage

### Temporary Result Sets

For complex operations, use temporary databases to store intermediate results:

```
// Step 1: Find all characters matching a condition
PROC
PROC_ProcessEnemies((CHARACTERGUID)_Player)
AND
DB_Characters(_Character)
AND
CharacterIsEnemy(_Character, _Player, 1)
THEN
DB_TempEnemies(_Character);

// Step 2: Process the results
PROC
PROC_ProcessEnemies(_Player)
AND
DB_TempEnemies(_Enemy)
THEN
// Process each enemy
NOT DB_TempEnemies(_Enemy); // Clean up
```

## Best Practices Summary

1. **Initialization Order**: Be aware of goal initialization order when designing dependencies.

2. **Single Responsibility**: Break complex logic into smaller, focused rules and subroutines.

3. **Managing State**: Use databases to track state, but clean them up when no longer needed.

4. **Temporary Databases**: Use temporary databases for intermediate results, but remember to clean them up.

5. **Rule Order Awareness**: Be conscious of rule execution order, especially for rules that depend on each other.

## Next Steps

Continue to the [Common Gotchas](Gotchas.md) section to learn about common pitfalls and how to avoid them.
