# Inbox Client Workspace

## 📬 Description

This repository defines a modular protocol-based interface for email clients (e.g., Gmail, Hotmail). It uses Python `Protocol` classes to describe standardised, mockable interfaces for both messages and inbox clients.

## Requirements

- **Python 3.10 or higher**
- `pytest` for testing
- `mypy` for type checking
- `ruff` for linting
- `uv` (for dependency and workspace management)
- `coverage`

## 🚀 Setup Instructions

1. Clone the repository  
   ```bash
   git clone https://github.com/khamseaffan/Inbox-Client.git
   cd Inbox-Client

2. Install UV, the package manager for dependency management:
   For macOS/linux

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Alternatively, for brew installation: [brew install uv](https://formulae.brew.sh/formula/uv) is sufficient.

   For Windows

   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. Install the project dependencies:
   ```bash
   uv sync
   ```

## Testing
To run all of the test suite at once:  
```bash
pytest
   ```  
To run individual test files:  
```bash
pytest <path-to-specific-test-file>
   ```  
To run individual tests within a file:  
```bash
pytest <path-to-specific-test-file::name-of-individual-test>
   ```  

## Contributions

We welcome any and all contributions and will be using GitHub to track bugs, feature requests, and pull requests.  
By contributing, you agree that your contributions will be licensed under the project's license.

## Bug Reports and Feature Requests

Use the provided templates to report any bugs and request new features. Please follow the templates accurately to help us understand and more efficiently address your issue.

## Pull Requests

When submitting a pull request:

- Use the pull request template provided in the repository and follow its instructions.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Additional Information

- This project uses CircleCI for continuous integration, which automatically runs tests and checks code formatting with ruff.
- The `.gitignore` file is configured to ignore Python-specific files and directories, such as `__pycache__` and the `venv` directory.
