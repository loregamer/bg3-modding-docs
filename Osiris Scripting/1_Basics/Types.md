# Types in Osiris

Osiris supports several data types that can be used in databases, variables, and parameters.

## Basic Types

Osiris supports the following basic types:

### INTEGER

A 32-bit integer number.

Examples:
```
-4, 0, 10
```

### INTEGER64

A 64-bit integer number, used for larger values.

Examples:
```
-99999999999, -4, 0, 10, 12345678901
```

### REAL

A single precision floating point number.

Examples:
```
-10.0, -0.1, 0.0, 0.5, 100.123
```

### STRING

A character string.

Examples:
```
"A", "ABC", "_This is a string_"
```

## GUID Types

Osiris also supports several GUID types to reference objects in the game:

### GUIDSTRING

A base GUID type that refers to an object or root template in the game. This object can be any of the specialized GUID types below.

Examples:
```
123e4567-e89b-12d3-a456-426655440000
MyObjectName_123e4567-e89b-12d3-a456-426655440000
CHARACTERGUID_MyObjectName_123e4567-e89b-12d3-a456-426655440000
```

Osiris only uses the GUID itself. Anything before it (as long as it does not contain "-") is ignored by the compiler and is only there to improve code readability. This ensures that renaming an object in the game won't break related scripts.

### Specialized GUID Types

All of these inherit from GUIDSTRING and can be used when you need to specifically reference a particular type of object:

- **CHARACTERGUID**: References a character object
- **ITEMGUID**: References an item object
- **TRIGGERGUID**: References a trigger object
- **SPLINEGUID**: References a spline object
- **LEVELTEMPLATEGUID**: References a level template object

## Type Casting

You can cast a GUIDSTRING to any of the specific types by adding the type name in parentheses:

```
(CHARACTERGUID)123e4567-e89b-12d3-a456-426655440000
(ITEMGUID)MyItem_123e4567-e89b-12d3-a456-426655440000
```

## Type Rules and Best Practices

1. **Automatic Prefix**: The code completion in the Story Editor will prepend the object type to the object name (e.g., `ITEMGUID_`), but this does not define or change the type for the Osiris compiler.

2. **First Declaration Rule**: The compiler uses the first occurrence of a database to determine the types of its columns. It will then typecast values in any further occurrences to match this type.

   ```
   // First declaration - defines column types (CHARACTERGUID, STRING)
   DB_Origins((CHARACTERGUID)CHARACTERGUID_S_Player_Ifan_123, "IFAN");
   
   // Later declarations - the first column will be cast to CHARACTERGUID automatically
   DB_Origins(CHARACTERGUID_S_Player_Beast_456, "BEAST");
   ```

3. **Naming Convention**: When referring to objects/local instances, follow the correct naming convention. Prefix names with the appropriate type (e.g., `CHARACTERGUID_`, `ITEMGUID_`) for better readability.

4. **Comparison**: GUIDSTRING and its descendent types can only be compared for equality (`==`) and inequality (`!=`), while the other types can also be compared with `<`, `<=`, `>`, and `>=`.

## Next Steps

Continue to the [Databases](Databases.md) section to learn how to store and manipulate data in Osiris.
