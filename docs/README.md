# 🤏🏻 Criteria Pattern Documentation

This directory contains deeper guides for using **Criteria Pattern** in real applications. The project root
[`README.md`](../README.md) is the quick overview; these pages explain the decisions, safety rules and converter
behaviors in more detail.

## Guides

- [🧱 Usage Guide](usage/README.md): Core models, composition rules, operator value shapes and pagination behavior.
- [🔄 Converter Guide](converters/README.md): SQL converters, request converters, placeholder styles and mapping options.
- [🔐 Security Guide](security/README.md): How to handle user-facing criteria safely and avoid SQL injection risks.
- [🧪 Testing Guide](testing/README.md): Object mother helpers and test-writing recommendations.

## Recommended Reading Order

1. Start with the [Usage Guide](usage/README.md) to understand the domain objects.
2. Read the [Converter Guide](converters/README.md) for your input and database style.
3. Read the [Security Guide](security/README.md) before exposing criteria parsing to users.
4. Use the [Testing Guide](testing/README.md) when adding criteria-heavy tests to your project.

## Quick Safety Rule

Criteria Pattern parameterizes filter values in SQL converters, but SQL identifiers are different: table names, selected
columns, filter fields and order fields must come from trusted code or explicit allowlists. See the
[Security Guide](security/README.md) before wiring request data to SQL conversion.
