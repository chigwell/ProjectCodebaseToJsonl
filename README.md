[![PyPI version](https://badge.fury.io/py/ProjectCodebaseToJsonl.svg)](https://badge.fury.io/py/ProjectCodebaseToJsonl)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/ProjectCodebaseToJsonl)](https://pepy.tech/project/ProjectCodebaseToJsonl)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# ProjectCodebaseToJsonl

`ProjectCodebaseToJsonl` is a Python package designed to convert project codebases into JSONL format. This is particularly useful for preparing data for training GPT models, as it allows for the easy transformation of existing project structures and code into a format compatible with machine learning pipelines.

## Installation

To install `ProjectCodebaseToJsonl`, you can use pip:

```bash
pip install ProjectCodebaseToJsonl
```

## Usage

### As a Python Module

You can use `ProjectCodebaseToJsonl` as a module in your Python scripts.

Example:

```python
from codebase_to_jsonl import generate_jsonl_for_project

# Generate JSONL for a project
project_data = generate_jsonl_for_project(
    project_path="path_to_your_project",
    project_name="YourProjectName",
    use_gitignore=True,
    validation_ratio=0.4
)

print("Project Data Generated:")
print(project_data)
```

### Customizing Your Generator

You can customize the behavior of `ProjectCodebaseToJsonl` by adjusting parameters like `use_gitignore` and `validation_ratio` to suit the specific needs of your codebase and desired dataset characteristics.

## Output Example

Running `ProjectCodebaseToJsonl` generates JSONL files for both training and validation, structured to facilitate GPT model training. Here's an example of the output structure:

```
{
    "project_name": "YourProjectName",
    "token_count": 12345,
    "training_file": "YourProjectName_training_20240101_123456.jsonl",
    "validation_file": "YourProjectName_validation_20240101_123456.jsonl"
}
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/chigwell/ProjectCodebaseToJsonl/issues).

## License

[MIT](https://choosealicense.com/licenses/mit/)
