# API Documentation

## Overview
The Multilingual Blog Generation API provides endpoints for generating blog content with optional translation capabilities using LangGraph workflows.

## Base URL
```
http://localhost:8002
```

## Authentication
Currently, no authentication is required. API keys are configured server-side through environment variables.

## Endpoints

### Generate Blog Content

**POST** `/blogs`

Generate a blog post based on a given topic, with optional translation to supported languages.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | Yes | The topic for blog generation |
| `language` | string | No | Target language for translation (`hindi`, `french`) |

**Example Requests:**

1. **Topic-only generation:**
```json
{
  "topic": "Machine Learning in Finance"
}
```

2. **Topic with translation:**
```json
{
  "topic": "Sustainable Energy Solutions",
  "language": "hindi"
}
```

#### Response

**Success Response (200 OK):**
```json
{
  "data": {
    "topic": "string",
    "blog": {
      "title": "string",
      "content": "string"
    },
    "current_language": "string"
  }
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `data.topic` | string | The input topic |
| `data.blog.title` | string | Generated blog title (Markdown formatted) |
| `data.blog.content` | string | Generated blog content (Markdown formatted) |
| `data.current_language` | string | Language of the content |

**Error Responses:**

**400 Bad Request:**
```json
{
  "detail": "Invalid request format"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error generating blog content"
}
```

## Supported Languages

Currently supported translation languages:
- `hindi` - Hindi translation
- `french` - French translation

## Content Format

All generated content uses Markdown formatting with:
- Headers for structure (`#`, `##`, `###`)
- Bullet points for lists
- Bold text for emphasis
- Code blocks where appropriate

## Rate Limits

Currently no rate limits are implemented. Consider implementing rate limiting for production use.

## Examples

### cURL Examples

**Generate English blog:**
```bash
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Benefits of Remote Work"
  }'
```

**Generate blog with Hindi translation:**
```bash
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Benefits of Remote Work",
    "language": "hindi"
  }'
```

### Python Example

```python
import requests
import json

# Generate blog with translation
url = "http://localhost:8002/blogs"
payload = {
    "topic": "Artificial Intelligence Ethics",
    "language": "french"
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    blog = data["data"]["blog"]
    print(f"Title: {blog['title']}")
    print(f"Content: {blog['content']}")
else:
    print(f"Error: {response.status_code}")
```

### JavaScript Example

```javascript
const generateBlog = async (topic, language = null) => {
  const payload = { topic };
  if (language) payload.language = language;
  
  try {
    const response = await fetch('http://localhost:8002/blogs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.data.blog;
    } else {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error generating blog:', error);
  }
};

// Usage
generateBlog("Blockchain Technology", "hindi")
  .then(blog => console.log(blog));
```

## Workflow Details

### Topic-only Workflow
1. **Title Creation** - Generates SEO-friendly title
2. **Content Generation** - Creates detailed blog content

### Topic + Language Workflow
1. **Title Creation** - Generates SEO-friendly title
2. **Content Generation** - Creates detailed blog content
3. **Language Routing** - Determines translation path
4. **Translation** - Translates content to target language

## Performance Considerations

- Average response time: 5-15 seconds (depending on content length)
- Concurrent requests: Limited by LLM API rate limits
- Content length: Typically 500-2000 words per blog post

## Error Handling

The API handles various error scenarios:
- Invalid JSON format
- Missing required parameters
- LLM API failures
- Network timeouts
- Invalid language codes

For production use, implement proper error logging and monitoring.