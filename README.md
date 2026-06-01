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
    <a href="https://pepy.tech/projects/criteria-pattern" target="_blank">
        <img src="https://static.pepy.tech/badge/criteria-pattern/month" alt="Package Downloads">
    </a>
    <a href="https://deepwiki.com/adriamontoto/criteria-pattern" target="_blank">
        <img src="https://img.shields.io/badge/DeepWiki-adriamontoto%2Fcriteria--pattern-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==" alt="Project Documentation">
    </a>
</p>

The **Criteria Pattern** is a Python 🐍 package that simplifies and standardizes criteria based filtering 🤏🏻, validation and selection. This package provides a set of prebuilt 👷🏻 objects and utilities that you can drop into your existing projects and not have to implement yourself.

These utilities 🛠️ are useful when you need complex filtering logic. It also enforces 👮🏻 best practices so all your filtering processes follow a uniform standard.

Easy to install and integrate, this is a must have for any Python developer looking to simplify their workflow, enforce design patterns and use the full power of modern ORMs and SQL 🗄️ in their projects 🚀.
<br><br>

## Table of Contents

- [📥 Installation](#installation)
- [📚 Documentation](#documentation)
- [✨ Features](#features)
- [💻 Utilization](#utilization)
  - [🧱 Core Concepts](#core-concepts)
  - [🧮 Supported Operators](#supported-operators)
  - [🔄 Available Converters](#available-converters)
  - [🔐 Security For User-Facing APIs](#security-for-user-facing-apis)
  - [🛡️ SQL Conversion And Safety](#sql-conversion-and-safety)
  - [📦 Request Body Examples](#request-body-examples)
  - [🧭 Structured URL Query Examples](#structured-url-query-examples)
  - [🎯 Real-Life Case: Multi-tenant User Search Service](#real-life-case)
  - [🔎 Simple URL Query Examples](#simple-url-query-examples)
  - [🧪 Testing Helpers](#testing-helpers)
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

<a name="documentation"></a>

## 📚 Documentation

The root README is the entry point. Deeper guides live in this repository and are linked here:

- [`🧱 Usage Guide`](docs/usage/README.md): Core models, composition rules, operators and pagination.
- [`🔄 Converter Guide`](docs/converters/README.md): SQL converters, request converters, placeholder styles and mapping.
- [`🔐 Security Guide`](docs/security/README.md): User-facing criteria safety and injection prevention.
- [`🧪 Testing Guide`](docs/testing/README.md): Object mother helpers and testing recommendations.

This [project's DeepWiki documentation](https://deepwiki.com/adriamontoto/criteria-pattern) is also available for generated repository navigation.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="features"></a>

## ✨ Features

**Criteria Pattern** gives you a typed, reusable way to describe queries before deciding how they should be executed.

- 🧱 **Composable criteria objects** with filters, orders, page size and page number.
- 🔗 **Boolean composition** with `&`, `|` and `~` for `AND`, `OR` and `NOT` logic.
- 🔎 **20 filter operators** covering equality, comparison, pattern matching, ranges, null checks and list membership.
- ↕️ **Ordering primitives** with duplicate order-field protection.
- 📄 **Pagination primitives** that enforce positive integer values and consistent page-number usage.
- 🗄️ **SQL converters** for PostgreSQL, MySQL, MariaDB and SQLite.
- 🧾 **Request converters** for decoded request bodies, structured URL queries and compact suffix-based URL queries.
- 🛡️ **Security-oriented allowlist validation** for tables, columns, fields, operators, directions and pagination bounds.
- 🧰 **Field and operator mapping** so public API names can be translated to internal model or database names.
- 🧪 **Object mother testing helpers** for downstream projects that want realistic criteria fixtures.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="utilization"></a>

## 💻 Utilization

```python
from criteria_pattern import Criteria, Filter, Operator
from criteria_pattern.converters import CriteriaToPostgresqlConverter

is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
email_is_gmail = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@gmail.com')])
email_is_yahoo = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@yahoo.com')])

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=is_adult & (email_is_gmail | email_is_yahoo),
    table='user',
    valid_columns=['age', 'email'],
    valid_operators=[Operator.GREATER_OR_EQUAL, Operator.ENDS_WITH],
)
print(query)
print(parameters)
# >>> SELECT * FROM "user" WHERE ("age" >= %(parameter_0)s AND ("email" LIKE '%%' || %(parameter_1)s OR "email" LIKE '%%' || %(parameter_2)s));
# >>> {'parameter_0': 18, 'parameter_1': '@gmail.com', 'parameter_2': '@yahoo.com'}
```

<a name="core-concepts"></a>

### 🧱 Core Concepts

The main model is `Criteria`. A criteria can contain filters, orders and pagination:

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order


criteria = Criteria(
    filters=[
        Filter(field='status', operator=Operator.EQUAL, value='ACTIVE'),
        Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18),
    ],
    orders=[
        Order(field='created_at', direction=Direction.DESC),
    ],
    page_size=20,
    page_number=1,
)
```

Criteria can be composed without losing the boolean structure:

```python
from criteria_pattern import Criteria, Filter, Operator


is_active = Criteria(filters=[Filter(field='status', operator=Operator.EQUAL, value='ACTIVE')])
is_adult = Criteria(filters=[Filter(field='age', operator=Operator.GREATER_OR_EQUAL, value=18)])
has_company_email = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value='@acme.com')])

criteria = is_active & (is_adult | has_company_email)
not_archived = ~Criteria(filters=[Filter(field='archived_at', operator=Operator.IS_NOT_NULL, value=None)])
```

Pagination is optional. `page_size` can be used alone for `LIMIT`, while `page_number` must be used with `page_size` so converters can calculate the offset.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="supported-operators"></a>

### 🧮 Supported Operators

| Operator | Meaning | Expected value |
| --- | --- | --- |
| `EQUAL` | Field equals value | scalar |
| `NOT_EQUAL` | Field does not equal value | scalar |
| `GREATER` | Field is greater than value | scalar |
| `GREATER_OR_EQUAL` | Field is greater than or equal to value | scalar |
| `LESS` | Field is less than value | scalar |
| `LESS_OR_EQUAL` | Field is less than or equal to value | scalar |
| `LIKE` | SQL-like pattern match | scalar pattern |
| `NOT_LIKE` | SQL-like pattern negation | scalar pattern |
| `CONTAINS` | Field contains value | scalar |
| `NOT_CONTAINS` | Field does not contain value | scalar |
| `STARTS_WITH` | Field starts with value | scalar |
| `NOT_STARTS_WITH` | Field does not start with value | scalar |
| `ENDS_WITH` | Field ends with value | scalar |
| `NOT_ENDS_WITH` | Field does not end with value | scalar |
| `BETWEEN` | Field is between two values | two values |
| `NOT_BETWEEN` | Field is not between two values | two values |
| `IS_NULL` | Field is null | ignored / `None` |
| `IS_NOT_NULL` | Field is not null | ignored / `None` |
| `IN` | Field is one of many values | one or more values |
| `NOT_IN` | Field is not one of many values | one or more values |

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="available-converters"></a>

### 🔄 Available Converters

The package includes converters for SQL generation and request parsing:

- [`criteria_pattern.converters.CriteriaToPostgresqlConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/criteria_to_postgresql_converter.py): Converts a `Criteria` object into PostgreSQL SQL + parameters.
- [`criteria_pattern.converters.CriteriaToMysqlConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/criteria_to_mysql_converter.py): Converts a `Criteria` object into MySQL SQL + parameters.
- [`criteria_pattern.converters.CriteriaToMariadbConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/criteria_to_mariadb_converter.py): Converts a `Criteria` object into MariaDB SQL + parameters.
- [`criteria_pattern.converters.CriteriaToSqliteConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/criteria_to_sqlite_converter.py): Converts a `Criteria` object into SQLite SQL + parameters.
- [`criteria_pattern.converters.SimpleUrlToCriteriaConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/simple_url_to_criteria_converter.py): Parses simple public URL query parameters into a `Criteria` object.
- [`criteria_pattern.converters.UrlToCriteriaConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/url_to_criteria_converter.py): Parses URL query parameters into a `Criteria` object.
- [`criteria_pattern.converters.BodyToCriteriaConverter`](https://github.com/adriamontoto/criteria-pattern/blob/master/criteria_pattern/converters/body_to_criteria_converter.py): Parses decoded request bodies into a `Criteria` object.

SQL converter output uses the placeholder style expected by each database family:

| Converter | Placeholder style | Parameters |
| --- | --- | --- |
| `CriteriaToPostgresqlConverter` | `%(parameter_0)s` | `dict[str, object]` |
| `CriteriaToMysqlConverter` | `%s` | `list[object]` |
| `CriteriaToMariadbConverter` | `%s` | `list[object]` |
| `CriteriaToSqliteConverter` | `:parameter_0` | `dict[str, object]` |

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="security-for-user-facing-apis"></a>

### 🔐 Security For User-Facing APIs

When criteria comes from a URL, JSON body, form, dashboard or any other user-facing surface, treat every field, operator, direction and pagination value as untrusted.

Criteria Pattern parameterizes **filter values** for SQL converters, quotes SQL identifiers per dialect, and enables allowlist validation by default. SQL identifiers still cannot be safely parameterized by database drivers, so for user-facing APIs you must pass explicit `valid_*` allowlists instead of relying on implicit defaults derived from the current criteria.

Use this rule of thumb:

| Input kind | Risk | Recommended protection |
| --- | --- | --- |
| Filter values like `'Doe'`, `18` or `['ACTIVE']` | SQL value injection | Handled by converter parameters |
| Table names | SQL identifier injection | `valid_tables` allowlist (validation on by default) |
| Selected columns | SQL identifier injection | `valid_columns` allowlist (validation on by default) |
| Filter and order fields | SQL identifier injection | `valid_fields` when parsing; `valid_columns` with mapped SQL column names when converting |
| Operators | Query behavior abuse | `valid_operators` allowlist with only the operators you expose |
| Directions | Query behavior abuse | `valid_directions` allowlist |
| Page size and page number | Expensive queries / overflow | strict `max_page_size` / `max_page_number` (validation on by default) |

The safest user-facing flow is:

1. Keep allowlists in application code, not in request data.
2. Parse request input with `BodyToCriteriaConverter`, `UrlToCriteriaConverter` or `SimpleUrlToCriteriaConverter`.
3. Map public field names to internal field or column names with `fields_mapping`.
4. Enable field, operator, direction and pagination validation in the request converter.
5. Enable table, column, criteria, operator, direction and pagination validation again in the SQL converter.

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import BodyToCriteriaConverter, CriteriaToPostgresqlConverter


body = {
    'filters': [{'field': 'q', 'operator': 'contains', 'value': 'Doe'}],
    'orders': [{'field': 'created', 'direction': 'DESC'}],
    'page_size': 20,
    'page_number': 1,
}

fields_mapping = {'q': 'name', 'created': 'created_at'}
valid_fields = ['name', 'created_at']
valid_operators = [Operator.CONTAINS]
valid_directions = [Direction.DESC]

criteria = BodyToCriteriaConverter.convert(
    body=body,
    fields_mapping=fields_mapping,
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_fields=valid_fields,
    valid_operators=valid_operators,
    valid_directions=valid_directions,
    max_page_size=100,
    max_page_number=1000,
)

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=['id', 'name', 'created_at'],
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=['users'],
    valid_columns=['id', 'name', 'created_at'],
    valid_operators=valid_operators,
    valid_directions=valid_directions,
    max_page_size=100,
    max_page_number=1000,
)
```

This keeps the public API flexible while ensuring SQL identifiers and query behavior are constrained by code you control.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="sql-conversion-and-safety"></a>

### 🛡️ SQL Conversion And Safety

Filter values are parameterized, which protects the values passed to predicates. Identifier validation is separate and must be enabled explicitly when identifiers can be influenced by users.

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToPostgresqlConverter


criteria = Criteria(
    filters=[Filter(field='public_name', operator=Operator.CONTAINS, value='Doe')],
    orders=[Order(field='created_at', direction=Direction.DESC)],
    page_size=20,
    page_number=2,
)

query, parameters = CriteriaToPostgresqlConverter.convert(
    criteria=criteria,
    table='users',
    columns=['id', 'name', 'email'],
    columns_mapping={'public_name': 'name'},
    check_table_injection=True,
    check_column_injection=True,
    check_criteria_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    check_pagination_bounds=True,
    valid_tables=['users'],
    valid_columns=['id', 'name', 'email', 'created_at', 'public_name'],
    valid_operators=[Operator.CONTAINS],
    valid_directions=[Direction.DESC],
    max_page_size=100,
    max_page_number=1000,
)

print(query)
print(parameters)
# >>> SELECT "id", "name", "email" FROM "users" WHERE "name" LIKE '%%' || %(parameter_0)s || '%%' ORDER BY "created_at" DESC LIMIT %(limit_1)s OFFSET %(offset_2)s;
# >>> {'parameter_0': 'Doe', 'limit_1': 20, 'offset_2': 20}
```

Use `columns_mapping` when your public API fields should not expose your database column names directly. When `check_criteria_injection` is enabled, include the accepted public criteria field names in `valid_columns` too.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="request-body-examples"></a>

### 📦 Request Body Examples

Use `BodyToCriteriaConverter` when your API receives a decoded dictionary, for example from JSON.

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import BodyToCriteriaConverter


body = {
    'filters': [
        {'field': 'full_name', 'operator': 'contains', 'value': 'Doe'},
        {'field': 'status', 'operator': 'IN', 'value': ['ACTIVE', 'PENDING']},
        {'field': 'price', 'operator': 'BETWEEN', 'value': [10, 100]},
    ],
    'orders': [
        {'field': 'created_at', 'direction': 'desc'},
    ],
    'page_size': 20,
    'page_number': 1,
}

criteria = BodyToCriteriaConverter.convert(
    body=body,
    fields_mapping={'full_name': 'name'},
    operator_mapping={'after': Operator.GREATER},
    check_field_injection=True,
    check_operator_injection=True,
    check_direction_injection=True,
    valid_fields=['name', 'status', 'price', 'created_at'],
    valid_operators=[Operator.CONTAINS, Operator.IN, Operator.BETWEEN],
    valid_directions=[Direction.DESC],
)

print(criteria.filters[0].field, criteria.filters[0].operator, criteria.filters[0].value)
# >>> name CONTAINS Doe
```

Accepted body keys are `filters`, `orders`, `page_size` and `page_number`. Unknown keys, missing required filter/order keys and invalid value shapes raise `IntegrityError`.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="structured-url-query-examples"></a>

### 🧭 Structured URL Query Examples

Use `UrlToCriteriaConverter` when you want an explicit URL format that can express filters, orders and pagination.

```python
from criteria_pattern import Direction, Operator
from criteria_pattern.converters import UrlToCriteriaConverter


url = (
    'https://api.example.com/users?'
    'filters[0][field]=name&filters[0][operator]=CONTAINS&filters[0][value]=Doe&'
    'filters[1][field]=age&filters[1][operator]=GREATER_OR_EQUAL&filters[1][value]=18&'
    'orders[0][field]=created_at&orders[0][direction]=DESC&'
    'page_size=20&page_number=1'
)

criteria = UrlToCriteriaConverter.convert(
    url=url,
    valid_fields=['name', 'age', 'created_at'],
    valid_operators=[Operator.CONTAINS, Operator.GREATER_OR_EQUAL],
    valid_directions=[Direction.DESC],
)

print(criteria.filters[0].field, criteria.filters[0].operator, criteria.filters[0].value)
# >>> name CONTAINS Doe

print(criteria.orders[0].field, criteria.orders[0].direction)
# >>> created_at DESC
```

Structured URL values are converted to useful primitive types where possible: booleans, `null` / `none`, integers and floats.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="real-life-case"></a>

### 🎯 Real-Life Case: Multi-tenant User Search Service

Imagine an admin dashboard where each request must:

1. Always restrict results to the current tenant.
2. Optionally filter active users.
3. Search only users with company emails.
4. Sort by newest users first.

With Criteria Pattern, each concern is a small reusable criteria object. You combine them using `&` and `|`, then convert once to SQL:

```python
from criteria_pattern import Criteria, Direction, Filter, Operator, Order
from criteria_pattern.converters import CriteriaToPostgresqlConverter


class UserSearchService:
    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id

    def build_query(self, *, only_active: bool, corporate_domain: str) -> tuple[str, dict[str, object]]:
        tenant_scope = Criteria(filters=[Filter(field='tenant_id', operator=Operator.EQUAL, value=self.tenant_id)])
        active_scope = Criteria(filters=[Filter(field='is_active', operator=Operator.EQUAL, value=True)])
        email_scope = Criteria(filters=[Filter(field='email', operator=Operator.ENDS_WITH, value=corporate_domain)])
        sort_scope = Criteria(orders=[Order(field='created_at', direction=Direction.DESC)])

        criteria = tenant_scope & email_scope & sort_scope
        if only_active:
            criteria = criteria & active_scope

        return CriteriaToPostgresqlConverter.convert(
            criteria=criteria,
            table='users',
            valid_columns=['tenant_id', 'is_active', 'email', 'created_at'],
            valid_operators=[Operator.EQUAL, Operator.ENDS_WITH],
            valid_directions=[Direction.DESC],
        )


service = UserSearchService(tenant_id='tenant_123')
query, parameters = service.build_query(only_active=True, corporate_domain='@acme.com')

print(query)
print(parameters)
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="simple-url-query-examples"></a>

### 🔎 Simple URL Query Examples

Use `SimpleUrlToCriteriaConverter` when you want a compact public query format where each parameter becomes one `AND` filter. Plain parameters use equality, and suffixes map to operators.

```python
from criteria_pattern import Operator
from criteria_pattern.converters import SimpleUrlToCriteriaConverter


criteria = SimpleUrlToCriteriaConverter.convert(
    url='https://api.example.com/users?name=Doe&age_gte=18&page_size=20&page_number=1',
    valid_fields=['name', 'age'],
    valid_operators=[Operator.EQUAL, Operator.GREATER_OR_EQUAL],
)

print(criteria.filters[0].field, criteria.filters[0].operator, criteria.filters[0].value)
# >>> name EQUAL Doe

print(criteria.filters[1].field, criteria.filters[1].operator, criteria.filters[1].value)
# >>> age GREATER_OR_EQUAL 18

print(criteria.page_size, criteria.page_number)
# >>> 20 1
```

Common suffixes:

| URL parameter | Parsed filter |
| --- | --- |
| `name=Doe` | `Filter(field='name', operator=Operator.EQUAL, value='Doe')` |
| `name_eq=Doe` | `Filter(field='name', operator=Operator.EQUAL, value='Doe')` |
| `status_ne=DELETED` | `Filter(field='status', operator=Operator.NOT_EQUAL, value='DELETED')` |
| `price_gt=10` | `Filter(field='price', operator=Operator.GREATER, value=10)` |
| `price_gte=10` | `Filter(field='price', operator=Operator.GREATER_OR_EQUAL, value=10)` |
| `price_lt=100` | `Filter(field='price', operator=Operator.LESS, value=100)` |
| `price_lte=100` | `Filter(field='price', operator=Operator.LESS_OR_EQUAL, value=100)` |
| `email_contains=gmail.com` | `Filter(field='email', operator=Operator.CONTAINS, value='gmail.com')` |
| `name_starts_with=Ad` | `Filter(field='name', operator=Operator.STARTS_WITH, value='Ad')` |
| `email_ends_with=.com` | `Filter(field='email', operator=Operator.ENDS_WITH, value='.com')` |
| `price_between=10,100` | `Filter(field='price', operator=Operator.BETWEEN, value=[10, 100])` |
| `age_not_between=18&age_not_between=30` | `Filter(field='age', operator=Operator.NOT_BETWEEN, value=[18, 30])` |
| `status_in=ACTIVE&status_in=PENDING` | `Filter(field='status', operator=Operator.IN, value=['ACTIVE', 'PENDING'])` |
| `status_not_in=DELETED` | `Filter(field='status', operator=Operator.NOT_IN, value=['DELETED'])` |
| `deleted_at_is_null=true` | `Filter(field='deleted_at', operator=Operator.IS_NULL, value=None)` |
| `deleted_at_is_not_null=true` | `Filter(field='deleted_at', operator=Operator.IS_NOT_NULL, value=None)` |

Comma-separated values are also supported for list operators:

```python
criteria = SimpleUrlToCriteriaConverter.convert(
    url='https://api.example.com/users?status_in=ACTIVE,PENDING,BLOCKED',
    valid_fields=['status'],
    valid_operators=[Operator.IN],
)

print(criteria.filters[0].value)
# >>> ['ACTIVE', 'PENDING', 'BLOCKED']
```

You can map public field names to internal field names:

```python
criteria = SimpleUrlToCriteriaConverter.convert(
    url='https://api.example.com/users?full_name_contains=Doe',
    fields_mapping={'full_name': 'name'},
    valid_fields=['name'],
    valid_operators=[Operator.CONTAINS],
)

print(criteria.filters[0].field, criteria.filters[0].operator, criteria.filters[0].value)
# >>> name CONTAINS Doe
```

You can also extend or override URL suffixes:

```python
criteria = SimpleUrlToCriteriaConverter.convert(
    url='https://api.example.com/users?created_at_after=2026-05-18',
    suffix_operator_mapping={'after': Operator.GREATER},
    valid_fields=['created_at'],
    valid_operators=[Operator.GREATER],
)

print(criteria.filters[0].field, criteria.filters[0].operator, criteria.filters[0].value)
# >>> created_at GREATER 2026-05-18
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

<a name="testing-helpers"></a>

### 🧪 Testing Helpers

The package includes object mother helpers for tests in downstream projects. They are useful when you need valid random criteria objects and want to override only the fields that matter for a specific test.

```python
from criteria_pattern import Filter, Operator
from criteria_pattern.models.testing.mothers import CriteriaMother
from criteria_pattern.models.testing.mothers.filter import FilterMother


criteria = CriteriaMother.with_filters(
    filters=[
        Filter(field='status', operator=Operator.EQUAL, value='ACTIVE'),
        FilterMother.create(field='age', operator=Operator.GREATER_OR_EQUAL, value=18),
    ]
)

print(criteria.has_filters())
# >>> True
```

Available helpers include `CriteriaMother`, `FilterMother`, `FiltersMother`, `OrderMother`, `OrdersMother`, `PageSizeMother`, `PageNumberMother`, plus field/operator/direction mothers under the filter and order testing packages.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

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
