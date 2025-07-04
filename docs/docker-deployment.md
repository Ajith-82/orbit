# ORBIT Docker Setup Guide

This guide will help you get ORBIT up and running with Docker in minutes. ORBIT is a flexible AI server that supports multiple inference providers, vector databases, and embedding models.

## Table of Contents
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running ORBIT](#running-orbit)
- [Managing ORBIT](#managing-orbit)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git** (to clone the repository)
- **4GB+ RAM** available for Docker
- **10GB+ disk space** for models and data

Verify your installation:
```bash
docker --version
docker compose version  # or docker-compose --version
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd orbit
```

### 2. Make Scripts Executable

```bash
chmod +x docker-init.sh orbit-docker.sh
```

### 3. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` to add your API keys (only if using commercial providers):
```bash
# Edit with your preferred editor
nano .env
# or
vim .env
```

### 4. Choose Your Setup Profile

ORBIT supports different dependency profiles:

| Profile | Description | Use Case |
|---------|-------------|----------|
| `minimal` | Core dependencies only | Local Ollama inference |
| `torch` | Includes PyTorch dependencies | GPU-accelerated inference |
| `commercial` | Commercial provider SDKs | OpenAI, Anthropic, etc. |
| `all` | Everything included | Maximum flexibility |

### 5. Initialize ORBIT

Basic setup with minimal profile:
```bash
./docker-init.sh --build --profile minimal
```

Setup with all features:
```bash
./docker-init.sh --build --profile all
```

Setup with GGUF model download:
```bash
./docker-init.sh --build --profile minimal --download-gguf
```

## Configuration

### Understanding Config Files

ORBIT uses YAML configuration files to control its behavior. The main sections are:

- **general**: Server settings, ports, providers
- **inference**: LLM provider configurations
- **datasources**: Vector database settings
- **embeddings**: Embedding model configurations
- **adapters**: Query processing pipelines

### Config File Locations

```
orbit/
├── config.yaml           # Default config file
├── configs/              # Directory for multiple configs
│   ├── minimal.yaml      # Minimal setup
│   ├── development.yaml  # Development with verbose logging
│   ├── production.yaml   # Production-ready config
│   └── commercial.yaml   # Commercial providers config
```

### Using Custom Configs

Start ORBIT with a specific config:
```bash
# During initialization
./docker-init.sh --build --config configs/production.yaml

# Or when running
./orbit-docker.sh start --config configs/production.yaml
```

### Important Docker Config Settings

When using Docker, ensure your config uses Docker service names instead of `localhost`:

```yaml
# Correct for Docker
inference:
  ollama:
    base_url: "http://ollama:11434"  # NOT http://localhost:11434

datasources:
  chroma:
    host: "chroma"  # NOT localhost
    port: 8000

internal_services:
  mongodb:
    host: "mongodb"  # NOT localhost
    port: 27017
```

## Running ORBIT

### Starting ORBIT

Use the `orbit-docker.sh` helper script:

```bash
# Start with default config
./orbit-docker.sh start

# Start with specific config
./orbit-docker.sh start --config configs/production.yaml

# Start with different profile
./orbit-docker.sh start --profile commercial

# Start on different port
./orbit-docker.sh start --port 8080

# Start in foreground (see logs)
./orbit-docker.sh start --attach
```

### Checking Status

```bash
# View container status
./orbit-docker.sh status

# Check health endpoint
curl http://localhost:3000/health
```

### Viewing Logs

```bash
# View recent logs
./orbit-docker.sh logs

# Follow logs in real-time
./orbit-docker.sh logs --follow

# Using docker-compose directly
docker compose logs -f orbit-server
```

### Stopping ORBIT

```bash
# Stop all services
./orbit-docker.sh stop

# Or using docker-compose
docker compose down
```

## Managing ORBIT

### API Key Management

ORBIT supports API key authentication for secure access:

```bash
# Create a new API key
./orbit-docker.sh cli key create --name "my-app"

# List all API keys
./orbit-docker.sh cli key list

# Delete an API key
./orbit-docker.sh cli key delete <key-id>
```

### Using the CLI

Access ORBIT's CLI tools inside the container:

```bash
# Get CLI help
./orbit-docker.sh cli --help

# Check server status
./orbit-docker.sh cli status

# Run any orbit command
./orbit-docker.sh cli <command> [options]
```

### Accessing Container Shell

```bash
# Open bash shell in container
./orbit-docker.sh exec bash

# Run specific commands
./orbit-docker.sh exec ls -la /app/logs
```

## Advanced Usage

### Using Multiple Configurations

Create different configs for different scenarios:

```bash
# Development setup
./orbit-docker.sh start --config configs/development.yaml

# Switch to production
./orbit-docker.sh stop
./orbit-docker.sh start --config configs/production.yaml
```

### Persistent Data

ORBIT stores data in Docker volumes:
- `mongodb-data`: API keys and metadata
- `ollama-data`: Downloaded models
- `chroma-data`: Vector embeddings

To backup data:
```bash
# Backup volumes
docker run --rm -v orbit_mongodb-data:/data -v $(pwd):/backup alpine tar czf /backup/mongodb-backup.tar.gz -C /data .
```

### Using Commercial Providers

1. Add API keys to `.env`:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

2. Use commercial profile:
```bash
./docker-init.sh --build --profile commercial
```

3. Update config to use commercial provider:
```yaml
general:
  inference_provider: "openai"  # or "anthropic", "gemini", etc.
```

### GPU Support

For GPU acceleration with NVIDIA:

1. Install NVIDIA Container Toolkit
2. Use the torch profile:
```bash
./docker-init.sh --build --profile torch
```

3. Update docker-compose.yml to add GPU support:
```yaml
orbit-server:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

## Making API Requests

### Basic Chat Request

```bash
curl -X POST http://localhost:3000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "What is ORBIT?",
    "session_id": "test-session"
  }'
```

### With API Key

```bash
curl -X POST http://localhost:3000/v1/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: orbit_your-key-here' \
  -d '{
    "message": "Tell me about vector databases"
  }'
```

### Streaming Response

```bash
curl -X POST http://localhost:3000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Explain quantum computing",
    "stream": true
  }'
```

## Troubleshooting

### Common Issues

#### 1. Services Won't Start

Check logs for specific service:
```bash
docker compose logs mongodb
docker compose logs ollama
docker compose logs chroma
```

#### 2. Ollama Model Not Found

Pull the model manually:
```bash
docker exec -it orbit-ollama ollama pull llama3.2
```

#### 3. Permission Errors

Fix permissions on directories:
```bash
sudo chown -R $USER:$USER logs data gguf
```

#### 4. Port Already in Use

Change the port in `.env`:
```bash
ORBIT_PORT=3001
```

Or when running:
```bash
./orbit-docker.sh start --port 3001
```

#### 5. Out of Memory

Increase Docker memory limit in Docker Desktop settings or:
```bash
# Check current usage
docker stats

# Restart with memory limits
docker compose down
docker compose up -d
```

#### 6. Database Service Issues (MongoDB/Redis)

If ORBIT server won't start and gets stuck waiting for dependencies:

**Check service status:**
```bash
# Check which services are running vs created
docker compose ps -a

# Look for services with "Created" status instead of "Running (healthy)"
```

**Check database logs:**
```bash
# Check MongoDB logs
docker compose logs mongodb

# Check Redis logs  
docker compose logs redis

# Follow logs in real-time
docker compose logs -f redis mongodb
```

**Identify port conflicts:**
```bash
# Check if Redis port is in use
sudo lsof -i :6379

# Check if MongoDB port is in use  
sudo lsof -i :27017

# Check ORBIT port
sudo lsof -i :3000
```

**Resolve port conflicts:**
```bash
# Stop system Redis service (if conflicting)
sudo systemctl stop redis-server
sudo systemctl disable redis-server

# Stop system MongoDB service (if conflicting)
sudo systemctl stop mongod
sudo systemctl disable mongod

# Verify ports are free
sudo lsof -i :6379
sudo lsof -i :27017
```

**Manual service startup for debugging:**
```bash
# Try starting Redis manually to see errors
docker compose up redis

# Try starting MongoDB manually
docker compose up mongodb

# Check container networking
docker network ls
docker network inspect orbit_orbit-network
```

**Test database connectivity:**
```bash
# Test Redis connection
docker exec -it orbit-redis redis-cli ping

# Test MongoDB connection  
docker exec -it orbit-mongodb mongosh --eval "db.adminCommand('ping')"
```

### Debug Mode

Enable verbose logging:

1. Update config.yaml:
```yaml
general:
  verbose: true
logging:
  level: "DEBUG"
```

2. Restart ORBIT:
```bash
./orbit-docker.sh restart
```

### Health Checks

Monitor service health:
```bash
# Check all services
docker compose ps

# Test individual services
curl http://localhost:11434/api/health  # Ollama
curl http://localhost:8000/api/v1/heartbeat  # Chroma
```

### Resetting Everything

To start completely fresh and test the full initialization process:

#### Complete Reset (Recommended)
```bash
# Stop the containers
docker rm -f orbit-server orbit-mongodb orbit-redis

# Stop and remove all containers
docker compose down

# Clean up unused Docker objects (containers, networks, images)
docker system prune -f

# Remove all unused volumes (WARNING: Deletes all data)
docker volume prune -f

# Remove the ORBIT server image to force rebuild
docker rmi orbit-server:latest mongo:8.0 redis:7.2

# Verify clean state (should show no containers)
docker ps -a

# Now rebuild from scratch
./docker-init.sh --build --profile minimal --download-gguf gguf-model.gguf
```

#### Quick Reset (Keeps Images)
```bash
# Stop and remove containers + volumes
docker compose down -v

# Restart fresh
./docker-init.sh --build --profile minimal
```

#### Nuclear Option (Complete Docker Reset)
If you're still having issues, reset Docker completely:
```bash
# Stop Docker service
sudo systemctl stop docker

# Remove all Docker data (WARNING: Removes EVERYTHING!)
sudo rm -rf /var/lib/docker

# Start Docker service
sudo systemctl start docker

# Rebuild everything
./docker-init.sh --build --profile minimal
```

#### Verify Clean Environment
Before running docker-init.sh, ensure no port conflicts:
```bash
# Check for existing services on required ports
sudo lsof -i :3000   # ORBIT
sudo lsof -i :6379   # Redis
sudo lsof -i :27017  # MongoDB

# Stop any conflicting services
sudo systemctl stop redis-server
sudo systemctl stop mongod
```

### 6. Docker overlay2 Storage Error

If you see an error like:

```
failed to solve: failed to read dockerfile: failed to prepare  as <id>: symlink ../<id>/diff /opt/dlami/nvme/docker/overlay2/l/<id>: no such file or directory
```

This indicates a problem with Docker's internal overlay2 storage, often due to corruption or missing files. This is not a problem with your code or Dockerfile, but with Docker's storage backend.

#### Solution (Non-Destructive First)

Try cleaning up unused Docker objects:

```bash
docker system prune -a --volumes
```

If the problem persists, you may need to reset Docker's storage (WARNING: this will delete all containers, images, and volumes!):

#### Solution (Destructive - Resets Docker Storage)

```bash
sudo systemctl stop docker
sudo rm -rf /var/lib/docker/overlay2
sudo rm -rf /var/lib/docker/containers
sudo systemctl start docker
```

Then rebuild your images:

```bash
./docker-init.sh --build --profile minimal --download-gguf
```

**Warning:** The destructive solution will remove all Docker data. Back up any important data before proceeding.

Happy Orbiting! 🚀