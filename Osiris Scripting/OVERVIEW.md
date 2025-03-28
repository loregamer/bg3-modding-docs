# Osiris Scripting Overview

This document provides a quick overview of Osiris scripting concepts for Baldur's Gate 3. For more detailed information on each topic, follow the links to the corresponding documents.

## What is Osiris?

Osiris is a declarative programming language used in Larian Studios' games, including Baldur's Gate 3. Unlike traditional programming languages where you specify exactly *how* to do something step-by-step, Osiris focuses on defining *what* conditions should trigger *what* actions.

Osiris has a higher priority over other scripting languages used in the Editor, meaning that Osiris calls have a guaranteed execution if the target of the call is valid.

[Read more about Osiris basics](1_Basics/Introduction.md)

## Key Concepts

### Program Structure

- **Story**: An Osiris program is called a Story and consists of all Goals from your mod and its dependencies
- **Goals**: Container units with three sections - INIT (initialization), KB (knowledge base/rules), and EXIT (cleanup)
- **Goals Hierarchy**: Goals can have subgoals that become active when the parent goal completes

[Read more about program structure](1_Basics/Program_Structure.md)

### Types

Osiris supports several data types:
- Basic types: INTEGER, INTEGER64, REAL, STRING
- GUID types: GUIDSTRING, CHARACTERGUID, ITEMGUID, TRIGGERGUID, etc.

[Read more about types](1_Basics/Types.md)

### Databases

- Databases store facts (similar to rows in a database table)
- Database names must start with `DB_` and should have a unique prefix
- Facts can be added and removed dynamically

```
DB_MyPrefix_Players("John", 10);
DB_MyPrefix_Players("Jane", 5);
```

[Read more about databases](1_Basics/Databases.md)

### Rules

Rules define what happens when certain conditions are met:

```
IF
CharacterDied(_Character)   // Trigger condition (must be first)
AND
DB_IsPlayer(_Character)     // Extra condition
THEN
DB_PlayerDied(_Character);  // Action
```

[Read more about rules](1_Basics/Rules.md)

### Variables

- Variables start with underscore (_) and are automatically typed
- They allow for generalization and data extraction
- Variable scope is limited to a single rule or subroutine

[Read more about variables](2_Intermediate/Variables.md)

### Subroutines

Osiris has two types of subroutines:

1. **Queries (QRY)**: Used to check conditions and implement OR-functionality
   ```
   QRY
   QRY_IsVulnerable((CHARACTERGUID)_Char)
   AND
   HasActiveStatus(_Char, "STUNNED", 1)
   THEN
   DB_NOOP(1);
   ```

2. **Procedures (PROC)**: Collections of actions with optional conditions
   ```
   PROC
   PROC_HealIfInjured((CHARACTERGUID)_Character)
   AND
   CharacterGetHitpointsPercentage(_Character, _HP)
   AND
   _HP < 100
   THEN
   CharacterHeal(_Character, 100);
   ```

[Read more about subroutines](2_Intermediate/Subroutines.md)

### Program Execution

- Osiris execution is event-driven
- Rules are evaluated when their trigger conditions are met
- Goals initialize in alphabetical order by name
- Execution happens in atomic "frames"

[Read more about program execution](2_Intermediate/Program_Execution.md)

## Advanced Topics

### Understanding Rules

- Learn how Osiris evaluates rules with variables
- Understand how database combinations work
- Optimize rule performance

[Read more about understanding rules](3_Advanced/Understanding_Rules.md)

### Design Patterns

Common design patterns in Osiris include:
- Program initialization patterns
- One-time execution patterns
- Triggering on database deletion
- Breaking off loops
- Implementing OR conditions with queries

[Read more about design patterns](3_Advanced/Design_Patterns.md)

### Common Gotchas

Things to watch out for:
- Result set explosion when combining multiple database queries
- Type casting issues with GUIDs
- Frame delays in dialogs
- Alphabetical goal ordering affecting execution

[Read more about common gotchas](3_Advanced/Gotchas.md)

## Reference

### Story Editor

The Story Editor is the primary tool for:
- Creating and editing Osiris scripts
- Building and reloading scripts
- Debugging and error handling

[Learn about the Story Editor](4_Reference/Story_Editor.md)

### API Reference

Osiris provides APIs in three categories:
- **Events**: Notifications from the game engine (e.g., `CharacterDied`)
- **Queries**: Get information about the game state (e.g., `CharacterGetLevel`)
- **Calls**: Change the game state (e.g., `CharacterHeal`)

[Osiris Events Reference](4_Reference/Osiris_Events.md)
[Osiris Queries Reference](4_Reference/Osiris_Queries.md)
[Osiris Calls Reference](4_Reference/Osiris_Calls.md)

## Recommended Learning Path

1. Start with basic concepts in the [1_Basics](1_Basics) folder:
   - [Introduction to Osiris](1_Basics/Introduction.md)
   - [Program Structure](1_Basics/Program_Structure.md)
   - [Types](1_Basics/Types.md)
   - [Databases](1_Basics/Databases.md)
   - [Rules](1_Basics/Rules.md)

2. Move on to intermediate topics in the [2_Intermediate](2_Intermediate) folder:
   - [Variables](2_Intermediate/Variables.md)
   - [Subroutines](2_Intermediate/Subroutines.md)
   - [Program Execution](2_Intermediate/Program_Execution.md)

3. Learn advanced patterns and gotchas in the [3_Advanced](3_Advanced) folder:
   - [Understanding Rules](3_Advanced/Understanding_Rules.md)
   - [Design Patterns](3_Advanced/Design_Patterns.md)
   - [Gotchas](3_Advanced/Gotchas.md)

4. Use the reference material in the [4_Reference](4_Reference) folder as needed:
   - [Story Editor](4_Reference/Story_Editor.md)
   - [Osiris Events](4_Reference/Osiris_Events.md)
   - [Osiris Queries](4_Reference/Osiris_Queries.md)
   - [Osiris Calls](4_Reference/Osiris_Calls.md)

Happy scripting!
