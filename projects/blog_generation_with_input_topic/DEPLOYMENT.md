# Deployment Guide

## Overview
This guide covers different deployment options for the Blog Generation API, from local development to production environments.

## Local Development

### Quick Start
```bash
# Navigate to project directory
cd /Users/kausik/Desktop/Agentic-AI/projects/blog_generation_with_input_topic

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Edit with your API keys

# Run the server
python app.py
```

### Development with Auto-reload
```bash
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

## Environment Configuration

### Required Environment Variables
Create a `.env` file in the project root:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here

# Optional
LANGSMITH_PROJECT_NAME=blog-generation
LANGSMITH_TRACING=true
```

### Getting API Keys

**Groq API Key**:
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login
3. Navigate to API Keys section
4. Create a new API key

**LangChain API Key**:
1. Visit [LangSmith](https://smith.langchain.com/)
2. Sign up/Login
3. Go to Settings → API Keys
4. Generate a new API key

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "app.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  blog-generator:
    build: .
    ports:
      - "8001:8001"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
    env_file:
      - .env
```

### Build and Run
```bash
# Build the image
docker build -t blog-generator .

# Run the container
docker run -p 8001:8001 --env-file .env blog-generator

# Or use docker-compose
docker-compose up -d
```

## Cloud Deployment

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-blog-generator
heroku config:set GROQ_API_KEY=your_key
heroku config:set LANGCHAIN_API_KEY=your_key
git push heroku main
```

### AWS Lambda (Serverless)
```bash
# Install serverless framework
npm install -g serverless

# Create serverless.yml
# Deploy
serverless deploy
```

## Production Considerations

### Performance Optimization
- Use a production WSGI server like Gunicorn
- Implement connection pooling
- Add caching for repeated requests
- Set up load balancing for high traffic

### Security
- Add API authentication/authorization
- Implement rate limiting
- Use HTTPS in production
- Validate and sanitize inputs
- Set up CORS properly

### Monitoring
- Enable LangSmith tracing
- Set up application logs
- Monitor API response times
- Track error rates
- Set up health checks

### Example Production Setup
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8001
```

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use container orchestration (Kubernetes, Docker Swarm)
- Implement service mesh for microservices

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize LLM inference settings
- Use GPU acceleration if available

## Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Find process using port 8001
lsof -i :8001
# Kill the process
kill -9 <PID>
```

**Environment Variables Not Loaded**:
```bash
# Verify .env file exists and has correct format
cat .env
# Check if variables are accessible
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

**Dependencies Issues**:
```bash
# Clean install
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## Health Checks

Add a health check endpoint to your FastAPI app:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

## Backup and Recovery

### Configuration Backup
- Store environment variables securely
- Version control your deployment scripts
- Document your infrastructure setup

### Data Backup
- Currently stateless, no data backup needed
- Consider logging requests/responses for analysis