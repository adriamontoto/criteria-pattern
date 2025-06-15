<a name="readme-top"></a>

# 🤏🏻 Criteria Pattern

<p align="center">
    <a href="https://github.com/adriamontoto/criteria-pattern/actions/workflows/ci.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/criteria-pattern/actions/workflows/ci.yaml/badge.svg?event=push&branch=master" alt="CI Pipeline">
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

query, parameters = SqlConverter.convert(criteria=is_adult & (email_is_gmail | email_is_yahoo), table='user')
print(query)
print(parameters)
# >>> SELECT * FROM user WHERE (age >= %(parameter_0)s AND (email LIKE '%%' || %(parameter_1)s OR email LIKE '%%' || %(parameter_2)s));
# >>> {'parameter_0': 18, 'parameter_1': '@gmail.com', 'parameter_2': '@yahoo.com'}
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="contributing"></a>

## 🤝 Contributing

We love community help! Before you open an issue or pull request, please read:

- [`🤝 How to Contribute`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/CONTRIBUTING.md)
- [`🧭 Code of Conduct`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/CODE_OF_CONDUCT.md)
- [`🔐 Security Policy`](https://github.com/adriamontoto/criteria-pattern/blob/master/.github/SECURITY.md)

_Thank you for helping make **🤏🏻 Criteria Pattern** package awesome! 🌟_

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="license"></a>

## 🔑 License

This project is licensed under the terms of the [`MIT license`](https://github.com/adriamontoto/criteria-pattern/blob/master/LICENSE.md).

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>
