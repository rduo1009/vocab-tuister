# AGENTS.md Guide for AI Agents

This AGENTS.md file provides comprehensive guidance for OpenAI Codex, Google Jules, or other AI agents working with this codebase.
This file can also be used by tools like Roo Code, but a .roorules symlink to this file also exists.
The contents of this file is based on a template from https://agentsmd.net/.

## Project Structure for Agent Navigation

- `/src`: Source code that the agent should analyse
  - `/_vendor`: Vendored dependencies (the agent should not modify these)
  - `/client`: The vocab-tuister TUI (written in Go)
  - `/core`: Handles Latin and English words and their inflection, reading vocab lists, and question creation
  - `/scripts`: Scripts, mostly for code generation
  - `/server`: The server code for running the vocab-tuister server
  - `/utils`: Utility functions that Agents.md documents for the agent
- `/tests`: Test files that the agent should maintain and extend (only Python tests, the Go tests are inside `/client`)
- `/stubs`: Type stubs for the untyped Python libraries used by the project.
- `/scripts`: Bash scripts used by the project for development and testing.
- `/docs`: Documentation. If the agent makes major changes, it should edit or add documentation here (as well as in doccomments and docstrings). Ask the user for confirmation before making changes here.
- `/assets`: Static assets i.e. vocab lists (the agent should not modify these directly unless there is a direct issue)

## Coding Conventions for Agent

### General Conventions for Implementation

Focus on code readability and maintainability. Especially for Go code, value simple and idiomatic solutions.
Variable names should not be too long, but should be clear anyway. A comment explaining a variable is better than a long variable name.
For Go code, an error returned in an `if err != nil` block or similar should have extra information added to it. This will help with error tracing. For example:

```go
return errMsg{
	      fmt.Errorf(
				        "failed to post vocab list, status code: %d",
				        resp1.StatusCode,
			  ),
}
```

### General Conventions for Testing

Write unit tests for all new functions. Unit tests should be extensive, especially if the function is complicated.
Use pytest for Python tests, and testify for Go tests.
Python and Go test files should be named in the format "thing being tested"\_test.py or "thing being tested"\_test.go respectively

### General Conventions for Documentation

For Python code, always provide docstrings in the Numpy style.
For Go code, always provide doccomments in the style used in idiomatic Go. Follow the style of the standard library doccomments.
Write comments liberally inside the code as well. A viewer should be able to understand what the code does without understanding or reading the code itself.
Edit docs inside `/docs` if major changes are made. As written earlier, ask the user for confirmation before making changes here.

## Testing Requirements for Agent

The agent should try to run tests specific to the changes that have been made.
However, more blanket tests are available with these commands:

```bash
uv run pytest -m 'not manual and not integration'
uv run pytest --pythonhashseed 1 -m 'integration'
go test ./src/...
```

Additionally, various linting tools (ruff, basedpyright, golangci-lint) can be used with the project.
Look at the code in .pre-commit-config.yaml for further information.

## Committing Requirements for Agent

When writing a commit description, the agent should aim to be clear and mention every change that has been made, even if minor. Just as with code comments, a viewer should be able to understand what the code does without understanding or reading the code itself.
For the commit title, the agent should use one of the following before the title:

- ✨ feat: ...
- 🐛 fix: ...
- 📚 docs: ...
- 🔨 refactor: ...
- 🚀 perf: ...
- 🚨 test: ...
- 🚧 build: ...
- 🤖 ci: ...
- 🧹 chore: ...
