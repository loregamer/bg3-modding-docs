# Osiris Calls

Calls are functions that change the game state. They are used in the action section of Osiris rules to make things happen in the game.

## Using Calls

Calls are always used after the `THEN` keyword in rules. They require parameters that specify exactly what you want to do.

Example:
```
IF
LongRestFinished()
AND
DB_Players(_Player)
THEN
AddGold(_Player, 100); // Call with parameters
```

## Call Parameters

Each call has specific parameters that determine what it does. Parameters are values passed to the call that tell it what to act on and how.

For example, the `AddGold` call has parameters for who receives the gold and how much:
```
AddGold((GUIDSTRING)_Character, (INTEGER)_Amount)
```

You can find the details for calls in the official list:
- [Mod.io Osiris Calls](https://mod.io/g/baldursgate3/r/osiris-calls)
- [GitHub Osiris Calls](https://github.com/LaughingLeader/BG3ModdingTools/blob/master/generated/Osi.lua)

## Overloaded Calls

Some calls have alternate versions with fewer parameters. These are called **overloaded calls**. Omitted parameters default to specific values.

For example, the `Equip` call has multiple overloaded versions:
```
// Full version with all parameters
Equip((CHARACTER)_Character, (ITEM)_Item, (INTEGER)_AddToMainInventoryOnFail, (INTEGER)_ShowNotification, (INTEGER)_ClearOriginalOwner)

// Overloaded version with fewer parameters
Equip((CHARACTER)_Character, (ITEM)_Item)
```

When using the shorter version, omitted parameters will use default values.

Important notes about overloaded calls:
- You cannot change the order of parameters
- If you want to set a later parameter, you must provide all earlier ones
- The documentation may not list all overloaded versions

## Common Calls in BG3

Here are some commonly used calls in Baldur's Gate 3:

### Character-Related Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `CharacterResurrect` | Resurrects a dead character | `(CHARACTERGUID)_Character` |
| `CharacterHeal` | Heals a character | `(CHARACTERGUID)_Character, (INTEGER)_Amount` |
| `CharacterApplyStatus` | Applies a status effect | `(CHARACTERGUID)_Character, (STRING)_Status, (REAL)_Duration, (INTEGER)_Force` |
| `CharacterRemoveStatus` | Removes a status effect | `(CHARACTERGUID)_Character, (STRING)_Status` |
| `CharacterGiveExperience` | Gives experience points | `(CHARACTERGUID)_Character, (INTEGER)_Amount` |
| `CharacterMoveTo` | Moves a character to a position | `(CHARACTERGUID)_Character, (REAL)_X, (REAL)_Y, (REAL)_Z, (INTEGER)_Running, (INTEGER)_OffStage` |

### Item-Related Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `CreateItemAtPosition` | Creates an item at a position | `(REAL)_X, (REAL)_Y, (REAL)_Z, (STRING)_Template, (INTEGER)_Amount` |
| `CreateItemInInventory` | Creates an item in an inventory | `(GUIDSTRING)_Inventory, (STRING)_Template, (INTEGER)_Amount` |
| `AddGold` | Adds gold to a character | `(CHARACTERGUID)_Character, (INTEGER)_Amount` |
| `RemoveGold` | Removes gold from a character | `(CHARACTERGUID)_Character, (INTEGER)_Amount` |
| `ItemSetDeltaMod` | Adds a deltamod (modification) to an item | `(ITEMGUID)_Item, (STRING)_DeltaMod, (INTEGER)_IsGenerated` |

### UI and Game-Related Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `ShowNotification` | Shows a notification on screen | `(CHARACTERGUID)_Character, (STRING)_Text` |
| `OpenMessageBox` | Opens a message box | `(CHARACTERGUID)_Character, (STRING)_Text` |
| `TextEvent` | Fires a custom text event | `(STRING)_EventName` |
| `SetFlag` | Sets a flag on an object | `(GUIDSTRING)_Object, (STRING)_FlagName` |
| `ClearFlag` | Clears a flag from an object | `(GUIDSTRING)_Object, (STRING)_FlagName` |

### Combat-Related Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `StartCombat` | Starts combat between characters | `(CHARACTERGUID)_Character1, (CHARACTERGUID)_Character2` |
| `LeaveCombat` | Makes a character leave combat | `(CHARACTERGUID)_Character` |
| `FinishCombat` | Finishes the current combat | `(GUIDSTRING)_CombatGuid` |

### Dialog-Related Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `StartDialog` | Starts a dialog | `(CHARACTERGUID)_Character1, (CHARACTERGUID)_Character2, (STRING)_Dialog` |
| `EndDialog` | Ends the current dialog | `(GUIDSTRING)_Dialog` |

### Debug Calls

| Call | Description | Parameters |
|------|-------------|------------|
| `DebugText` | Shows text above an object | `(GUIDSTRING)_Object, (STRING)_Text` |
| `DebugBreak` | Forces a debugger breakpoint | |

## Best Practices

1. **Type Safety**: Make sure you pass the correct type of parameters to calls.

2. **Error Handling**: Calls will fail silently if given invalid parameters. Add defensive conditions when necessary.

3. **Overloaded Calls**: Be aware that using shorter versions of calls sets unspecified parameters to default values.

4. **Optimization**: Group related calls together for better performance and readability.

5. **Safety Checks**: For critical operations, check conditions thoroughly before making calls.

## Example Usage

### Creating a Healing Spell Effect

```
IF
CharacterUsedSkill(_Caster, "Target_FirstAid", _)
AND
SkillGetTarget(_Caster, _Target)
AND
CharacterGetHitpointsPercentage(_Target, _HP)
AND
_HP < 100
THEN
CharacterHeal(_Target, 10);
CharacterApplyStatus(_Target, "REGENERATION", 12.0, 0);
PlayEffectAtPosition("RS3_FX_GP_ScriptedEvent_Regenerate_01", GetPosition(_Target));
```

### Giving a Reward

```
IF
QuestRewardEvent("QUEST_Example")
AND
DB_Players(_Player)
THEN
AddGold(_Player, 500);
CreateItemInInventory(_Player, "LOOT_GEN_Ring_Ring_A_Magic_Fire_1", 1);
ShowNotification(_Player, "You have received a reward!");
```

Calls are the heart of making things happen in your mods. By understanding how to use them effectively, you can create all sorts of interesting effects and behaviors in the game.
