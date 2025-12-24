# Contributing to Local Data Engineering Environment

Thank you for your interest in contributing to this project! This guide will help you get started.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check existing issues to avoid duplicates
2. Open a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Specify your environment (OS, Python version, etc.)

### Submitting Changes

1. **Fork the repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add or update tests as needed
   - Update documentation if necessary

4. **Test your changes**
   - Run `python test_setup.py`
   - Execute the Jupyter notebook end-to-end
   - Verify on multiple platforms if possible

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes

## Code Style Guidelines

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Add comments for complex logic

Example:
```python
def load_sales_data():
    """
    Load sales data from CSV file.

    Returns:
        list: List of dictionaries containing sales records

    Raises:
        FileNotFoundError: If sample.csv doesn't exist
    """
    csv_path = Path("../data/sample.csv")
    # Implementation here
```

### Jupyter Notebooks

- Use markdown cells for documentation
- Add clear section headers
- Include explanatory text before code cells
- Keep code cells focused on single tasks
- Add output examples where helpful

### Documentation

- Use clear, concise language
- Include code examples
- Update README.md for new features
- Add troubleshooting tips for common issues

## Development Setup

1. Fork and clone the repository
2. Run the setup script for your platform
3. Activate the virtual environment
4. Make your changes
5. Test thoroughly

## Testing Guidelines

### Before Submitting

Ensure all of these pass:

- [ ] `python test_setup.py` - All checks pass
- [ ] Jupyter notebook runs without errors
- [ ] New features are documented
- [ ] Code follows style guidelines
- [ ] No breaking changes (or clearly documented)

### Adding Tests

If adding new functionality:

1. Add validation to `test_setup.py`
2. Include example usage in the notebook
3. Document expected behavior

## Areas for Contribution

### Beginner-Friendly

- Improve documentation
- Add more sample datasets
- Create additional example queries
- Fix typos or clarify instructions
- Add troubleshooting tips

### Intermediate

- Add new data quality checks
- Implement data visualizations
- Create additional notebooks (e.g., visualization, advanced analytics)
- Improve error handling
- Add configuration options

### Advanced

- Implement incremental loading strategies
- Add support for new data sources (APIs, databases)
- Create pipeline scheduling examples
- Implement data lineage tracking
- Add performance optimizations
- Create automated testing suite

## Feature Requests

When suggesting new features:

1. Explain the use case
2. Describe the expected behavior
3. Consider impact on existing functionality
4. Provide implementation ideas (optional)

## Code Review Process

All contributions go through code review:

1. Maintainers will review your PR
2. Feedback may be provided for improvements
3. Update your PR based on feedback
4. Once approved, it will be merged

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Share knowledge and experiences
- Have patience with beginners

## Questions?

If you have questions about contributing:

- Open an issue with the "question" label
- Check existing issues and discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

---

Thank you for helping make this project better!
