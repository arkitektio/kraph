# CHANGELOG


## v0.2.0 (2025-07-24)

### Bug Fixes

- Refactor datalayer and rath context management; update execute and subscribe functions
  ([`7803ffe`](https://github.com/arkitektio/kraph/commit/7803ffe657b8e8c7253fed6df9df04ca4e671cad))

- Updated the `__aexit__` method in `DataLayer` and `KraphRath` to include type hints and return
  None. - Refactored `execute` and `subscribe` functions in `funcs.py` to use type hints and
  improved error handling. - Changed `adownload_file` and `download_file` functions in `io.py` to
  require a non-optional `file_name`. - Removed unused imports and unnecessary code in `kraph.py`
  and `scalars.py`. - Updated dependencies in `pyproject.toml` and `uv.lock` to use `dokker` version
  2.1.1. - Deleted unused `utils.py` file to clean up the codebase.

### Features

- Add unitests and pairs
  ([`e331d86`](https://github.com/arkitektio/kraph/commit/e331d86068316f47803d85dc07d058035c5fe6ff))

- Updated arkitekt stack
  ([`151ed10`](https://github.com/arkitektio/kraph/commit/151ed10a041b9286536dc2cd7c8ce55e9e3a47e6))


## v0.1.0 (2025-05-11)

### Features

- Enhance import handling and update dependencies for improved functionality
  ([`b1067ad`](https://github.com/arkitektio/kraph/commit/b1067ad6b1f898d6e5ea9dc737a89738817c34c1))

- Refactor code structure for improved readability and maintainability
  ([`f2714f8`](https://github.com/arkitektio/kraph/commit/f2714f81f75520331a42b3bec74c6dca89bc0924))

- Remove integration test exclusion from CI workflows
  ([`66fe07d`](https://github.com/arkitektio/kraph/commit/66fe07d5339c08bc3e8d60508c3a93591daf5309))

- Update README with project description and features
  ([`974e3d8`](https://github.com/arkitektio/kraph/commit/974e3d83048be355b7938f807106b36516f269f0))
