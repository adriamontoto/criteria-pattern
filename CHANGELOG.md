# CHANGELOG

<!-- version list -->

## v3.0.2 (2025-09-15)

### 🐛 Bug Fixes

- Return pagination size and number in combined criteria
  ([`241a09c`](https://github.com/adriamontoto/criteria-pattern/commit/241a09cf32110ec6ae03e41fb196a0f985d10b95))


## v3.0.1 (2025-09-15)

### 🐛 Bug Fixes

- Solve a bug while using multiple filters in the same criteria
  ([`3051d00`](https://github.com/adriamontoto/criteria-pattern/commit/3051d0026edd9de9d5b28eccc304f0383bd9a2a4))


## v3.0.0 (2025-09-15)

### ✨ Features

- Rename converter folder to converters
  ([`0524679`](https://github.com/adriamontoto/criteria-pattern/commit/052467950b46a569ca793c2a792c26e3014e31ec))


## v2.2.0 (2025-09-11)

### 📦 Build System

- Using sqlglot[rs] for faster runtime
  ([`0a4bbe4`](https://github.com/adriamontoto/criteria-pattern/commit/0a4bbe41df5325d028bacf4de647f3351503a720))

### ✨ Features

- Implement url to criteria converter and its tests
  ([`c5b5b37`](https://github.com/adriamontoto/criteria-pattern/commit/c5b5b37282e679f65e3bec4b7496229160818c20))


## v2.1.1 (2025-09-10)

### 🐛 Bug Fixes

- Enhance CriteriaToPostgresqlConverter to quote identifiers
  ([`3038593`](https://github.com/adriamontoto/criteria-pattern/commit/30385936c03d0088cad9d69af3bdb3da7a5878c3))

- Enhance CriteriaToSqliteConverter to quote identifiers
  ([`966a35e`](https://github.com/adriamontoto/criteria-pattern/commit/966a35e79e1a6f5cd72ad5c1edd317d0f15d134d))

- Enhance MySQL and Mariadb converters to use their dialect parameter style
  ([`1af2496`](https://github.com/adriamontoto/criteria-pattern/commit/1af24968ea3c1bc063ab0a238fe5e26cf06322c1))

- Enhance MySQL and Mariadb converters to use their dialect parameter style
  ([`4ae0446`](https://github.com/adriamontoto/criteria-pattern/commit/4ae0446f998cd284d58ffbda2c6c5a91b25ff3ce))


## v2.1.0 (2025-09-10)

### 🐛 Bug Fixes

- Update FilterOperatorMother to exclude specific operators that can cause random test failures
  ([`eafad7d`](https://github.com/adriamontoto/criteria-pattern/commit/eafad7dfa9dcf555a6cca3206d7f385ca186a7b4))

### ✨ Features

- Implement sqlite criteria converter
  ([`b05576b`](https://github.com/adriamontoto/criteria-pattern/commit/b05576be4742f4819040471e658e0cc01e09a0c1))


## v2.0.0 (2025-09-10)

### ✨ Features

- Change raw sql converter name to postgresql
  ([`83ce2b1`](https://github.com/adriamontoto/criteria-pattern/commit/83ce2b14fe88606dd7313721ae05dc93e65dbae3))

- Implement criteria to mysql and mariadb converters
  ([`73a67ff`](https://github.com/adriamontoto/criteria-pattern/commit/73a67ff369812370e2f3ab9e03f36309aef816e9))


## v1.3.0 (2025-09-10)

### 🐛 Bug Fixes

- Remove redundant colons in error messages for InvalidColumnError and InvalidTableError
  ([`631bfcc`](https://github.com/adriamontoto/criteria-pattern/commit/631bfcce1d355ed64b657a98e18cd2dc36def147))

### ✨ Features

- Implement criteria pagination
  ([`0b89c05`](https://github.com/adriamontoto/criteria-pattern/commit/0b89c057ce10b3348134f03975ff2d9cff4bc008))


## v1.2.0 (2025-09-09)

### ✨ Features

- Enhance model constructors with title and parameter attributes
  ([`65b1b77`](https://github.com/adriamontoto/criteria-pattern/commit/65b1b77f5f483d0292f73406ded5f5caebc8d24a))


## v1.1.0 (2025-09-07)

### ✨ Features

- Implement in and not in operators
  ([`e5294ee`](https://github.com/adriamontoto/criteria-pattern/commit/e5294eeffb77be81cae131b7f9dd36714279f92d))


## v1.0.0 (2025-07-20)

### ✨ Features

- Implement hole library using value objects pattern library
  ([`7427554`](https://github.com/adriamontoto/criteria-pattern/commit/7427554202bfbc6b9c08dd4b1cee209e8bc8cc9a))


## v0.1.1 (2025-06-15)

### 📦 Build System

- Update package license locations
  ([`4c05682`](https://github.com/adriamontoto/criteria-pattern/commit/4c05682394b245e8d4f3df23e2c3c3952a76066f))


## v0.1.0 (2025-06-15)

### 🐛 Bug Fixes

- --requirements parameter was not working in requirements file
  ([`5842d22`](https://github.com/adriamontoto/criteria-pattern/commit/5842d22089fbc9a7dc687a44bf27aa5614cde73d))

- Add @override decorator to AndCriteria.orders method
  ([`2d6f519`](https://github.com/adriamontoto/criteria-pattern/commit/2d6f51955c67a5f8b6a24896714e35e84a48ed66))

- Add test to make file folders
  ([`1a7e752`](https://github.com/adriamontoto/criteria-pattern/commit/1a7e7528aa3d6a8b2b181274644cf0f5792dd964))

- Add unique decorator to filter operator enum
  ([`9dce440`](https://github.com/adriamontoto/criteria-pattern/commit/9dce4402798d08b5cd50f65831e932e713bf1e01))

- Add unique decorator to filter operator enum
  ([`cff3973`](https://github.com/adriamontoto/criteria-pattern/commit/cff39738030c4ebd4c33917db31ae62504cf72b3))

- Allow or, and criteria to access criteria method filters and orders
  ([`03b5f56`](https://github.com/adriamontoto/criteria-pattern/commit/03b5f568b493aebdfe6f3c83519982f361c31022))

- Change PyPI URL to point to criteria-pattern in publish workflow
  ([`860485b`](https://github.com/adriamontoto/criteria-pattern/commit/860485b9b5f720d51085baed3b4cfa337a703e54))

- Dict.get can not have default argument
  ([`59e21be`](https://github.com/adriamontoto/criteria-pattern/commit/59e21bef169b12b229ca34602be61c00e130fb7f))

- Fix a typo
  ([`d78e8d4`](https://github.com/adriamontoto/criteria-pattern/commit/d78e8d443b2555ba7c3dedbd621e852c96c2309b))

- Fix a typo of functions names
  ([`64338f9`](https://github.com/adriamontoto/criteria-pattern/commit/64338f93f54aaba3a309c06a9efda1fdb1f779c7))

- Move NOT operator outside the parentheses
  ([`8ae7ed2`](https://github.com/adriamontoto/criteria-pattern/commit/8ae7ed22ca430fd5cf1a5164d15fb8320e623b41))

- Remove generic type on criteria classes
  ([`c462c99`](https://github.com/adriamontoto/criteria-pattern/commit/c462c9994623ee4e17a615e80436bfe54c73d8ab))

- Remove SqlAlchemyConverter from the converter module's exports to prevent installing sqlalchemy if
  not used
  ([`50da2b8`](https://github.com/adriamontoto/criteria-pattern/commit/50da2b83fed7461becd1d410b6d753bd3490b511))

### 📦 Build System

- Accept all packages versions that not exceed the major
  ([`bb1748d`](https://github.com/adriamontoto/criteria-pattern/commit/bb1748d1af809443f9af7ca2e9b140fae74c12b5))

- Add faker as dev requirements
  ([`db40f95`](https://github.com/adriamontoto/criteria-pattern/commit/db40f95b78d8fb805fd6d92a35498c20a7a2100d))

- Add sqlalchemy as project dependency
  ([`b551c8c`](https://github.com/adriamontoto/criteria-pattern/commit/b551c8cf5ef3ddc27e2d804a537dd6ccd41c366b))

- Add sqlglot as package development dependency
  ([`df57dc4`](https://github.com/adriamontoto/criteria-pattern/commit/df57dc40d09f7a227cd36f8b7dc257396193cba9))

- Change package versioning to date based
  ([`9a7f959`](https://github.com/adriamontoto/criteria-pattern/commit/9a7f95944e333affcc14656ed2f7c62d87f5376b))

- Prepare version 2024.11.05
  ([`f485318`](https://github.com/adriamontoto/criteria-pattern/commit/f485318de922835c980963e5e0efe4d14f2b7385))

- Remove requirements files
  ([`e9312dd`](https://github.com/adriamontoto/criteria-pattern/commit/e9312dd16ed183ce9823bcc1c7ff0af17cef8140))

- Update dependencies in pyproject.toml
  ([`811047a`](https://github.com/adriamontoto/criteria-pattern/commit/811047a3dc1d86b4cdd0cadc3779612dc5be5d81))

- Update dev dependencies to use version ranges for better compatibility and future-proofing
  ([`ad2eee0`](https://github.com/adriamontoto/criteria-pattern/commit/ad2eee09ddddb587a042a14b3d9c827e5198d1d5))

- Update faker requirement
  ([`49e22d9`](https://github.com/adriamontoto/criteria-pattern/commit/49e22d9af0a796130282879054d60cddcc69d4ed))

- Update faker requirement
  ([`0cfd083`](https://github.com/adriamontoto/criteria-pattern/commit/0cfd08317be72a769bf4c14e0a03c3eb6203f41d))

- Update faker requirement
  ([`dc2d42a`](https://github.com/adriamontoto/criteria-pattern/commit/dc2d42ae2bb61bd3b13abfe01299ae08b81947f4))

- Update faker requirement
  ([`433dcf1`](https://github.com/adriamontoto/criteria-pattern/commit/433dcf1528feb48536f813ababf66a17a4fc8852))

### ✨ Features

- Adapt code to run in python 3.11
  ([`9ccbb5c`](https://github.com/adriamontoto/criteria-pattern/commit/9ccbb5cd8b63b57d658659807cbced6e261c4767))

- Add __all__ attribute to import all criteria objects
  ([`f53ff65`](https://github.com/adriamontoto/criteria-pattern/commit/f53ff651c98e3462539cb7d376532fcfa6e2b752))

- Add a basic implementation of criteria to sqlalchemy query
  ([`b0e34d1`](https://github.com/adriamontoto/criteria-pattern/commit/b0e34d1ab829027c750f528d134e55cc6088cbc4))

- Add column_mapping parameter so frontend names can be mapped in the backend models or tables
  ([`9376727`](https://github.com/adriamontoto/criteria-pattern/commit/9376727935fb0f966409c9f0c8e6518dd8be106e))

- Add issues template
  ([`2c7b643`](https://github.com/adriamontoto/criteria-pattern/commit/2c7b64318964d7ba5172866791ee7ebc2780b316))

- Add not like operator
  ([`d59fcc7`](https://github.com/adriamontoto/criteria-pattern/commit/d59fcc701ec930e62b0d198029897683c92f5b58))

- Add py.typed file to the package
  ([`8b457fe`](https://github.com/adriamontoto/criteria-pattern/commit/8b457fe0b2bc02d6e066621a32da0880527a33bd))

- Add test folder
  ([`4e23381`](https://github.com/adriamontoto/criteria-pattern/commit/4e23381ba165cbcb797a1f901307415fbcbd4c63))

- Allow and and or operators to use left and right orders
  ([`72bd50b`](https://github.com/adriamontoto/criteria-pattern/commit/72bd50b00e5d2fec97f0d9a701fc74536fb71e2d))

- Bump version to 2024.09.24 in __init__.py for release planning
  ([`bd4ba01`](https://github.com/adriamontoto/criteria-pattern/commit/bd4ba0173b16eac3f16714f3a8e70414d5e78735))

- Create test criteria mother
  ([`97090d4`](https://github.com/adriamontoto/criteria-pattern/commit/97090d48e2d6993e8cf849c1e80957dae1f258c5))

- Create test filter mother
  ([`49ea20c`](https://github.com/adriamontoto/criteria-pattern/commit/49ea20c49ce47e9716c667ae74ff30d6075a0bf1))

- Create test order mother
  ([`6ab3307`](https://github.com/adriamontoto/criteria-pattern/commit/6ab3307b99bec21e655c9720badf624ea8e9ebb4))

- Extend license year range to 2024-2025
  ([`358f01d`](https://github.com/adriamontoto/criteria-pattern/commit/358f01d5b7e15985a75146248e80e4e7e6bd0051))

- Implement all filter operators
  ([`5cead6b`](https://github.com/adriamontoto/criteria-pattern/commit/5cead6be16727864c5c9555478e1cef7f52ed42c))

- Implement and logic with a new class AndCriteria
  ([`8d2720a`](https://github.com/adriamontoto/criteria-pattern/commit/8d2720af513fdc04223fc02fe4278880df6df903))

- Implement and operator to criteria class
  ([`217e6a6`](https://github.com/adriamontoto/criteria-pattern/commit/217e6a69b7c0a5681d734c0f8ba680b4e7173d87))

- Implement column mapping to change the filter name to the database filed
  ([`f0de9ad`](https://github.com/adriamontoto/criteria-pattern/commit/f0de9ad1c00b72394eb82792479eaf770b37e733))

- Implement columns injection prevention
  ([`a88b54c`](https://github.com/adriamontoto/criteria-pattern/commit/a88b54c90bdebe4da025e94d313f7a8379bb6cd5))

- Implement converter interface
  ([`c8a33ca`](https://github.com/adriamontoto/criteria-pattern/commit/c8a33cab614a234e9be082950bd7364f8531c4f5))

- Implement criteria field injection prevention
  ([`d89b693`](https://github.com/adriamontoto/criteria-pattern/commit/d89b6937e4196dda9750f94e1f739ef74066bb60))

- Implement criteria pattern class
  ([`9a9c5e0`](https://github.com/adriamontoto/criteria-pattern/commit/9a9c5e0b2a6b5b8d541c813c28703fb446f402d5))

- Implement criteria to raw sql queries
  ([`b32c6d4`](https://github.com/adriamontoto/criteria-pattern/commit/b32c6d470286c0816bec54d4122e71452aabe758))

- Implement filter and filter operator
  ([`e9c77ed`](https://github.com/adriamontoto/criteria-pattern/commit/e9c77eda96fc73346b801d58dc6c1afa4997f4f2))

- Implement not criteria logic
  ([`3743da3`](https://github.com/adriamontoto/criteria-pattern/commit/3743da3232fc804f66e2390826f92905a5763305))

- Implement or logic with OrCriteria class
  ([`8f8eef7`](https://github.com/adriamontoto/criteria-pattern/commit/8f8eef70bc3d53e35d1318e631a20e73716866af))

- Implement order to criteria
  ([`6ba9c63`](https://github.com/adriamontoto/criteria-pattern/commit/6ba9c63487ff45a8bc5a8fcc526f16ed907d568e))

- Implement table injection prevention
  ([`6afa1fc`](https://github.com/adriamontoto/criteria-pattern/commit/6afa1fcd381fc4995d0cc3ff3d09633609ced4c7))

- Improve Filter and Order string representations
  ([`2f19cde`](https://github.com/adriamontoto/criteria-pattern/commit/2f19cde9a26608ef5384d7a9f4c1c952c00e83dc))

- Improve sqlalchemy converter type hints
  ([`a818c7c`](https://github.com/adriamontoto/criteria-pattern/commit/a818c7c6800bf3937922c10b0fe405f5a97c6694))

- Prevent sql injection in sql converter where clauses
  ([`7288844`](https://github.com/adriamontoto/criteria-pattern/commit/7288844e57435c8fcc423b685cdfe51eacf59c92))

- Remove converter interface
  ([`bbcb5ef`](https://github.com/adriamontoto/criteria-pattern/commit/bbcb5efc4dd7f9ad830c8a1b432e5e49dacfc73e))

- Remove sqlalchemy support
  ([`43827dc`](https://github.com/adriamontoto/criteria-pattern/commit/43827dc24319ace2e4b6d848b1bafc2b1783fa19))

- Remove support of IN operator
  ([`a8aa308`](https://github.com/adriamontoto/criteria-pattern/commit/a8aa308497601880e77c2e3661929edc3a371584))

- Repository configuration
  ([`a4b344a`](https://github.com/adriamontoto/criteria-pattern/commit/a4b344a2ff1333296f5b7d95f496eb96b414bebc))

- Support select all columns with *
  ([`302f834`](https://github.com/adriamontoto/criteria-pattern/commit/302f83473dde205c02e1fbc47fcdc10fd6025dcb))
