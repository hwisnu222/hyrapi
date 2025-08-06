<div align="center">
  <h1>Hyrapi</h1>
  <div align="center">
    <img src="https://img.shields.io/badge/CLI-Rest%20API-green?style=flat-square" alt="Badge">
    <img src="https://img.shields.io/badge/Version-v1.1.0-orange?style=flat-square" alt="Badge">
  </div>
</div>
**Hyrapi** is a CLI-based REST API client powered by a YAML collection file. It helps you organize and execute API requests by grouping endpoints, headers, tokens, and authentication configs in a single file.

---

## Installation

### Method 1: Manual

```bash
git clone https://github.com/hwisnu222/hyrapi.git
cd hyrapi
make build
cd dist/
chmod +x hyr
sudo mv hyr /usr/local/bin/
```

### Method 2: One-Line Script

```bash
curl -fsSL https://raw.githubusercontent.com/hwisnu222/hyrapi/main/install.sh | sh
```

---

## Usage

Run `hyr` with a YAML config file:

```bash
hyr -c collections.yml
```

### List all servers:

```bash
hyr -c collections.yml -s
```

### List all paths:

```bash
hyr -c collections.yml -p
```

---

## Sample `collections.yml`

```yaml
servers:
  - url: http://localhost:3000/api/v1
    name: development
    description: Development Server
  - url: http://example.com/api/v1
    name: staging
    description: Staging Server
  - url: http://example.com/api/v1
    name: production
    description: Production Server

variables:
  global_token: abc123 # global variable
  development:
    token: dev_token_value # scoped to 'development'
  staging:
    token: staging_token_value
  production:
    token: production_token_value

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

---

## Configuration Reference

### `servers`

Defines base URLs grouped by environment:

```yaml
servers:
  - url: http://localhost:3000/api
    name: development
    description: Dev server
```

### `variables`

Reusable values, defined globally or per-environment:

```yaml
variables:
  token: abc123 # global
  development:
    token: devtoken123 # only for development
```

To reference variables: `{{token}}`

---

## `paths`

Defines API requests:

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    method: GET
    auth:
      type: bearer
      token: "{{token}}"
    headers:
      Content-Type: application/json
```

Supported fields:

| Field      | Description                   |
| ---------- | ----------------------------- |
| `endpoint` | Relative path of API route    |
| `name`     | Identifier for the request    |
| `method`   | HTTP method (GET, POST, etc.) |
| `auth`     | Auth config (see below)       |
| `headers`  | Optional custom headers       |

---

## Authentication Options

Hyrapi supports multiple authentication types:

### Bearer Token

```yaml
auth:
  type: bearer
  token: "{{token}}"
```

Sends `Authorization: Bearer <token>`.

### Basic Auth

```yaml
auth:
  type: basic
  username: admin
  password: secret
```

Sends base64-encoded `Authorization: Basic`.

### API Key (Header-based)

```yaml
auth:
  type: apikey
  api_key: abc123
  api_key_header: X-API-Key
```

Sends `X-API-Key: abc123`. Header name is customizable.

### Digest Auth

```yaml
auth:
  type: digest
  username: admin
  password: secret
```

Sends HTTP Digest Authentication headers.

---

## Features

- YAML-based API request collection
- Multiple environments (dev/staging/prod)
- Built-in support for Bearer, Basic, Digest, and API Key auth
- Variable interpolation
- CLI commands:
  - `-s`: list servers
  - `-p`: list all paths

---

## Roadmap (Planned Features)

- Request body support for `POST`, `PUT`, `PATCH`
- Path/query parameter support
- Response highlighting
- Time and size measurement
- Collection/file manager (like Postman)
- Output formatter (raw / table / JSON)

---

## Author

Hyrapi by [@hwisnu222](https://github.com/hwisnu222)  
Contributions and feedback are welcome!
