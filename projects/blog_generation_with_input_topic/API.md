# API Documentation

## Overview
This document provides detailed information about the Blog Generation API endpoints and usage.

## Base URL
```
http://localhost:8001
```

## Authentication
Currently, no authentication is required. API keys are configured via environment variables.

## Endpoints

### Generate Blog Post

**Endpoint**: `POST /blogs`

**Description**: Generates a complete blog post with title and content based on the provided topic.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
    "topic": "string (required) - The topic for blog generation"
}
```

**Response Format**:
```json
{
    "data": {
        "topic": "string - The input topic",
        "blog": {
            "title": "string - Generated blog title in markdown",
            "content": "string - Generated blog content in markdown"
        },
        "current_language": "string - Language setting (optional)"
    }
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8001/blogs" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Machine Learning in Finance"}'
```

**Example Response**:
```json
{
    "data": {
        "topic": "Machine Learning in Finance",
        "blog": {
            "title": "# Transforming Finance: The Machine Learning Revolution",
            "content": "## Introduction\n\nMachine Learning is revolutionizing the financial industry...\n\n## Key Applications\n\n### 1. Fraud Detection\n...\n\n### 2. Algorithmic Trading\n...\n\n## Conclusion\n..."
        }
    }
}
```

## Error Handling

### Common Error Responses

**400 Bad Request**:
```json
{
    "detail": "Missing required field: topic"
}
```

**500 Internal Server Error**:
```json
{
    "detail": "Error occurred with LLM processing"
}
```

## Rate Limiting
Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## Development Testing

### Using curl
```bash
# Test the blog generation endpoint
curl -X POST "http://localhost:8001/blogs" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Artificial Intelligence Ethics"}'
```

### Using Python requests
```python
import requests
import json

url = "http://localhost:8001/blogs"
payload = {"topic": "Sustainable Technology Trends"}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

### Using JavaScript fetch
```javascript
fetch('http://localhost:8001/blogs', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        topic: 'Future of Renewable Energy'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```