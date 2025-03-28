# Introduction to Osiris

Osiris is a mostly declarative programming language used in Larian Studios' games, including Baldur's Gate 3. It's similar to Prolog in some ways and is used to script game behaviors, quests, and interactions.

## What is Osiris for?

Osiris' responsibility is to handle the global world and game states, and the transitions between these states. **Osiris has a higher priority over other scripting languages used in the Editor.** This means that Osiris calls have a guaranteed execution if the target of this call is valid.

> Note that the validity of the target is defined by different conditions, specific to the Call you're using. For example, you cannot request a character to move using `CharacterMoveTo` if this character is dead.

## What is Declarative Programming?

Unlike imperative programming languages (like C#, Python, or JavaScript) where you specify exactly *how* to do something with sequences of commands, declarative programming focuses on *what* you want to achieve. You describe the conditions and results rather than the step-by-step process.

If you're familiar with SQL or logic programming, you'll find some similarities with Osiris. Instead of writing sequences of commands, you write rules that automatically trigger when specific conditions are met.

## How Osiris Works

In Osiris, you can think of your program as a collection of rules that operate on a single, game-wide database. The rules dynamically add and remove tables and rows in reaction to:

1. Other database entries being modified
2. Game state changes
3. Player actions
4. In-game events

Your rules can:
- React to events that happen in the game
- Query information about the current game state
- Change the game state

## Structure of an Osiris Program

An Osiris program is called a **Story**, and it consists of different **Goals**.

Every Goal in Osiris consists of three sections:

1. **INIT**: Contains actions that are executed when the goal initializes
2. **KB**: Contains rules that become active as soon as the goal starts initializing
3. **EXIT**: Contains actions that are executed when the goal completes

## Key Components

Here's a breakdown of the main components of Osiris:

1. **Events**: Notifications from the game engine about things happening (e.g., `CharacterDied`, `TextEvent`)
2. **Queries**: Ways to get information from the game (e.g., `CharacterGetLevel`, `CharacterGetHitpointsPercentage`)
3. **Calls**: Ways to change the game state (e.g., `CharacterHeal`, `AddGold`)
4. **Databases**: Tables that store facts (similar to database tables)
5. **Rules**: If-then statements that trigger actions when conditions are met
6. **Variables**: Names starting with underscore (_) that allow for generalization and data extraction

## A Simple Example

Here's a basic example of Osiris code:

```
INIT
    DB_MyPrefix_Fruit("Apple");     // Defines a database with one entry: "Apple"
    DB_MyPrefix_Fruit("Pear");      // Adds another entry: "Pear"
    DB_MyPrefix_Fruit("Banana");    // Adds another entry: "Banana"
KB
    IF                              // Rules always start with IF
    DB_MyPrefix_Fruit(_SomeFruit)   // This rule triggers when any fruit is added to the database
                                    // The name of the fruit is stored in the _SomeFruit variable
    THEN                            // THEN indicates the actions to perform
    DB_MyPrefix_FruitFound(1);      // We define another database and add a value

    IF
    DB_MyPrefix_Fruit("Pear")       // This rule triggers specifically when "Pear" is added
    AND
    NOT DB_MyPrefix_Fruit("Lemon")  // And only if "Lemon" doesn't exist in the database
    THEN
    DB_MyPrefix_PearNoLemon(1);     // Define another database entry

EXIT
    NOT DB_MyPrefix_Fruit("Apple"); // Remove the "Apple" entry when the goal completes
    NOT DB_MyPrefix_Fruit("Pear");  // Remove the "Pear" entry
    NOT DB_MyPrefix_Fruit("Banana"); // Remove the "Banana" entry
```

## Execution Order

Osiris execution is completely **event-driven**, which means that there are no main procedures at which a Story starts executing. It can be broken down into this:

1. Top-level Goals become available as soon as the mod is loaded and a story becomes active.
2. When the Goal becomes active, its **INIT** section gets executed.
3. **KB** section becomes active as soon as the goal starts initializing. Rules, queries and procedures defined in this Goal start getting executed.
   - The earliest event that Osiris can react to is `GameModeStarted`;
   - However, rules in **KB** section can still react to facts being added to a **DB** in **INIT** section of the same goal, even if the **INIT** is still being executed.
4. `GoalCompleted` is used for finalizing a Goal.
   - This will execute the **EXIT** section of the Goal and deactivate rules, queries, and procedures defined in this Goal.
   - Databases defined in the Goal will still be active after completing the Goal.
   - Sub-goals of the Goal will become active after this.
   - However, the action block (the whole **KB** section for example) where `GoalCompleted` was called will be executed until the end. So, you can add rules below `GoalCompleted` statement is called, and even reference procedures and queries inside sub-goals, as they become active after `GoalCompleted` is executed.

All Goals are merged into a single story file. Inside this file, all goals are sorted alphabetically. Rules are executed from top to bottom.

So, for example, if you want to use a database defined in another Goal, you need to make sure this Goal is located before any Goal you want to use this database in.

## When to Use Osiris

Osiris is particularly useful for:

1. **Event-driven behavior**: Making things happen in response to player actions or game events
2. **Quest logic**: Managing quest states, objectives, and rewards
3. **Complex game state management**: Tracking relationships between game entities
4. **World interactions**: Creating dynamic interactions between NPCs and the environment

## Next Steps

Now that you have a basic understanding of what Osiris is, continue to the [Program Structure](Program_Structure.md) section to learn more about how Osiris programs are organized.
