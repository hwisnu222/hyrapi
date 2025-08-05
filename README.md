# Hyrapi

Hyrapi is a CLI-based REST API client powered by a YAML collection file. It's designed to simplify making HTTP requests by organizing endpoints, headers, tokens, and parameters in a single configuration file.

## Installation

You can install `hyr` in two ways:

### Method 1: Manual Installation

```
git clone https://github.com/hwisnu222/hyrapi.git
cd hyrapi
make build
cd dist/
chmod +x hyr
sudo mv hyr /usr/local/bin/
```

### Method 2: One-Line Install Script

```
curl -fsSL https://raw.githubusercontent.com/hwisnu222/hyrapi/main/install.sh | sh
```

## Usage

To use `hyrapi`, you need to provide a YAML collection file:

```
hyr -c collections.yml
```

## Sample `collections.yml`

```
servers:
  - url: http://localhost:3000/api/v1
    description: development

variables:
  token: token

paths:

  - endpoint: /incomes
    name: getIncomes
    method: GET
    auth:
      type: bearer
      token: "{{token}}"
    headers:
      Content-Type: application/json

  - endpoint: /incomes/4
    name: deleteIncomes
    method: DELETE
    auth:
      type: bearer
      token: "{{token}}"
    headers:
      Content-Type: application/json
```

## Structure Explained

### `servers`

Defines base URLs for your API. You can use multiple environments (dev, staging, prod).

### `variables`

Declare reusable variables like tokens, API keys, etc.

### `paths`

List of API requests:

- `endpoint`: the path to the API route
- `name`: a label to identify this request
- `method`: HTTP method (`GET`, `POST`, `PUT`, `DELETE`, etc.)
- `auth`: authentication configuration
  - `type`: `bearer` (currently supported)
  - `token`: value or reference using `{{variable}}`
- `headers`: optional headers to send with the request

## Features

- YAML-based API collection
- Built-in support for Bearer Token authentication
- Easily switch between environments
- CLI interface for fast request execution

## Roadmap Ideas (Planned Features)

- Support for:
  - `basic` and `custom` auth types
  - Request body for `POST`, `PUT`, `PATCH`
  - Path parameters and query strings
  - Response highlighting
  - Response time and size display
- Collection management (similar to Postman)
- Output formatting (JSON / Table / Raw)

## Author

Hyrapi by [@hwisnu222](https://github.com/hwisnu222)

Contributions and feedback are welcome!
