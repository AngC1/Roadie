# Contributing to Roadie MCP Server

Thank you for your interest in contributing to the Roadie MCP Server! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/Roadie.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Description of changes"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and concise

## Adding New Templates

To add a new YAML template:

1. Add the template to `src/roadie_mcp_server/templates.py`
2. Register it in the `list_resources()` function in `server.py`
3. Add a mapping in `read_resource()` function
4. Create an example in the `templates/` or `examples/` directory
5. Update documentation in `README.md` and `USAGE.md`

## Adding New Tools

To add a new tool:

1. Define the tool in `list_tools()` function in `server.py`
2. Implement the tool logic as a function
3. Add the tool handler in `call_tool()` function
4. Write tests for the tool
5. Document the tool in `USAGE.md`

## Testing

Before submitting a PR:

1. Test all existing functionality
2. Add tests for new features
3. Ensure all tests pass: `pytest`
4. Test the server manually:
   ```bash
   python -m roadie_mcp_server.server
   ```

## Documentation

- Update `README.md` for major changes
- Update `USAGE.md` for new tools or resources
- Add examples to the `examples/` directory
- Keep code comments up to date

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include examples if adding new features
- Ensure tests pass
- Update documentation as needed

## Reporting Issues

When reporting issues:

- Use a clear, descriptive title
- Describe the expected behavior
- Describe the actual behavior
- Provide steps to reproduce
- Include error messages if applicable
- Mention your Python version and OS

## Feature Requests

We welcome feature requests! When suggesting a feature:

- Explain the use case
- Describe the expected behavior
- Consider implementation details
- Discuss how it fits with existing features

## Code Review Process

1. All PRs require review
2. Address reviewer feedback
3. Keep PRs focused on a single feature/fix
4. Be responsive to comments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for questions or discussions about contributing.

Thank you for contributing! 🎉
