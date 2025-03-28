# Program Structure

An Osiris program is called a **Story**. A story consists of all **Goals** from the current mod and its dependencies.

## Goals

A goal is a plain text file with three sections:

1. **INIT**: Contains actions that are executed when the goal initializes
2. **KB**: Contains rules that become active as soon as the goal starts initializing
3. **EXIT**: Contains actions that are executed when the goal completes

### Goal Structure

In the Story Editor, these sections are represented by separate panes when you open a goal for editing. You do not type the `INIT`, `KB`, and `EXIT` keywords in the editor.

```
INIT
    // Actions executed when the goal initializes
    // You can define databases, set initial states, etc.
    DB_ExampleDatabase("Value1");
    DB_ExampleDatabase("Value2");

KB
    // Rules that are active while the goal is active
    IF
    DB_ExampleDatabase(_Value)
    THEN
    DB_ProcessedValue(_Value);

EXIT
    // Actions executed when the goal completes
    // Often used to clean up databases to reduce savegame size
    NOT DB_ExampleDatabase("Value1");
    NOT DB_ExampleDatabase("Value2");
```

### Goal Hierarchy

Goals can have subgoals, creating a hierarchical structure. The general pattern is:

1. **Top-level goals**: Contain global helper functionality and are activated as soon as Osiris is initialized
2. **Level-specific goals**: One main goal per level that completes when the level starts
3. **Quest-specific goals**: Subgoals of level goals, handling specific quest logic

## Goal Initialization and Completion

- **Initialization**: When a goal becomes active, its INIT section executes and its rules become active
- **Completion**: When a goal completes:
  - All its subgoals are initialized
  - Its EXIT section is executed
  - None of its rules, queries, or procedures remain active
  - Databases defined in the goal remain active unless explicitly deleted

### Goal Completion

A goal is completed by executing the `GoalCompleted;` action in any action block. For example:

```
IF
SomeCondition(_Param)
THEN
GoalCompleted; // This completes the current goal
```

After the `GoalCompleted;` statement, the current action block will still finish executing, so you can put additional actions after it.

## Mod Dependencies and Story Compilation

When a mod depends on other mods, the story includes goals from all of those mods. For example, if your mod depends on the Shared mod, your story will include all goals from both your mod and the Shared mod.

Goals from all mods are merged into a single story, and the rules are evaluated from top to bottom in alphabetical order by goal name, regardless of parent/subgoal relationships or mod dependencies.

## Rule Execution Order

Rules are executed in alphabetical order based on goal name. This is important when you have rules that depend on databases defined by other rules. If you need a rule to execute after another, ensure the goal name comes later alphabetically.

For example, a goal named `_AAA_FirstGoal` in the Shared mod will execute before any goal that starts with a letter. Many modders use underscores (`_`) to control the execution order of their goals, as underscores are sorted before any letter or number.

## Next Steps

Continue to the [Types](Types.md) section to learn about the data types available in Osiris.
