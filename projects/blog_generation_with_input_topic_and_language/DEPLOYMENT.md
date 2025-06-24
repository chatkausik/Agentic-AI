# Deployment Guide

## Overview
This guide covers deployment options for the Multilingual Blog Generation API, from local development to production environments.

## Prerequisites

### Required API Keys
- **Groq API Key**: Get from [Groq Console](https://console.groq.com/)
- **LangChain API Key**: Get from [LangSmith](https://smith.langchain.com/) (optional, for tracing)

### System Requirements
- Python 3.13+
- 2GB+ RAM (for LLM operations)
- Stable internet connection

## Local Development

### Quick Start
```bash
# Navigate to project directory
cd /Users/kausik/Desktop/Agentic-AI/projects/blog_generation_with_input_topic_and_language

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp _copy.env .env
# Edit .env with your API keys

# Run the server
python app.py
```

The server starts on `http://localhost:8002`

### Development with Auto-reload
```bash
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```

## Environment Configuration

### Environment Variables (.env)
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (for tracing and monitoring)
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGSMITH_PROJECT_NAME=blog-generation-multilingual
LANGSMITH_TRACING=true
```

## Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8002

# Run the application
CMD ["python", "app.py"]
```

### Docker Compose Setup
```yaml
version: '3.8'
services:
  blog-generator-multilingual:
    build: .
    ports:
      - "8002:8002"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - LANGSMITH_PROJECT_NAME=blog-generation-multilingual
    env_file:
      - .env
    restart: unless-stopped
```

### Build and Run
```bash
# Build the image
docker build -t blog-generator-multilingual .

# Run the container
docker run -p 8002:8002 --env-file .env blog-generator-multilingual

# Or use docker-compose
docker-compose up -d
```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8002
```

### Production Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy source code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8002

# Production command
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8002"]
```

## Cloud Deployment Options

### 1. Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Set environment variables
railway variables set GROQ_API_KEY=your_key
railway variables set LANGCHAIN_API_KEY=your_key

# Deploy
railway up
```

### 2. Heroku
```bash
# Create Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:\$PORT" > Procfile

# Create app
heroku create your-blog-generator-multilingual

# Set environment variables
heroku config:set GROQ_API_KEY=your_key
heroku config:set LANGCHAIN_API_KEY=your_key

# Deploy
git push heroku main
```

### 3. Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/blog-generator-multilingual

# Deploy to Cloud Run
gcloud run deploy blog-generator-multilingual \
  --image gcr.io/PROJECT_ID/blog-generator-multilingual \
  --platform managed \
  --port 8002 \
  --set-env-vars GROQ_API_KEY=your_key,LANGCHAIN_API_KEY=your_key
```

### 4. AWS ECS/Fargate
```bash
# Create task definition
# Deploy using AWS CLI or CDK
aws ecs create-service \
  --cluster your-cluster \
  --service-name blog-generator-multilingual \
  --task-definition blog-generator:1 \
  --desired-count 2
```

## Production Considerations

### Performance Optimization
- **Worker Configuration**: Use 2-4 workers based on CPU cores
- **Memory Management**: Monitor memory usage during LLM operations
- **Response Caching**: Consider caching similar topic requests
- **Load Balancing**: Use multiple instances for high traffic

### Security Best Practices
- **API Keys**: Store securely using cloud secret managers
- **HTTPS**: Always use TLS in production
- **Rate Limiting**: Implement to prevent abuse
- **Input Validation**: Sanitize topic inputs
- **CORS**: Configure properly for web clients

### Example Security Headers
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

### Monitoring and Observability

#### Health Check Endpoint
Add to your `app.py`:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

#### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

#### LangSmith Tracing
Ensure environment variables are set:
```env
LANGCHAIN_API_KEY=your_key
LANGSMITH_PROJECT_NAME=blog-generation-multilingual-prod
LANGSMITH_TRACING=true
```

## Scaling Strategies

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use container orchestration (Kubernetes, ECS)
- Implement service discovery

### Vertical Scaling
- Increase CPU/RAM for faster LLM processing
- Use GPU instances if supported by Groq
- Optimize worker count based on resources

### Database Considerations
Currently stateless, but consider adding:
- Request/response caching (Redis)
- User management (PostgreSQL)
- Analytics storage (ClickHouse)

## Troubleshooting

### Common Production Issues

**Port Conflicts:**
```bash
# Check port usage
netstat -tulpn | grep :8002
# Or with lsof
lsof -i :8002
```

**Memory Issues:**
```bash
# Monitor memory usage
docker stats
# Or for processes
top -p $(pgrep -f "python app.py")
```

**Environment Variables:**
```bash
# Verify in container
docker exec -it container_name env | grep GROQ
```

**API Connectivity:**
```bash
# Test Groq API access
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

### Error Monitoring
Consider integrating:
- **Sentry**: For error tracking
- **Prometheus**: For metrics collection
- **Grafana**: For visualization
- **DataDog**: For comprehensive monitoring

## Backup and Recovery

### Configuration Backup
- Environment variables in secure vault
- Infrastructure as Code (Terraform/CDK)
- Deployment scripts in version control

### Disaster Recovery
- Multi-region deployment
- API key rotation procedures
- Rollback strategies

## Cost Optimization

### Groq API Usage
- Monitor token consumption
- Implement request caching
- Use appropriate model sizes
- Set usage limits/alerts

### Infrastructure Costs
- Use auto-scaling groups
- Implement graceful shutdown
- Monitor resource utilization
- Use spot instances where appropriate