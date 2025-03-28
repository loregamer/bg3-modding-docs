# Working with the Story Editor

The Story Editor is the primary tool for creating, editing, and building Osiris scripts in Baldur's Gate 3.

![Story Editor](https://docs.larian.game/images/8/8d/StoryEditor.png)

## Editor Interface

The Story Editor consists of several panes:

1. **Goal Tree** (left pane): Shows the hierarchical structure of goals in your mod
2. **Goal Editing Panes** (right panes): INIT, KB (Knowledge Base), and EXIT sections
3. **Code Editor**: For writing and editing Osiris code
4. **Status Bar**: Shows compilation status and other information

## Building the Story

To build your Osiris scripts, the Story Editor provides several options under the "File" menu:

### Build Options

1. **Generate Definitions, Build and Reload**
   - The most thorough option
   - Recreates all function definitions
   - Builds the story
   - Reloads the story so your changes take effect immediately
   - Use this when you've made significant changes

2. **Build**
   - Only builds the story without regenerating definitions
   - Sufficient for checking errors when no function definitions have changed
   - Faster than a full build with definition generation

3. **Build and Reload**
   - Builds the story and reloads it
   - Use when you've made changes and want to see them in the editor

4. **Generate Definitions and Build**
   - Recreates definitions and builds the story
   - Does not reload the story
   - Required for the first story build after an editor update

5. **Generate Definitions**
   - Only generates function definitions
   - Useful to get code completion without rebuilding the story

## Code Editing Helper Functionality

The Story Editor provides several features to help you write code:

### Code Completion

Press `Ctrl+Space` to access code completion. This helps you:

- Find API functions
- Complete database names
- See parameter types

**Note**: For user-defined queries, code completion may add a wrong "__DEF" suffix that you'll need to delete.

### Parameter Information

When you're within a function call's parameter list, the editor shows parameter definitions at the top of the code editing window. This helps you understand:

- Parameter names
- Parameter types
- Parameter order

**Note**: The parameter list shown will always be for the last defined overload in the Story, so other definitions with more parameters may exist.

### Global Search

Press `Ctrl+Shift+F` to open the global search dialog. This allows you to search across all story files, which is useful for:

- Finding examples of API usage
- Locating specific databases or rules
- Understanding how existing code works

## Working with Goals

Goals are the main organizational unit in Osiris:

### Creating Goals

1. Right-click on a goal in the tree to create a new subgoal
2. Give it a descriptive name
3. Goals become active when their parent completes

### Editing Goals

Each goal has three sections:

1. **INIT**: Actions executed when the goal initializes
2. **KB**: Rules that are active while the goal is active
3. **EXIT**: Actions executed when the goal completes

### Organizing Goals

Follow these best practices:

1. Use a hierarchical structure that matches your game's structure
2. Name goals descriptively
3. Use alphabetical ordering to control execution order when needed
4. Create separate goals for different features or quests

## Known Limitations

The Story Editor has a few limitations to be aware of:

1. **Find Dialog Box**: Each pane has its own "Find" dialog (Ctrl+F). If you press Ctrl+F while a "Find" dialog is already open, it won't regain focus. Either close the dialog after searching or click on it to regain focus.

2. **Parameter List Display**: The parameter list shown at the top of the window only shows the last defined overload of a function. Other overloads with different parameters may exist.

3. **Performance with Large Files**: The editor can be slower when working with very large story files. Consider breaking your code into smaller, more manageable goals.

## Debugging Tips

The Story Editor doesn't have a traditional debugger, but you can use these techniques:

1. **Temporary Databases**: Create temporary databases to log values
   ```
   DB_Debug_Value(_Variable);
   ```

2. **Status Text**: Use `CharacterStatusText` to display messages in-game
   ```
   CharacterStatusText(_Character, "Debug: Value is [1]", _Value);
   ```

3. **Console Commands**: Some debug commands can be entered in the console, like:
   ```
   AddDebugText("Debug message");
   ```

4. **Incremental Development**: Build and test small pieces of functionality before combining them

## Best Practices

1. **Regular Builds**: Build your story regularly to catch errors early

2. **Consistent Naming**: Use consistent naming conventions for:
   - Goals
   - Databases
   - Queries and procedures

3. **Comments**: Add comments to explain complex logic
   ```
   // This rule handles the special case where...
   ```

4. **Structure**: Organize your goals in a logical hierarchy

5. **Modularity**: Create reusable queries and procedures instead of duplicating code

## Next Steps

Now that you understand the basics of Osiris scripting and how to use the Story Editor, start experimenting with creating your own scripts.

Remember that learning Osiris is a process, and you'll get better with practice. Don't hesitate to look at examples from the main game or ask for help on the [Larian Forums](http://larian.com/forums/ubbthreads.php?ubb=postlist&Board=77&page=1).
