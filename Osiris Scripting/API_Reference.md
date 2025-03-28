# Osiris API Reference

Osiris provides a large set of APIs that allow you to interact with the game world. These APIs are categorized into three main types:

1. **Events**: Notifications from the game engine about things that happen
2. **Queries**: Ways to get information about the current game state
3. **Calls**: Ways to change the game state

## How to Find API Declarations

The Osiris API documentation is a work in progress. To see all available APIs:

1. Open the Story Editor
2. Generate definitions (File -> Generate Definitions)
3. Open the Story Header (File -> Open Story Header)

You can also find this file at: `.\Data\Mods\<mod name>\Story\RawFiles\story_header.div`

## Looking Up API Usage Examples

To find examples of how to use a specific API:

1. Create an Adventure Add-on mod that depends on DivinityOrigins
2. Build the story for that mod
3. In the Story Editor, press Ctrl+Shift+F and search for the API name
4. The results will show you all places where that API is used in the game

You can also examine the story.div file at: `.\Data\Mods\<mod name>\Story\RawFiles\story.div`

## API Categories

### Events

Events are used as trigger conditions in rules. They notify your script that something has happened in the game.

**Key Points about Events**:
- Must be the first condition in a rule
- Cannot be called directly from your code
- Are triggered by the game engine

**Common Events**:

| Event | Description |
|-------|-------------|
| `CharacterCreated` | A character has been created |
| `CharacterDied` | A character has died |
| `ItemAddedToCharacter` | An item has been added to a character's inventory |
| `DialogStarted` | A dialog has started |
| `GameStarted` | The game has started |
| `RegionStarted` | A level/region has started |

### Queries

Queries allow you to get information about the game state without changing it.

**Key Points about Queries**:
- Used in rule conditions to check the state of the game
- Return boolean results (success/failure)
- Can bind output variables with values
- Never trigger automatically

**Common Queries**:

| Query | Description |
|-------|-------------|
| `CharacterGetLevel` | Get a character's level |
| `CharacterIsDead` | Check if a character is dead |
| `CharacterIsEnemy` | Check if a character is an enemy of another |
| `ItemGetStat` | Get a statistic from an item |
| `ObjectExists` | Check if an object exists |
| `CharacterIsInPartyWith` | Check if a character is in a party with another |

### Calls

Calls allow you to change the game state.

**Key Points about Calls**:
- Used in action blocks to modify the game state
- Do not return results directly (though their effects can be queried later)
- Can create, modify, or destroy game objects

**Common Calls**:

| Call | Description |
|------|-------------|
| `CharacterHeal` | Heal a character |
| `CharacterDie` | Kill a character |
| `CharacterMoveTo` | Move a character to a position |
| `ItemCreate` | Create a new item |
| `CharacterGiveQuestReward` | Give a quest reward to a character |
| `CharacterPlayAnimation` | Play an animation on a character |

## Shared Mod Helpers

The Shared mod provides many useful helper routines and databases that you can use in your mods.

**Common Helpers**:

| Helper | Description |
|--------|-------------|
| `QueryOnlyOnce` | Execute something only once per unique ID |
| `DB_DialogNPCs` | Database of NPCs in dialog |
| `DB_Dialogs` | Database of dialog mappings |
| `DB_GLO_Traders` | Database of traders in the game |
| `DB_Origins` | Database of origin characters |

## Best Practices for Using APIs

1. **Check the Documentation**: Always check if an API is documented before using it
2. **Look at Examples**: Find examples of the API being used in the game's scripts
3. **Test Thoroughly**: Test your usage of APIs in different scenarios
4. **Type Safety**: Be careful with parameter types, especially with GUID types
5. **Error Handling**: Handle cases where queries might fail

## API Usage Examples

### Event Example

```
IF
CharacterDied(_Character) // Event trigger
AND
DB_IsPlayer(_Character)
THEN
DB_PlayerDied(_Character);
```

### Query Example

```
IF
DB_CheckLevel(_Character)
AND
CharacterGetLevel(_Character, _Level) // Query to get character level
AND
_Level >= 5
THEN
DB_HighLevelCharacter(_Character);
```

### Call Example

```
IF
DB_HealCharacter(_Character)
THEN
CharacterHeal(_Character, 100); // Call to heal the character
```

## Finding Undocumented APIs

If you can't find documentation for an API:

1. Search for usage examples in the game's scripts
2. Look at the parameter types in the story_header.div file
3. Test the API in a controlled environment
4. Ask on the [Scripting Forum](http://larian.com/forums/ubbthreads.php?ubb=postlist&Board=77&page=1)

## Next Steps

Continue to the [Working with the Story Editor](Story_Editor.md) section to learn how to use the Story Editor effectively for writing and testing Osiris scripts.
