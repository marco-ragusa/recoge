# ReCoGe (Repo Context Generator)

ReCoGe is a Python-based script designed to convert a given repository path into a structured `<context>` XML tag, making it easily interpretable by a Large Language Model (LLM). The output includes a human-readable tree structure as well as a detailed XML representation of the directory structure and file contents.

## Features

- **Tree Generation**: Creates a text-based tree structure of the provided directory using visually intuitive connectors.
- **XML Representation**: Produces an XML tree structure with:
  - Directory and file names.
  - File contents encapsulated within XML tags.
  - Error handling for inaccessible files, annotated as comments in the XML output.
- **Extensibility**: The use of XML ensures a clear and structured output that is easy to parse programmatically.

## Requirements

- Python 3.6 or higher.

## Usage

### Command Syntax

```bash
python recoge.py <directory> [output_file]
```

### Parameters

- `<directory>`: The path to the directory you want to analyze.
- `[output_file]`: Optional. The name of the output file. Defaults to `output.xml`.

### Example

To generate the XML representation for the directory `./my_project` and save it to `output.xml`:

```bash
python recoge.py ./my_project output.xml
```

## Output Format

The script produces an XML file with the following structure:

### `<context>` Root Tag

Encapsulates all output, including:
- A `tree` section enclosed in `<![CDATA[]]>` for a readable directory tree.
- A `fileTree` section containing a detailed XML representation of the directory.

### Example Output

```xml
<context>
  <tree><![CDATA[
├── README.md
└── app.py
  ]]></tree>
  <fileTree>
    <directory name="my_project">
      <file name="README.md">
        <content>
          # My Project
          A simple Python project.
        </content>
      </file>
      <file name="app.py">
        <content>
          def run():
              print("Application is running")
        </content>
      </file>
    </directory>
  </fileTree>
</context>
```

## Example LLM Prompt

The XML output can be used as context for an LLM to analyze the repository. Here's an example:

### Context and Prompt:

```text
<context>
  <tree><![CDATA[
├── README.md
└── app.py
  ]]></tree>
  <fileTree>
    <directory name="my_project">
      <file name="README.md">
        <content>
          # My Project
          A simple Python project.
        </content>
      </file>
      <file name="app.py">
        <content>
          def run():
              print("Application is running")
        </content>
      </file>
    </directory>
  </fileTree>
</context>

Analyze the above repository structure and explain its purpose and how it might function.
```

### Expected LLM Response:

- The repository appears to be a simple Python project.
- The `README.md` file provides a brief description of the project.
- The `app.py` file contains a single function `run` that prints a message indicating the application is running.
- This suggests that the repository is a minimal starting point for a Python application, possibly for demonstration or as a template for further development.

## How It Works

1. **Tree Generation**:
   - The `generate_tree` function recursively traverses the directory structure.
   - Constructs a readable tree with `├──`, `└──`, and `│` connectors.
2. **XML Generation**:
   - The `generate_tree_xml` function produces a detailed XML representation.
   - Escapes special XML characters using `xml.sax.saxutils.escape`.
   - Reads file contents line-by-line and embeds them in `<content>` tags.
   - Handles exceptions (e.g., permission errors) gracefully, logging them in comments.

## Error Handling

- Invalid directory paths will terminate execution with an error message.
- Files that cannot be read due to permission issues or other errors are annotated with comments in the XML output.

## Why XML?

XML was chosen for its:

- **Hierarchical Structure**: Ideal for representing nested directories and files.
- **Readability**: Tags make it clear what each part of the structure represents.
- **Machine Interpretability**: XML can be easily parsed and consumed by LLMs or other tools.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests on the repository. Improvements such as additional output formats or enhanced error handling are welcome.
