# Collections

## Servers

You can define multiple servers for different environments such as development, staging, or production.

```yaml
servers:
  - url: http://localhost:3000/api/v1
    name: development
    description: Development server
  - url: http://example.com/api/v1
    name: staging
    description: Staging server
```

## Variables

You can define global or environment-specific (local) variables.

### Global Variables

```yaml
variables:
  key: key_value # Global variable
```

### Local Variables (Per Environment)

You can define variables scoped to specific environments.

```yaml
variables:
  development:
    token: key_value # Local variable, available only for the development environment
```

To access variables, use this syntax:

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    auth:
      type: bearer
      token: "{{token}}"
```

## Headers

To define request headers (such as `Content-Type`), you can configure them per path.

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    headers:
      Content-Type: application/json
      # Content-Type: application/x-www-form-urlencoded
```

## Authentication

You can define authentication for each endpoint as follows:

### Bearer Token

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    auth:
      type: bearer
      token: "{{token}}"
```

### Basic Auth

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    auth:
      type: basic
      username: "{{username}}"
      password: "{{password}}"
```

### API Key (Header)

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    auth:
      type: apikey
      api_key: abc123
      api_key_header: X-API-Key
```

This will send the header:  
`X-API-Key: abc123`

You can customize the header name using `api_key_header`.

### Digest Authentication

```yaml
paths:
  - endpoint: /posts
    name: getPosts
    auth:
      type: digest
      username: admin
      password: secret
```
