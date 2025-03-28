# Osiris Events

Events are notifications from the game engine about things happening in the game. They are used as trigger conditions in Osiris rules, always appearing as the first condition.

## Using Events

Events must always be the first condition in a rule. They have parameters that provide information about what happened.

Example:
```
IF
CharacterDied(_Character) // Event with parameter
AND
DB_IsPlayer(_Character) // Additional condition
THEN
DB_PlayerDied(_Character); // Action
```

You can use constants in event parameters to filter specific cases:
```
IF
AddedTo(_Object, S_Player_Laezel_58a69333-40bf-8358-1d17-fff240d7fb12, _)
THEN
// Only triggers when Lae'zel receives an item
```

## Event Parameters

Each event has specific parameters that provide information about what happened. For example, the `AddedTo` event has parameters for the object added, who received it, and how it was added.

You can find the details for events in the official list:
- [Mod.io Osiris Events](https://mod.io/g/baldursgate3/r/osiris-events)
- [GitHub Osiris Events](https://github.com/LaughingLeader/BG3ModdingTools/blob/master/generated/Osi.Events.lua)

## Common Events in BG3

Here are some commonly used events in Baldur's Gate 3:

### Character-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `CharacterCreationFinished` | Triggered when character creation is completed | `(CHARACTERGUID)_Character` |
| `CharacterDied` | Triggered when a character dies | `(CHARACTERGUID)_Character` |
| `CharacterJoinedParty` | Triggered when a character joins the party | `(CHARACTERGUID)_Character` |
| `CharacterLeftParty` | Triggered when a character leaves the party | `(CHARACTERGUID)_Character` |
| `StatusApplied` | Triggered when a status is applied to a character | `(CHARACTERGUID)_Character, (STRING)_Status, (INTEGER)_WasApplied` |
| `StatusRemoved` | Triggered when a status is removed from a character | `(CHARACTERGUID)_Character, (STRING)_Status, (INTEGER)_WasRemoved` |

### Item-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `AddedTo` | Triggered when an item is added to an inventory | `(GUIDSTRING)_Object, (GUIDSTRING)_InventoryHolder, (STRING)_AddType` |
| `ItemDestroyed` | Triggered when an item is destroyed | `(ITEMGUID)_Item` |
| `ItemEquipped` | Triggered when an item is equipped | `(CHARACTERGUID)_Character, (ITEMGUID)_Item` |
| `ItemUnequipped` | Triggered when an item is unequipped | `(CHARACTERGUID)_Character, (ITEMGUID)_Item` |

### Game-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `GameModeStarted` | Triggered when a game mode starts | `(STRING)_Mode` |
| `GameModeEnded` | Triggered when a game mode ends | `(STRING)_Mode` |
| `TextEvent` | Custom event fired through TextEvent action | `(STRING)_EventName` |
| `FlagSet` | Triggered when a flag is set | `(GUIDSTRING)_Object, (STRING)_FlagName` |
| `FlagCleared` | Triggered when a flag is cleared | `(GUIDSTRING)_Object, (STRING)_FlagName` |

### Combat-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `CombatStarted` | Triggered when combat begins | `(GUIDSTRING)_CombatGuid` |
| `CombatEnded` | Triggered when combat ends | `(GUIDSTRING)_CombatGuid` |
| `TurnStarted` | Triggered when a character's turn starts | `(CHARACTERGUID)_Character` |
| `TurnEnded` | Triggered when a character's turn ends | `(CHARACTERGUID)_Character` |

### Rest-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `ShortRestStarted` | Triggered when a short rest begins | `_` |
| `ShortRestFinished` | Triggered when a short rest completes | `_` |
| `LongRestStarted` | Triggered when a long rest begins | `_` |
| `LongRestFinished` | Triggered when a long rest completes | `_` |

### Dialog-Related Events

| Event | Description | Parameters |
|-------|-------------|------------|
| `DialogStarted` | Triggered when a dialog starts | `(GUIDSTRING)_Dialog, (CHARACTERGUID)_Speaker, (CHARACTERGUID)_Listener` |
| `DialogEnded` | Triggered when a dialog ends | `(GUIDSTRING)_Dialog, (CHARACTERGUID)_Speaker, (CHARACTERGUID)_Listener` |

## Best Practices

1. **Use the Right Event**: Choose the event that most specifically matches what you're looking to respond to.

2. **Filter Parameters**: When possible, use constants in event parameters to focus on specific scenarios rather than filtering with additional conditions.

3. **Consider Performance**: Events that trigger frequently (like StatusApplied) should have efficient rules to prevent performance issues.

4. **TextEvent for Debugging**: Use the `TextEvent` event with custom strings for debugging your scripts.

## Example Usage

### Responding to a Character Death

```
IF
CharacterDied(_Character)
AND
DB_IsPlayer(_Character)
THEN
DB_PlayerDied(_Character);
PlayEffectAtPosition("RS3_FX_UI_Icon_Negative_01", GetPosition(_Character));
```

### Custom Event Handling

```
IF
DB_Players(_Player)
AND
CharacterGetLevel(_Player, _Level)
AND
_Level >= 5
THEN
TextEvent("PlayerReachedLevel5");

// Respond to the custom event
IF
TextEvent("PlayerReachedLevel5")
THEN
DB_HighLevelPlayersExist(1);
```

Remember that events are the entry points to your Osiris logic. Choosing the right events and handling them efficiently is key to creating responsive and performance-friendly mods.
