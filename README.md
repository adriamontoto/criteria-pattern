<a name="readme-top"></a>

# 🤏🏻 Criteria Pattern

<p align="center">
    <a href="https://github.com/adriamontoto/criteria-pattern/actions/workflows/test.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/criteria-pattern/actions/workflows/test.yaml/badge.svg?event=push&branch=master" alt="Test Pipeline">
    </a>
    <a href="https://github.com/adriamontoto/criteria-pattern/actions/workflows/lint.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/criteria-pattern/actions/workflows/lint.yaml/badge.svg?event=push&branch=master" alt="Lint Pipeline">
    </a>
        <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/adriamontoto/criteria-pattern" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/adriamontoto/criteria-pattern.svg" alt="Coverage Pipeline">
    </a>
    <a href="https://pypi.org/project/criteria-pattern" target="_blank">
        <img src="https://img.shields.io/pypi/v/criteria-pattern?color=%2334D058&label=pypi%20package" alt="Package Version">
    </a>
    <a href="https://pypi.org/project/criteria-pattern/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/criteria-pattern.svg?color=%2334D058" alt="Supported Python Versions">
    </a>
</p>

The **Criteria Pattern** is a Python 🐍 package that simplifies and standardizes criteria based filtering 🤏🏻, validation and selection. This package provides a set of prebuilt 👷🏻 objects and utilities that you can drop into your existing projects and not have to implement yourself.

These utilities 🛠️ are useful when you need complex filtering logic. It also enforces 👮🏻 best practices so all your filtering processes follow a uniform standard.

Easy to install and integrate, this is a must have for any Python developer looking to simplify their workflow, enforce design patterns and use the full power of modern ORMs and SQL 🗄️ in their projects 🚀.
<br><br>

## Table of Contents

- [📥 Installation](#installation)
- [💻 Utilization](#utilization)
- [🤝 Contributing](#contributing)
- [🔑 License](#license)

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="installation"></a>

## 📥 Installation

You can install **Criteria Pattern** using `pip`:

```bash
pip install criteria-pattern
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="utilization"></a>

## 💻 Utilization

```python
from criteria_pattern import Criteria, Filter, FilterOperator
from criteria_pattern.converter import SqlConverter

is_adult = Criteria(filters=[Filter('age', FilterOperator.GREATER_OR_EQUAL, 18)])
email_is_gmail = Criteria(filters=[Filter('email', FilterOperator.ENDS_WITH, '@gmail.com')])
email_is_yahoo = Criteria(filters=[Filter('email', FilterOperator.ENDS_WITH, '@yahoo.com')])

query = SqlConverter.convert(criteria=is_adult & (email_is_gmail | email_is_yahoo), table='user')

print(query)

# >>> SELECT * FROM user WHERE (age >= '18' AND (email LIKE '%@gmail.com' OR email LIKE '%@yahoo.com'));
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="contributing"></a>

## 🤝 Contributing

We welcome contributions to **Criteria Pattern**! To ensure a smooth collaboration process, please follow the guidelines below.

### How to Contribute

**1. Fork the Repository:** Click the "Fork" button at the top right of the repository page.

**2. Clone Your Fork:**

```bash
git clone git+ssh://git@github.com/<your-username>/criteria-pattern.git
```

**3. Create a Branch:**

```bash
git checkout -b feature/your-feature-name
```

**4. Make Your Changes:** Implement your new feature or fix a bug.

**5. Run Tests:** Ensure all the following tests pass before submitting your changes.

- Run tests:

```bash
make test
```

- Run tests with coverage:

```bash
make coverage
```

- Run linter:

```bash
make lint
```

- Run formatter:

```bash
make format
```

**6. Commit Your Changes:**

```bash
git commit -m "✨ feature: your feature description"
```

**7. Push to Your Fork:**

```bash
git push origin feature/your-feature-name
```

**8. Create a Pull Request:** Navigate to the original repository and create a pull request from your fork.

**9. Wait for Review:** Your pull request will be reviewed by the maintainers. Make any necessary changes based on their feedback.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="license"></a>

## 🔑 License

This project is licensed under the terms of the [`MIT license`](https://github.com/adriamontoto/criteria-pattern/blob/master/LICENSE.md).

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>
