import os
import json
import pathspec
from datetime import datetime
import random

def generate_jsonl_for_project(project_path, project_name, use_gitignore=True, validation_ratio=0.4):
    jsonl_data = []
    validation_questions = []
    unique_lines = {}
    token_count = 0
    spec = None

    if use_gitignore:
        spec = load_gitignore(project_path)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            if spec and spec.match_file(file_path):
                continue

            content = get_file_content(file_path)
            relative_file_path = os.path.relpath(file_path, project_path)
            jsonl_data.append(generate_source_code_entry(relative_file_path, content, project_name))
            token_count += len(tokenize(content))

            # Find unique lines for validation
            update_unique_lines(unique_lines, content, relative_file_path)


    # Generate validation questions based on unique lines
    validation_questions = generate_validation_questions(unique_lines, validation_ratio, project_name)


    # get 10 percent of the validation questions and add them to the training data
    additional_training_q = validation_questions[:int(len(validation_questions) * 0.1)]
    jsonl_data.extend(additional_training_q)
    # delete additional_training_q from validation_questions
    validation_questions = validation_questions[int(len(validation_questions) * 0.1):]

    # Add project structure question to training data
    project_structure_question = generate_project_structure_question(project_name, get_project_structure(project_path, spec))
    jsonl_data.append(project_structure_question)

    # Writing data to files
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_jsonl_files(jsonl_data, validation_questions, project_name, current_datetime)

    return {
        "project_name": project_name,
        "token_count": token_count,
        "training_file": f'{project_name}_training_{current_datetime}.jsonl',
        "validation_file": f'{project_name}_validation_{current_datetime}.jsonl'
    }

def generate_additional_training_questions(unique_lines, validation_questions):
    # Select a subset of unique lines for additional training questions
    selected_lines = random.sample(list(unique_lines.items()), int(len(unique_lines) * 0.2))  # 20% for additional training
    training_questions = []
    for line, file_path in selected_lines:
        if line not in [q["messages"][0]["content"] for q in validation_questions]:  # Ensure no overlap with validation
            question = {
                "messages": [
                    {"role": "user", "content": f"Can you explain this line of code found in {file_path}? '{line}'"},
                    {"role": "assistant", "content": "Explanation about the line of code..."}  # Placeholder for actual explanation
                ]
            }
            training_questions.append(question)
    return training_questions

def generate_contextual_training_question(file_path, content):
    lines = content.splitlines()
    if len(lines) < 3:  # Need at least 3 lines to form a meaningful question
        return None

    # Randomly select a starting line, avoiding the first and last lines
    start_line_idx = random.randint(1, len(lines) - 2)
    selected_line = lines[start_line_idx]
    question = {
        "messages": [
            {"role": "user",
             "content": f"In {os.path.basename(file_path)}, can you explain this line of code? '{selected_line}'"},
            {"role": "assistant", "content": "Explanation about the line of code..."}  # Placeholder for actual explanation
        ]
    }
    return question

def write_jsonl_file(data, file_name):
    with open(file_name, 'w') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n')


def get_random_line(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [line for line in file]

        valid_lines = [(i, line.strip()) for i, line in enumerate(lines, start=1) if
                       line.strip() and not line.strip().startswith('#')]
        if valid_lines:
            line_number, line = random.choice(valid_lines)
            return line, (line_number)
        else:
            return None, None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, None

def get_random_line_with_context(file_path, context_size=2):
    try:
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]

        # Identifying valid lines for selection
        valid_lines_indices = [i for i, line in enumerate(lines)]

        if valid_lines_indices:
            chosen_index = random.choice(valid_lines_indices)
            # Extract context while maintaining original file structure
            context_start = max(0, chosen_index - context_size)
            context_end = min(len(lines), chosen_index + context_size + 1)
            context = lines[context_start:context_end]
            return ' ... '.join(context), (chosen_index + 1)  # +1 for 1-based indexing
        else:
            return None, None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, None


def get_project_structure(project_path, spec):
    file_paths = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            if spec and spec.match_file(file_path):
                continue
            relative_file_path = os.path.relpath(file_path, project_path)
            file_paths.append(relative_file_path.replace(os.sep, '/'))
    return file_paths

def generate_project_structure_question(project_name, project_structure):
    question = (
        f"What is the file structure of the {project_name} project? "
        "Please answer with json with the next structure: "
        "{\"project_structure\": [\"file1\", \"file2\", ...]}"
    )
    answer = json.dumps({"project_structure": project_structure})
    return {
        "messages": [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    }

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

def load_gitignore(project_path):
    try:
        with open(os.path.join(project_path, '.gitignore'), 'r') as file:
            return pathspec.PathSpec.from_lines('gitwildmatch', file)
    except FileNotFoundError:
        return None

def tokenize(text):
    # Simple tokenizer: split by whitespace and punctuation
    return text.split()

def get_random_snippet_with_context(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [file.read().strip() for line in file]

        # Identifying valid snippets for selection
        valid_snippet_indices = [i for i, line in enumerate(lines) if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('//')]
        if valid_snippet_indices:
            chosen_index = random.choice(valid_snippet_indices)
            snippet = lines[chosen_index]

            # Extracting a few lines around the chosen snippet for context
            context_start = max(0, chosen_index - 2)
            context_end = min(len(lines), chosen_index + 3)
            context = ' ... '.join(lines[context_start:context_end])
            return snippet, context
        else:
            return None, None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, None


# Example usage
# generate_jsonl_for_project('.', 'MyProject')


def update_unique_lines(unique_lines, content, file_path):
    lines = content.splitlines()
    for line in lines:
        if line not in unique_lines:
            unique_lines[line] = file_path

def generate_validation_questions(unique_lines, validation_ratio, project_name):
    # Select a subset of unique lines for validation
    selected_lines = random.sample(list(unique_lines.items()), int(len(unique_lines) * validation_ratio))
    return [
        {
            "messages": [
                {"role": "user", "content": f"In the {project_name} project, where can I find this line of code: '{line}'?"},
                {"role": "assistant", "content": json.dumps({"file_path": file_path})}
            ]
        }
        for line, file_path in selected_lines
    ]

def generate_source_code_entry(file_path, content, project_name):
    return {
        "messages": [
            {"role": "user", "content": f"What is the source code of {file_path} for the {project_name} project?"},
            {"role": "assistant", "content": content}
        ]
    }

def write_jsonl_files(jsonl_data, validation_questions, project_name, current_datetime):
    training_file_name = f'{project_name}_training_{current_datetime}.jsonl'
    validation_file_name = f'{project_name}_validation_{current_datetime}.jsonl'
    write_jsonl_file(jsonl_data, training_file_name)
    write_jsonl_file(validation_questions, validation_file_name)
