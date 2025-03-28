# Program Execution in Osiris

Understanding how Osiris programs execute is crucial for writing effective scripts. This section covers the execution model, rule matching, frames, and other important execution concepts.

## Event-Driven Execution

Osiris execution is completely event-driven:

- Rules are only triggered when an event occurs or when a database is modified
- Subroutines (queries and procedures) can only be called from action blocks
- There is no "main" function or entry point

This means that your Osiris code primarily reacts to game events and player actions rather than executing in a linear sequence.

## Goal Initialization and Completion

As mentioned in the [Program Structure](Program_Structure.md) section:

1. When a goal initializes:
   - Its INIT section executes
   - Rules in its KB section become active
   - Its queries and procedures become available

2. When a goal completes (via `GoalCompleted;`):
   - All its subgoals initialize
   - Its EXIT section executes
   - Its rules, queries, and procedures become inactive
   - Databases set in the goal remain active unless deleted

### Initialization Order

Goals are initialized in alphabetical order by goal name, regardless of their parent-child relationships or mod dependencies. This has important implications:

- A goal named `AAA_FirstGoal` will initialize before `ZZZ_LastGoal`
- Top-level goals initialize when the mod loads
- Subgoals initialize when their parent goal completes

## Rule Order

Rules are evaluated in the order they appear in the merged story, from top to bottom:

1. Goals are ordered alphabetically by name
2. Rules within goals are ordered as they appear in the files
3. When a trigger occurs, all matching rules execute in this defined order

This means that if you have rules that depend on each other, you need to ensure they're in the correct order.

## Rule Matching

### Rule Evaluation State

When a rule's conditions are being evaluated:

1. Osiris generates a temporary internal table of valid possibilities for each condition
2. It iterates through this table to find all combinations that fulfill the conditions
3. For each valid combination, it executes the actions

This means that removing a database fact in an action won't prevent subsequent matches from being processed, as the rule is already working with a snapshot of the state when it started evaluating.

### Rule Trigger Evaluation

When a trigger condition occurs:

1. Osiris collects all rules with matching first trigger conditions
2. It executes these rules one by one with the matched parameters
3. Removing the trigger condition in an action won't prevent other rules from executing

### Iterating Database Contents

You can use variables to iterate through all entries in a database:

```
IF
DB_Players(_Player, _Level)
THEN
// This executes once for each entry in DB_Players
```

### Looking Up Specific Facts

You can use fixed values to look up specific database entries:

```
IF
DB_Players("John", _Level)
THEN
// This executes only for the entry with name "John"
```

## Osiris Frames

Osiris execution is organized into **frames**:

- A frame is an atomic unit of rule evaluations and actions
- Everything in a single frame happens atomically (can't be interrupted)
- Players cannot save during a frame execution
- Either a frame completes entirely, or it doesn't start at all

When an event triggers multiple rules, all of those rules (and any subroutines they call) execute in the same frame.

## Frame Delays

Actions don't always take effect immediately, even within the same frame:

### Dialog Frame Delays

A common example is flag visibility in dialogs:

1. **Frame 1**: A flag is set in an Osiris action
2. **Frame 2**: The dialog system loads the next nodes and evaluates conditions
3. **Frame 3**: The node with the condition checking for the flag is shown

To handle this, you need to add a "frame delay node" between setting a flag and checking it:

```
// In a dialog:
1. Player chooses option that sets MYPRE_give_item flag
2. Empty "frame delay" node with no text
3. Next node checks for MYPRE_got_item flag
```

The empty node ensures that the flag set in Frame 1 is visible when checking it in Frame 3.

## Best Practices

1. **Goal Naming**:
   - Use alphabetical ordering to your advantage
   - Prefix important initialization goals with underscores to ensure they run first

2. **Rule Dependencies**:
   - Be aware of rule execution order when one rule depends on another
   - Don't rely on side effects of one rule in another unless you're sure of the order

3. **Frame Awareness**:
   - Remember that databases modified in the current frame are immediately visible to subsequent rules
   - But some game state changes (like dialog flags) may only be visible in the next frame

4. **Database Cleanup**:
   - Clean up temporary databases in the EXIT section of goals
   - This improves performance and reduces savegame size

## Next Steps

Continue to the [Design Patterns](Design_Patterns.md) section to learn about common design patterns used in Osiris scripting.
