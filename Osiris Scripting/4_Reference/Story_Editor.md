# Using the Story Editor

The Story Editor is the primary tool for creating and editing Osiris scripts in Baldur's Gate 3. This guide covers how to use the Story Editor effectively, including building and debugging your scripts.

## Opening the Story Editor

In the Editor's main toolbar, click on the book icon to open the Story Editor. Alternatively, if the viewport is selected, you can use the keyboard shortcut `Ctrl+X`.

![Story Editor Button](https://example.com/storyeditor_button.png)

## Story Editor Interface

The Story Editor is divided into several panels:

1. **Goal Hierarchy Panel (Left)**: Shows all goals in the game, organized in a hierarchical structure
2. **Script Editor Panel (Right)**: Contains three sections:
   - **INIT**: For initialization code
   - **KB**: For knowledge base rules
   - **EXIT**: For cleanup code
3. **Error Panel (Bottom)**: Shows errors and warnings during compilation

![Story Editor Interface](https://example.com/storyeditor_interface.png)

## Creating a New Script

To create a new script:

1. Find the appropriate parent goal in the hierarchy panel
2. Right-click on the parent goal and select **Add New Sub Item**
3. In the **New Script** dialog, select your mod project and name the script

### Goal Naming Convention

When creating new goals for BG3, it's recommended to follow the `Act_Region_Situation` naming convention. For example:
- `Act3b_LOW_Applesnatcher` - For a quest in Act 3b, Lower City, involving an "Applesnatcher"

## Building and Reloading Scripts

### Generate Definitions, Build and Reload

This is the most comprehensive option for building your script:

1. Press `Ctrl+F7` or select **Generate Definitions, Build and Reload** from the menu
2. This will:
   - Generate definitions for autocomplete
   - Build your script
   - Reload the story in the editor

### Advanced Build Options

- **Build**: Compiles your script so the game can read and evaluate it
- **Reload Story**: Reloads all goal files and executes their INIT sections in the Editor
- **Generate Definitions**: Updates definitions for autocomplete without building

### Reloading in the Game

There are two ways to reload your script in the game:

#### Option 1: Reload Level and Story
- Press `Ctrl+F8` or select **Reload Level and Story** from the menu
- This reloads both your script and all objects in the current level
- Useful when testing changes to objects, but takes longer

#### Option 2: Reload Story Only
- Press `F8` or select **Reload Story** from the Story Editor
- Only reloads the scripts, not the level objects
- Faster than reloading the entire level

## Common Build Errors and Warnings

### 1. Conflict with function definition

This occurs when a variable is used with different types. For example:

```
IF
FlagSet(_Player, "SOME_FLAG") // _Player is GUIDSTRING
AND
DB_Players(_Player) // DB_Players expects CHARACTER type
```

**Fix**: Cast the variable to the expected type:

```
IF
FlagSet(_Player, "SOME_FLAG")
AND
DB_Players((CHARACTER)_Player) // Cast to CHARACTER type
```

### 2. Database checked but never defined

This error appears when you reference a database in a condition but never define any facts for it.

**Fix**: Either define the database or remove the reference.

### 3. Parameter X is an unbound variable

This occurs when you use a variable that hasn't been assigned a value:

```
IF
StatusRemoved(_Player, "STATUS_SLEEPING")
AND
IsOnStage(_Character, 1) // _Character is not defined anywhere
```

**Fix**: Use the correct variable name:

```
IF
StatusRemoved(_Player, "STATUS_SLEEPING")
AND
IsOnStage(_Player, 1) // Use _Player which is defined above
```

### 4. Auto-define Osiris query failed: type of parameter X unknown

This error occurs when you try to check a database for more values than it contains:

```
DB_BuffedPlayers(_Player); // Defines a single-column database

IF
DB_BuffedPlayers(_Player, _Duration) // Trying to get two columns from a single-column database
```

**Fix**: Make sure the database has the right number of columns for your query.

### 5. Could not find any complete/correct definition of Osiris User Query/Procedure

This happens when you use a query or procedure that doesn't exist or with the wrong number of parameters:

```
IF
DB_Players(_Player)
AND
IsOnStage(_Player, 1, _Level) // IsOnStage only takes 2 parameters
```

**Fix**: Check the definition of the query or procedure and use the correct number of parameters.

### 6. Conflict with function definition: parameter X type mismatch

This occurs when you pass the wrong type to a query or procedure:

```
IF
DB_Players(_Player)
AND
IsOnStage(1, _Player) // First parameter should be GUIDSTRING, not INTEGER
```

**Fix**: Use the correct parameter types.

## Debugging with the Osiris Log

The Osiris Log contains a trace of all Osiris activity, making it invaluable for debugging.

### Opening the Osiris Log

You can open the Osiris Log from the Story Editor via **File** > **Open Story Log**, or find it in your Baldur's Gate 3 Toolkit installation folder as `osirislog.[date_of_creation].log`.

### Understanding the Log

The Osiris Log includes:

- **Events**: Lines starting with `>>> event` for game events
- **Queries**: Lines with `exec [DIV/Osi user query]` for query execution
- **Procedures**: Lines ending with `[Osiris procedure call]` for procedure calls
- **Database Operations**: Entries and removals from databases

### Debugging Tips

1. **Nested Execution**: Lines with `X---->` show the nesting level of execution. The larger the number, the deeper the nesting.
2. **Failed Queries**: Failed queries will show `*** Query Failed! ***` at the end of the line.
3. **Sequential Execution**: The log shows exactly what happens and in what order, making it easier to track down issues.
4. **Limited History**: The editor keeps the last 11 log files, so don't worry about losing logs when you reload.

## Debugging Functions

Osiris provides several debugging functions to help you trace script execution:

### DebugText

Displays text over a character's head:

```
IF
DB_Players(_Player)
THEN
DebugText(_Player, "This is a debug message");
```

### TextEvent

Simulates an event that can trigger other rules:

```
IF
DB_Players(_Player)
THEN
TextEvent("my_debug_event");
```

Then you can have a rule triggered by this event:

```
IF
TextEvent("my_debug_event")
THEN
// Debug code here
```

## Best Practices

1. **Use descriptive names**: Choose clear, descriptive names for your goals, databases, and variables.
2. **Comment your code**: Add comments to explain complex logic and the purpose of rules.
3. **Test incrementally**: Build and test small pieces of functionality before moving on.
4. **Watch the Osiris Log**: Regularly check the log to understand what's happening.
5. **Optimize for performance**: Be mindful of rules that might generate many evaluations.
