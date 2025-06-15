# 🤝 How to Contribute

First off, **thank you** for wanting to improve **🤏🏻 Criteria Pattern** package! Whether you're fixing a typo or building a whole new feature, your help makes the library better for everyone.

## 🏃🏻‍➡️ Before You Start

1. **Be kind, inclusive, and patient**: we follow our [`🧭 Code of Conduct`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/CODE_OF_CONDUCT.md).
2. **Search first**: check for existing [issues](https://github.com/adriamontoto/criteria-pattern/issues) before opening a new one.
3. **Security issues**: report privately via our [`🔐 Security Policy`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/SECURITY.md); **do not** raise a public issue for vulnerabilities.

## 🚀 Quick-Start Workflow

All examples assume you are using a Linux system with `GNU Make` installed. For more information about the Makefile, see the [🛠️ Tooling](#tooling) section.

1. **Fork the Repository**: Click the fork button on the repository page.

2. **Clone Your Fork**:

```bash
git clone git+ssh://git@github.com/<your-username>/criteria-pattern.git
```

3. **Setup the Development Environment**: Create a virtual environment, install all dependencies (development + production), and install pre-commit hooks.

```bash
make setup
```

4. **Create a Feature Branch**: Create a feature branch from the `master` branch.

```bash
git checkout -b feat/<branch-name>
```

5. **Time to Code**: Make your changes.

6. **Quality Checks**: Run the following commands to ensure your code is formatted, linted, and passes the test suite.

```bash
make format
make lint
make test
make coverage
```

7. **Commit Your Changes**: Commit your changes with a descriptive commit message.
   > More information about our commit message guidelines can be found in the [✍️ Commit Message Guidelines](#commit-message-guidelines) section.

```bash
git add .
git commit -m "feat(converter): implement PostgreSQL converter" -S --signoff  # we only accept signed and signed-off commits
```

8. **Push Your Changes**: Push your changes to your fork.

```bash
git push -u origin feat/<branch-name>
```

9. **Open a Pull Request**: Open a pull request against the `master` branch and fill out our [`pull request template`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/pull_request_template.md).
   > More information about our pull request guidelines and feedback can be found in the [✍️ Pull Request Guidelines](#pull-request-guidelines) section.

<a name="commit-message-guidelines"></a>

## ✍️ Commit Message Guidelines

This repository follows **[Conventional Commits](https://www.conventionalcommits.org)** enforced by [Commitizen](https://commitizen-tools.github.io) as a pre-commit hook and **[Semantic Versioning](https://semver.org)** used by [python-semantic-release](https://python-semantic-release.readthedocs.io) to cut releases and generate changelogs. So any merged commit with `feat`, `fix`, `build` or a `BREAKING CHANGE` bumps the version and publishes to PyPI automatically.

> This repository only accepts signed and signed-off commits, check [GitHub documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) if you need help with that.

### How to Write a Good Commit Message

- **Structure**: Each commit message must consist of a type, an optional scope, and a concise description (e.g., `feat(converter): implement PostgreSQL converter`).
- **Types**: Common types include:
  - `feat`: New feature (minor release).
  - `fix`: Bug fix (patch release).
  - `docs`: Documentation update.
  - `refactor`: Code change that neither fixes a bug nor adds a new feature.
  - `perf`: Performance improvement (patch release).
  - `test`: Update suite of tests.
  - `build`: Changes that affect the build system (new dependencies, tools, ...) (patch release).
  - `ci`: Pipeline changes (GitHub Actions, make commands, ...).
- **Scope**: Use the scope to clarify what part of the codebase is affected (e.g., `primitives`, `dates`, `tests`).
- **Description**: Use the imperative mood ("add", "fix", "update", ...; not "added", "fixed", "updates", ...).
- **Body (optional)**: Explain what and why vs. how. Reference issues if relevant.
- **Breaking Changes**: Append `!` to the commit type or start the body with `BREAKING CHANGE:` if the commit introduces an API or behavioral change (major release).

<a name="pull-request-guidelines"></a>

## ✍️ Pull Request Guidelines

> Only code owners are allowed to merge a pull request.

- Use our [`pull request template`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/pull_request_template.md).
- **Keep PRs Focused**: Submit one logical change per pull request. Avoid bundling unrelated changes together.
- **Descriptive Titles and Summaries**: Use clear, descriptive PR titles and fill out all sections of the PR template, especially the motivation and context.
- **Reference Issues**: Link related issues by number (e.g., `Closes #123`) to enable automatic closing and better tracking.
- **Checklist Completion**: Ensure all items in the PR template checklist are addressed before requesting a review.
- **Passing Checks Required**: PRs must pass all CI checks (format, lint, tests, coverage, ...) before being considered for review (enforced with branch rules).
- **Request Reviews Thoughtfully**: Assign reviewers only after your PR is ready and all checks pass.
- **Rebase or Update**: If your branch is behind `master`, rebase or merge the latest changes before requesting a review (enforced with branch rules).
- **No Force Pushes on Shared Branches**: Only force-push to your own feature branches, not shared or open PR branches (enforced with branch rules).
- **Explain Breaking Changes**: Clearly highlight any breaking changes in the PR description and label/tag accordingly.
- **Documentation and Tests**: Update documentation and tests as needed for your changes.

### How to Write Good Feedback

We follow [Conventional Comments](https://conventionalcomments.org) to keep reviews clear and actionable.

- **Start with a label**: praise:, nitpick:, suggestion:, issue:, or question:.
- **Indicate blockers correctly**: If the pull request must not be merged until the comment is resolved, add the blocking modifier in parentheses after the label, e.g. issue (blocking):.
- **Be specific**: quote the relevant code or line numbers.
- **Stay constructive & courteous**: focus on the code, not the coder.
- **Offer alternatives when pointing out issues**.

<a name="tooling"></a>

## 🛠️ Tooling

> All default project commands require **GNU Make** and are intended to be run on a **Linux system**.

> You must have **UV** installed to use the most of the default project commands.

The project provides a [`Makefile`](https://github.com/adriamontoto/criteria-pattern/blob/master/Makefile) with some helpful commands, this commands must be run from the root of the project. For more details on each command, run `make help`.

- **Environment Setup:** Run `make setup` to create a virtual environment, install all dependencies (development + production), and install pre-commit hooks.
- **Install Dependencies:** Run `make install` to install all dependencies (development + production), use the `GROUP` variable to install only a specific group of dependencies (all, audit, coverage, format, lint, release, test, types).
- **Code Formatting:** Run `make format` to automatically format code using Ruff ([PEP 8](https://peps.python.org/pep-0008) and [PEP 257](https://peps.python.org/pep-0257) compliance), most style issues are auto-corrected.
- **Linting:** Run `make lint` to check code quality using Ruff and mypy for static analysis and type checking.
- **Testing:** Run `make test` to execute all tests.
- **Coverage:** Run `make coverage` to generate a test coverage report.
- **Build:** Run `make build` to build the project.
- **Audit:** Run `make audit` to audit dependencies for known vulnerabilities.
- **Secrets Scanning:** Run `make secrets` to scan for secrets in the hole codebase.
- **Environment Cleanup:** Run `make clean` to remove the virtual environment, caches, and all generated files.

_Thank you for helping make **🤏🏻 Criteria Pattern** package awesome! 🌟_
