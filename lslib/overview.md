# LSLib - Larian Studios Library

## Overview

LSLib is a comprehensive library and collection of tools for manipulating game files from Larian Studios games, including:

- Divinity: Original Sin 1
- Divinity: Original Sin Enhanced Edition
- Divinity: Original Sin 2
- Baldur's Gate 3

This toolkit provides utilities for various file operations including:

- Extracting and creating PAK packages
- Extracting and creating LSV savegame packages
- Converting between different resource formats (LSB, LSF, LSX, LSJ)
- Importing and exporting meshes and animations (conversion from/to GR2 format)
- Editing story (OSI) databases

## License

LSLib is licensed under the MIT License. See the LICENSE file for more details.

## Project Structure

### Core Components

#### LSLib

The core library containing all the file format handling functionality.

- **LSLib/LS**: Main namespace for Larian Studios file formats
  - **Resources**: Handlers for various resource formats (LSB, LSF, LSX, LSJ)
  - **Story**: Story (OSI) database handling
  - **Stats**: Game stats handling
  - **Save**: Save game file handling
  - **Mods**: Mod package handling

- **LSLib/Granny**: Handles GR2 file formats for models and animations
  - **GR2**: GR2 file format implementation
  - **Model**: Model data structures
  - **Collada**: Conversion between GR2 and Collada (DAE) formats

- **LSLib/VirtualTextures**: Texture handling functionality

#### Tools

##### Divine (Command Line Tool)

A command line interface (CLI) for all the LSLib functionality, allowing:

- Package extraction and creation
- Resource format conversion
- Model/mesh conversion
- Localization handling

##### ConverterApp (GUI Tool)

A graphical user interface providing access to:

- Package extraction and creation
- Resource conversion
- GR2 model/animation conversion
- Osiris story database viewing
- Localization file handling
- Virtual texture processing

##### Other Specialized Tools

- **PakReader**: Simple PAK package explorer
- **StatParser**: Game stat file parser
- **StoryCompiler/StoryDecompiler**: Tools for compiling/decompiling story files
- **VTexTool**: Virtual texture tool

## File Formats

### Package Formats

- **PAK**: Game package format containing bundled game files
- **LSV**: Savegame package format

### Resource Formats

- **LSB**: Binary resource format
- **LSF**: Binary resource format (different version)
- **LSX**: XML resource format
- **LSJ**: JSON resource format

### Other Formats

- **GR2**: Granny3D file format for models and animations
- **OSI**: Osiris story database format

## API Documentation

### Package Handling

#### PackageReader

Used to read PAK packages from files:

```csharp
var reader = new PackageReader();
using var package = reader.Read("game.pak");
```

#### PackageWriter

Used to create PAK packages:

```csharp
var build = new PackageBuildData
{
    Version = PackageVersion.V13,
    Compression = CompressionMethod.Zlib,
    CompressionLevel = LSCompressionLevel.DefaultCompression
};

// Add files to the package
build.Files.Add(PackageBuildInputFile.CreateFromFilesystem("local_file.txt", "package_path.txt"));

// Write the package
using var writer = PackageWriterFactory.Create(build, "output.pak");
writer.Write();
```

#### Packager

Higher-level package handling:

```csharp
var packager = new Packager();
packager.ProgressUpdate += (status, numerator, denominator) => {
    Console.WriteLine($"{status}: {numerator}/{denominator}");
};

// Extract a package
packager.UncompressPackage("game.pak", "output_dir/");

// Create a package
var build = new PackageBuildData {
    Version = PackageVersion.V13,
    Compression = CompressionMethod.Zlib
};
packager.CreatePackage("new_package.pak", "input_dir/", build);
```

### Resource Handling

LSLib supports converting between different resource formats:

#### ResourceUtils

```csharp
// Convert a resource file
ResourceUtils.Convert("input.lsf", "output.lsx", ResourceFormat.LSX);

// Load a resource
var resource = ResourceUtils.LoadResource("input.lsf");

// Save a resource
ResourceUtils.SaveResource(resource, "output.lsj", ResourceFormat.LSJ);
```

#### Resource Formats

Resource data can be converted between the following formats:

- **LSB**: Binary resource format
- **LSF**: Another binary resource format with different compression
- **LSX**: XML-based resource format (good for version control)
- **LSJ**: JSON-based resource format (good for scripted editing)

### Granny Model/Animation Handling

LSLib provides functionality to convert between the GR2 format used by the games and industry-standard Collada (.dae) format:

#### GR2Utils

```csharp
// Convert from GR2 to Collada
GR2Utils.ExportGR2("model.gr2", "model.dae");

// Convert from Collada to GR2
GR2Utils.ImportCollada("model.dae", "model.gr2");
```

#### Model Conversion Options

- Export/import skeletons
- Export/import meshes
- Export/import animations
- Conform to existing skeletons
- Generate normals/tangents/UVs

## Command Line Usage (Divine)

Divine provides command-line access to all LSLib functionality. 

For basic usage:

```
# Extract a package
Divine.exe extract-package --game bg3 --source "game.pak" --destination "output_dir/"

# Create a package
Divine.exe create-package --game bg3 --source "input_dir/" --destination "game.pak"

# Convert a resource
Divine.exe convert-resource --game bg3 --source "input.lsf" --destination "output.lsx"

# Convert a model
Divine.exe convert-model --game bg3 --source "model.gr2" --destination "model.dae"
```

For a comprehensive guide to all CLI features and options, see the [Divine CLI Guide](docs/cli-guide.md).

## GUI Usage (ConverterApp)

The ConverterApp provides a graphical interface with tabs for different functionality:

### Package Tab
- Extract packages
- Create packages
- Select files with filtering options

### Resource Tab
- Convert between resource formats
- Browse and select input/output files
- Set game version

### GR2 Tab
- Convert models and animations
- Import/export from GR2 format
- Set conversion options

### Osiris Tab
- View story databases
- Export story data

### Localization Tab
- Handle game localization files

## Building from Source

To build the tools, you need the following dependencies:

- GPLex 1.2.2: Extract to `External\gplex\`
- GPPG 1.5.2: Extract to `External\gppg\`
- Protocol Buffers 3.6.1: Extract to `External\protoc\`

Then open the `LSTools.sln` solution in Visual Studio and build it.

## Common Use Cases

### Modding Game Files

1. Extract the game package:
   ```
   Divine.exe extract-package --game bg3 --source "Game.pak" --destination "extracted/"
   ```

2. Convert files to a human-readable format:
   ```
   Divine.exe convert-resources --game bg3 --source "extracted/" --destination "editable/" --input-format LSB --output-format LSX
   ```

3. Make your changes to the XML files

4. Convert back to the game format:
   ```
   Divine.exe convert-resources --game bg3 --source "editable/" --destination "modified/" --input-format LSX --output-format LSB
   ```

5. Create a new mod package:
   ```
   Divine.exe create-package --game bg3 --source "modified/" --destination "MyMod.pak"
   ```

### Working with Models/Animations

1. Extract models from the game:
   ```
   Divine.exe extract-package --game bg3 --source "Game.pak" --destination "extracted/" --expression "*.gr2"
   ```

2. Convert to Collada format for editing:
   ```
   Divine.exe convert-model --game bg3 --source "extracted/model.gr2" --destination "model.dae"
   ```

3. Edit in 3D software (Blender, 3ds Max, etc.)

4. Convert back to GR2:
   ```
   Divine.exe convert-model --game bg3 --source "model.dae" --destination "modified/model.gr2"
   ```

5. Create a mod package with the modified models:
   ```
   Divine.exe create-package --game bg3 --source "modified/" --destination "ModelMod.pak"
   ```

## Version History

See the CHANGES.md file for a detailed version history. Some highlights:

- Added support for Baldur's Gate 3
- Improved GR2 import/export
- Added JSON (LSJ) format support
- Enhanced package handling
- Multiple bug fixes and optimizations

## Contributing

The LSLib repository is maintained on GitHub. Contributions can be made via pull requests.

## Troubleshooting

### Common Issues

1. **File format errors**: Ensure you're using the correct conversion formats for your game version.
2. **Model conversion issues**: Check that your Collada file follows the expected structure.
3. **Package extraction failures**: Verify that the package is not corrupted.

## Advanced Topics

### Custom Resource Processing

LSLib provides comprehensive APIs for programmatically manipulating game resources:

```csharp
// Load a resource
Resource resource = ResourceUtils.LoadResource("file.lsf");

// Manipulate nodes and attributes
foreach (var region in resource.Regions.Values)
{
    foreach (var child in region.Children["node_type"])
    {
        child.Attributes["attribute_name"] = new NodeAttribute(AttributeType.String) { Value = "new_value" };
    }
}

// Save the modified resource
ResourceUtils.SaveResource(resource, "modified.lsf", ResourceFormat.LSF);
```

### Working with Savegames

Savegames can be manipulated similarly to regular packages:

```csharp
// Extract a savegame
packager.UncompressPackage("save.lsv", "save_extracted/");

// Modify the files

// Create a new savegame
var build = new PackageBuildData {
    Version = PackageVersion.V10, // Savegame version
    Compression = CompressionMethod.Zlib
};
packager.CreatePackage("modified_save.lsv", "save_modified/", build);
```

## Final Notes

LSLib is an essential toolkit for modders and developers working with Larian Studios games. Its versatile API and command-line tools provide powerful capabilities for working with game assets, from simple package extraction to complex model conversion and resource manipulation.
