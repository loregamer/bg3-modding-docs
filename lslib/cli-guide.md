# LSLib Divine Command Line Interface (CLI) Guide

This document provides a comprehensive guide to using the LSLib Divine Command Line Interface (CLI) tool for manipulating game files from Larian Studios games.

## Table of Contents

- [Installation](#installation)
- [Basic Syntax](#basic-syntax)
- [Global Options](#global-options)
- [Package Operations](#package-operations)
  - [Extracting Packages](#extracting-packages)
  - [Creating Packages](#creating-packages)
  - [Listing Package Contents](#listing-package-contents)
  - [Extracting Single Files](#extracting-single-files)
  - [Batch Extracting Packages](#batch-extracting-packages)
- [Resource Conversion](#resource-conversion)
  - [Converting Single Resources](#converting-single-resources)
  - [Batch Converting Resources](#batch-converting-resources)
  - [Localization Conversion](#localization-conversion)
- [Model/Animation Operations](#modelanimation-operations)
  - [Converting GR2/DAE Models](#converting-gr2dae-models)
  - [Batch Converting Models](#batch-converting-models)
  - [Model Conversion Options](#model-conversion-options)
- [Advanced Usage](#advanced-usage)
  - [Filtering Package Contents](#filtering-package-contents)
  - [Working with Specific Game Versions](#working-with-specific-game-versions)
  - [Using Regular Expressions](#using-regular-expressions)
  - [Compression Settings](#compression-settings)
  - [Encryption Settings](#encryption-settings)
- [Example Workflows](#example-workflows)
  - [Creating a Mod](#creating-a-mod)
  - [Extracting and Editing Models](#extracting-and-editing-models)
  - [Converting Savegames](#converting-savegames)
- [Troubleshooting](#troubleshooting)
  - [Common Errors](#common-errors)
  - [Log Levels](#log-levels)

## Installation

Divine is included in the LSLib package. To use it:

1. Build the LSLib solution or download a pre-built release
2. Navigate to the directory containing `Divine.exe`
3. Run Divine commands using a command prompt or terminal

## Basic Syntax

Divine commands follow this general syntax:

```
Divine.exe --action <action> --game <game> --source <source_path> [--destination <destination_path>] [other options]
```

- `--action` or `-a`: The operation to perform (extract-package, create-package, convert-resource, etc.)
- `--game` or `-g`: Target game (dos, dosee, dos2, dos2de, bg3)
- `--source` or `-s`: Source file or directory path
- `--destination` or `-d`: Destination file or directory path (optional for some actions)

## Global Options

These options apply to most Divine commands:

| Option | Short | Description | Values | Default |
|--------|-------|-------------|--------|---------|
| `--game` | `-g` | Target game | dos, dosee, dos2, dos2de, bg3 | (required) |
| `--source` | `-s` | Source path | file/directory path | (required) |
| `--destination` | `-d` | Destination path | file/directory path | (often required) |
| `--loglevel` | `-l` | Logging verbosity | off, fatal, error, warn, info, debug, trace, all | info |
| `--action` | `-a` | Action to perform | (see below) | extract-package |
| `--expression` | `-x` | Filter expression | glob/regex pattern | * |
| `--use-regex` | | Use regex for filtering | true/false | false |
| `--legacy-guids` | | Use legacy GUID format | true/false | false |
| `--use-package-name` | | Use package name for destination | true/false | false |
| `--encryption-method` | | Set encryption method | none, aes128, aes256, xor | none |
| `--encryption-key` | | Set encryption key/password | any string | (none) |

## Package Operations

### Extracting Packages

Extract the contents of a package (.pak or .lsv) file:

```
Divine.exe --action extract-package --game bg3 --source "Game.pak" --destination "extracted_files/"
```

### Creating Packages

Create a new package (.pak or .lsv) file from a directory:

```
Divine.exe --action create-package --game bg3 --source "mod_files/" --destination "MyMod.pak" --compression-method zlib
```

Compression method options:
- `zlib`: Standard Zlib compression (good balance of size/speed)
- `zlibfast`: Faster Zlib compression (worse compression ratio)
- `lz4`: Fast LZ4 compression (fast, lower compression)
- `lz4hc`: LZ4 high compression (slower, better compression)
- `none`: No compression

Note: The package priority can be set with `--package-priority <value>` (default: 0)

### Listing Package Contents

List the contents of a package without extracting:

```
Divine.exe --action list-package --game bg3 --source "Game.pak"
```

This displays filename, size, and CRC for each file in the package.

### Extracting Single Files

Extract one specific file from a package:

```
Divine.exe --action extract-single-file --game bg3 --source "Game.pak" --destination "extracted_file.lsf" --packaged-path "Mods/ModName/meta.lsx"
```

### Batch Extracting Packages

Extract multiple packages at once:

```
Divine.exe --action extract-packages --game bg3 --source "packages_directory/" --destination "extracted_files/" --input-format pak
```

## Resource Conversion

### Converting Single Resources

Convert between resource formats (LSB, LSF, LSX, LSJ):

```
Divine.exe --action convert-resource --game bg3 --source "file.lsf" --destination "file.lsx"
```

The input and output formats are determined by the file extensions.

### Batch Converting Resources

Convert multiple resources at once:

```
Divine.exe --action convert-resources --game bg3 --source "resources_directory/" --destination "converted_directory/" --input-format lsf --output-format lsx
```

### Localization Conversion

Convert localization files:

```
Divine.exe --action convert-loca --game bg3 --source "English.loca" --destination "English.xml"
```

## Model/Animation Operations

### Converting GR2/DAE Models

Convert between GR2 (game format) and DAE (Collada) formats:

```
Divine.exe --action convert-model --game bg3 --source "model.gr2" --destination "model.dae"
```

### Batch Converting Models

Convert multiple models at once:

```
Divine.exe --action convert-models --game bg3 --source "models_directory/" --destination "converted_models/" --input-format gr2 --output-format dae
```

### Model Conversion Options

Model conversion can be customized with the `--gr2-options` (or `-e`) parameter:

```
Divine.exe --action convert-model --game bg3 --source "model.gr2" --destination "model.dae" --gr2-options export-normals,export-tangents,export-uvs
```

Available options:
- `export-normals`: Export normal vectors (default: true)
- `export-tangents`: Export tangent vectors (default: true)
- `export-uvs`: Export UV coordinates (default: true)
- `export-colors`: Export vertex colors (default: true)
- `deduplicate-vertices`: Remove duplicate vertices (default: true)
- `flip-uvs`: Flip UV coordinates vertically (default: true)
- `ignore-uv-nan`: Ignore NaN values in UV coordinates (default: true)
- `disable-qtangents`: Disable quaternion tangents (default: false)
- `y-up-skeletons`: Use Y-up coordinate system for skeletons (default: true)
- `force-legacy-version`: Use legacy GR2 format version (default: false)
- `compact-tris`: Optimize triangle indices (default: true)
- `build-dummy-skeleton`: Build skeleton if missing (default: true)
- `apply-basis-transforms`: Apply basis transformations (default: true)
- `x-flip-skeletons`: Flip skeletons along X axis (default: false)
- `x-flip-meshes`: Flip meshes along X axis (default: false)
- `conform`: Conform to original skeleton (requires --conform-path) (default: false)
- `conform-copy`: Copy bones from conform skeleton (default: false)

For the `conform` option, specify the path to the reference skeleton:

```
Divine.exe --action convert-model --game bg3 --source "animation.dae" --destination "animation.gr2" --gr2-options conform --conform-path "original_model.gr2"
```

## Advanced Usage

### Filtering Package Contents

You can filter package contents using glob patterns or regular expressions:

```
# Extract only LSF files using glob pattern
Divine.exe --action extract-package --game bg3 --source "Game.pak" --destination "extracted/" --expression "*.lsf"

# Extract files using regex pattern (with --use-regex)
Divine.exe --action extract-package --game bg3 --source "Game.pak" --destination "extracted/" --expression "Public/ModName/.*\.lsx" --use-regex
```

### Working with Specific Game Versions

Specify the target game version with the `--game` parameter:

- `dos`: Divinity: Original Sin
- `dosee`: Divinity: Original Sin Enhanced Edition
- `dos2`: Divinity: Original Sin 2
- `dos2de`: Divinity: Original Sin 2 Definitive Edition
- `bg3`: Baldur's Gate 3

```
Divine.exe --action extract-package --game dos2de --source "Game.pak" --destination "extracted/"
```

### Using Regular Expressions

For more complex filtering, use regular expressions with the `--use-regex` flag:

```
Divine.exe --action list-package --game bg3 --source "Game.pak" --expression "Public/SharedDev/.*_(A|B)\.lsf" --use-regex
```

### Compression Settings

Control package compression with the `--compression-method` parameter:

```
Divine.exe --action create-package --game bg3 --source "mod_files/" --destination "MyMod.pak" --compression-method lz4hc
```

### Encryption Settings

Secure your package files with encryption (BG3/V18 only):

```
# Create with encryption
Divine.exe --action create-package --game bg3 --source "mod_files/" --destination "MyMod.pak" --encryption-method aes256 --encryption-key "my_secure_password"

# Extract encrypted package
Divine.exe --action extract-package --game bg3 --source "encrypted.pak" --destination "extracted/" --encryption-key "my_secure_password"
```

Available encryption methods:
- `none`: No encryption (default)
- `aes128`: AES encryption with 128-bit key
- `aes256`: AES encryption with 256-bit key (strongest)
- `xor`: Simple XOR-based encryption (lightweight)

**Important notes:**
- Encryption is only available for BG3 packages (version 18+)
- The same key must be used for extraction as was used for creation
- There is no way to recover a lost encryption key

## Example Workflows

### Creating a Mod

1. Extract relevant game files:
   ```
   Divine.exe --action extract-package --game bg3 --source "Game.pak" --destination "extracted/" --expression "Public/Game/GUI/Portraits/*"
   ```

2. Convert binary files to editable XML:
   ```
   Divine.exe --action convert-resources --game bg3 --source "extracted/" --destination "editable/" --input-format lsf --output-format lsx
   ```

3. [Edit the XML files]

4. Convert back to game format:
   ```
   Divine.exe --action convert-resources --game bg3 --source "editable/" --destination "mod/" --input-format lsx --output-format lsf
   ```

5. Create a mod package:
   ```
   Divine.exe --action create-package --game bg3 --source "mod/" --destination "MyPortraitMod.pak"
   ```
   
   For a secured mod with encrypted content:
   ```
   Divine.exe --action create-package --game bg3 --source "mod/" --destination "MySecureMod.pak" --encryption-method aes256 --encryption-key "my_secure_password"
   ```

### Extracting and Editing Models

1. Extract models from game:
   ```
   Divine.exe --action extract-package --game bg3 --source "Game.pak" --destination "extracted/" --expression "*.gr2"
   ```

2. Convert to Collada format for editing:
   ```
   Divine.exe --action convert-model --game bg3 --source "extracted/model.gr2" --destination "model.dae"
   ```

3. [Edit in 3D software like Blender]

4. Convert back to GR2:
   ```
   Divine.exe convert-model --game bg3 --source "model.dae" --destination "modified/model.gr2"
   ```

5. Create mod package:
   ```
   Divine.exe create-package --game bg3 --source "modified/" --destination "ModelMod.pak"
   ```

### Converting Savegames

1. Extract a savegame:
   ```
   Divine.exe extract-package --game bg3 --source "savegame.lsv" --destination "extracted_save/"
   ```

2. Convert save files to editable format:
   ```
   Divine.exe convert-resources --game bg3 --source "extracted_save/" --destination "editable_save/" --input-format lsf --output-format lsx
   ```

3. [Edit the save files]

4. Convert back to game format:
   ```
   Divine.exe convert-resources --game bg3 --source "editable_save/" --destination "modified_save/" --input-format lsx --output-format lsf
   ```

5. Create a new savegame:
   ```
   Divine.exe create-package --game bg3 --source "modified_save/" --destination "modified_savegame.lsv" --compression-method zlib
   ```

## Troubleshooting

### Common Errors

1. **"Cannot parse path from input"** - Ensure paths are valid and absolute
2. **"Failed to extract package because the package is not an Original Sin package"** - Verify the file is a valid package
3. **"Unknown game"** - Specify a valid game parameter (dos, dosee, dos2, dos2de, bg3)
4. **"Unknown resource format"** - Use a valid format for resource conversion
5. **"Failed to convert resource"** - Check file formats and permissions
6. **"Invalid encryption key provided"** - The provided key doesn't match the one used to encrypt the package
7. **"Encryption is only supported for package version V18"** - Only BG3 packages support encryption

### Log Levels

Use different log levels for troubleshooting:

```
Divine.exe extract-package --game bg3 --source "Game.pak" --destination "extracted/" --loglevel debug
```

Log levels from least to most verbose:
- `off`: No logging
- `fatal`: Only fatal errors
- `error`: Errors and fatal errors
- `warn`: Warnings and above
- `info`: General information (default)
- `debug`: Detailed debugging information
- `trace`: Extremely detailed tracing
- `all`: All possible logging
