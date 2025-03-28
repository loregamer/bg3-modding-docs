# Introduction to Osiris

Osiris is a mostly declarative programming language used in Larian Studios' games, including Baldur's Gate 3. It's similar to Prolog in some ways and is used to script game behaviors, quests, and interactions.

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

## Key Concepts

- **Databases**: Tables that store facts (similar to database tables)
- **Rules**: If-then statements that trigger actions when conditions are met
- **Events**: Notifications from the game engine about things happening
- **Queries**: Ways to get information from the game
- **Calls**: Ways to change the game state

## When to Use Osiris

Osiris is particularly useful for:

1. **Event-driven behavior**: Making things happen in response to player actions or game events
2. **Quest logic**: Managing quest states, objectives, and rewards
3. **Complex game state management**: Tracking relationships between game entities
4. **World interactions**: Creating dynamic interactions between NPCs and the environment

## Next Steps

Now that you have a basic understanding of what Osiris is, continue to the [Program Structure](Program_Structure.md) section to learn how Osiris programs are organized.
