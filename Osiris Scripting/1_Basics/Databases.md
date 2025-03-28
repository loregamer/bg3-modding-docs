# Databases in Osiris

In Osiris, databases are similar to tables in a relational database. They store facts (rows) with typed columns.

## What are Databases?

Databases are used to store data that will be manipulated later. Every database name should begin with `DB_` and the name itself should be unique for **every goal in every mod**.

Databases in Osiris are more like tables in an actual database. To store data, we need to add a row to the desired DB. Adding a row is often referred to as **defining a fact**.

## Database Naming

Database names must start with `DB_` and should be followed by a prefix that is unique to your mod or goal. This is important because there is only one namespace across all mods, so all database names must be globally unique.

Good examples of database naming:
- `DB_MyMod_Players` - For a list of players in your mod
- `DB_MyQuest_Progress` - For tracking quest progress
- `DB_MySystem_Settings` - For storing system settings

## Database Structure

The structure of a database fact definition is:

```
DB_Prefix_DatabaseName(TypedValue1[, TypedValue2...]);
```

Each entry that gets added to a database is called a **fact**.

## Examples

### Single Column Database

```
// Type: String
DB_Overview_StringDB("SomeString");
DB_Overview_StringDB("AnotherString");
```

### Multiple Column Database

```
// Type: Integer, String
DB_Overview_IntegerStringDB(0, "String0");
DB_Overview_IntegerStringDB(1, "String1");
```

### Using GUIDs

```
// Type: CHARACTERGUID, String
DB_Overview_Origins((CHARACTERGUID)CHARACTERGUID_S_Player_Ifan_ad9a3327-4456-42a7-9bf4-7ad60cc9e54f, "IFAN");
DB_Overview_Origins(CHARACTERGUID_S_Player_Beast_f25ca124-a4d2-427b-af62-df66df41a978, "BEAST");
```

## Database Overloading

You can have multiple databases with the same name as long as they have a different number of columns:

```
// Single column database (Type: GUIDSTRING)
DB_Overview_Origins(CHARACTERGUID_S_Player_Ifan_ad9a3327-4456-42a7-9bf4-7ad60cc9e54f);

// Two-column database (Type: CHARACTERGUID, String)
DB_Overview_Origins((CHARACTERGUID)CHARACTERGUID_S_Player_Ifan_ad9a3327-4456-42a7-9bf4-7ad60cc9e54f, "IFAN");
```

However, it will not work to reuse a database name for one that has the same number of parameters but with different types or in a different order.

## Database Type Determination

The compiler uses the first occurrence of a database to determine the types of its columns. It will then typecast values in any further occurrences to match these types.

```
// First occurrence - sets column types
DB_Overview_Origins((CHARACTERGUID)CHARACTERGUID_S_Player_Ifan_ad9a3327-4456-42a7-9bf4-7ad60cc9e54f, "IFAN");

// Later occurrences - typecast to match first occurrence
DB_Overview_Origins(CHARACTERGUID_S_Player_Beast_f25ca124-a4d2-427b-af62-df66df41a978, "BEAST");
```

This is an important rule to keep in mind, as it's a frequent source of type errors for beginners.

## Removing Database Facts

You can remove facts from a database using the `NOT` operator:

```
NOT DB_Overview_StringDB("SomeString");
```

This removes the specific fact from the database. It won't cause an error if the fact doesn't exist; it will simply be ignored.

## Checking if a Fact Exists

To check if a fact exists in a database, you can use the database name directly in a condition:

```
IF
DB_Overview_StringDB("SomeString") // This condition evaluates to true if the fact exists
THEN
// Do something
```

You can also use variables to match any fact in the database:

```
IF
DB_Overview_StringDB(_String) // This will match any fact in the database
THEN
// Do something with _String
```

## Database as Global State

Databases in Osiris effectively function as global state storage. They persist until explicitly removed and can be accessed from any goal in your mod (or other mods that depend on yours).

This makes databases useful for:

1. **Storing Quest States**: Track the progress of quests and player choices
2. **Managing Game Objects**: Keep track of important characters, items, or locations
3. **Caching Calculations**: Store results of complex calculations that would be expensive to repeat
4. **Cross-Goal Communication**: Share information between different goals

## Database Best Practices

1. **Unique Naming**: Always use a mod-specific prefix after `DB_` to avoid naming conflicts.

2. **Cleanup**: Remove databases when they're no longer needed to reduce savegame size.

   ```
   EXIT
       NOT DB_Overview_StringDB("SomeString");
       NOT DB_Overview_StringDB("AnotherString");
   ```

3. **Type Consistency**: Be careful with column types. Define the types explicitly in the first occurrence of a database.

4. **Naming Conventions**: Follow consistent naming conventions to make your code more readable.

5. **Use Simple Types When Possible**: Where possible, use simple types like INTEGER and STRING for better performance.

## Next Steps

Continue to the [Rules](Rules.md) section to learn how to create rules that react to database changes and game events.
