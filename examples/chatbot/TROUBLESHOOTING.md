# Troubleshooting Guide

Common issues and solutions for the MemMachine chatbot.

## Issue: 500 Internal Server Error

### Symptoms
```
ERROR - Failed to add memory: 500 - Internal Server Error
ERROR - Failed to search memory: 500 - Internal Server Error
```

### Cause
MemMachine server is missing the `sentence-transformers` package required for the reranker.

### Solution

**Option 1: Fix Running Docker Container (Quick)**
```bash
# Install the missing package
docker exec memmachine-app pip install sentence-transformers

# Restart MemMachine
docker restart memmachine-app

# Wait a few seconds, then verify
curl http://localhost:8080/health
```

**Option 2: Rebuild Docker Image (Permanent)**
```bash
# Edit docker-compose.yml or Dockerfile to include sentence-transformers
# Then rebuild:
docker-compose down
docker-compose build
docker-compose up -d
```

**Option 3: Disable Reranker (Workaround)**

Edit your `configuration.yml`:
```yaml
reranker:
  type: "none"  # Disable reranker
```

Then restart MemMachine.

## Issue: Connection Refused

### Symptoms
```
Failed to connect to MemMachine API
```

### Solution
```bash
# Check if MemMachine is running
docker ps | grep memmachine

# If not running, start it
docker-compose up -d

# Check health
curl http://localhost:8080/health
```

## Issue: Health Check at Wrong Endpoint

### Symptoms
```
Failed to connect: 404 Not Found at /v1/health
```

### Solution
The health endpoint is at `/health` (not `/v1/health`). This has been fixed in the latest version of `memmachine_chatbot.py`.

Update your code or pull the latest version.

## Issue: OpenAI API Key Not Found

### Symptoms
```
❌ OPENAI_API_KEY not found!
```

### Solution
```bash
# Set the API key
export OPENAI_API_KEY='sk-your-key-here'

# Or add to your shell profile for persistence
echo "export OPENAI_API_KEY='sk-your-key-here'" >> ~/.zshrc
source ~/.zshrc
```

## Issue: Required Fields Missing

### Symptoms
```
Field required: group_id
Field required: metadata
```

### Solution
The API requires all fields to be present. The chatbot has been updated to include these automatically. Make sure you're using the latest version of `memmachine_chatbot.py`.

## Checking MemMachine Logs

```bash
# View recent logs
docker logs memmachine-app --tail 50

# Follow logs in real-time
docker logs memmachine-app -f

# Search for errors
docker logs memmachine-app 2>&1 | grep -i error
```

## Quick Diagnostic Commands

```bash
# 1. Check if MemMachine is running
docker ps | grep memmachine

# 2. Check health
curl http://localhost:8080/health

# 3. Check available endpoints
curl http://localhost:8080/openapi.json | python3 -m json.tool

# 4. Test adding a memory
curl -X POST http://localhost:8080/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "session": {
      "user_id": ["test"],
      "session_id": "test_session",
      "agent_id": ["bot"],
      "group_id": null
    },
    "producer": "test",
    "produced_for": "bot",
    "episode_content": "test message",
    "episode_type": "dialog",
    "metadata": {"timestamp": "2025-01-01T00:00:00"}
  }'

# 5. Check recent MemMachine errors
docker logs memmachine-app --tail 20 | grep -i error
```

## Common MemMachine Configuration Issues

### Missing Dependencies

If MemMachine fails to start or gives 500 errors, check for missing Python packages:

```bash
# Check what's installed
docker exec memmachine-app pip list | grep -E "(sentence|transformer|torch)"

# Install missing packages
docker exec memmachine-app pip install sentence-transformers
docker exec memmachine-app pip install torch
```

### Database Connection Issues

```bash
# Check if databases are accessible
docker ps | grep -E "(neo4j|postgres)"

# Check MemMachine database configuration
docker exec memmachine-app cat /app/configuration.yml
```

### Port Conflicts

```bash
# Check what's using port 8080
lsof -i :8080

# If another service is using it, either:
# 1. Stop that service, or
# 2. Change MemMachine port in docker-compose.yml
```

## Getting Help

If you're still experiencing issues:

1. **Check MemMachine logs**: `docker logs memmachine-app`
2. **Check chatbot logs**: Enable debug logging in your code
3. **Verify configuration**: Ensure `configuration.yml` is correct
4. **Check documentation**: https://docs.memmachine.ai
5. **Ask for help**:
   - Discord: https://discord.gg/usydANvKqD
   - GitHub Issues: https://github.com/MemMachine/MemMachine/issues

## Debug Mode

Enable debug logging in the chatbot:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from memmachine_chatbot import MemMachineChatbot
chatbot = MemMachineChatbot(user_id="debug_user")
```

This will show detailed information about API calls and responses.

## Success Checklist

✅ MemMachine container is running  
✅ Health endpoint returns 200 OK  
✅ sentence-transformers is installed  
✅ Can add memories successfully  
✅ Can search memories successfully  
✅ OpenAI API key is set (for LLM features)  
✅ Chatbot connects without errors  

## Fixed Issues Log

- **2025-09-30**: Fixed health check endpoint (was `/v1/health`, now `/health`)
- **2025-09-30**: Added missing `sentence-transformers` dependency for reranker
- **2025-09-30**: Ensured all required fields (`group_id`, `metadata`) are included

---

**Still having issues?** Open a GitHub issue with:
- Error messages
- Docker logs output
- Your configuration.yml (redact sensitive info)
- Steps to reproduce

