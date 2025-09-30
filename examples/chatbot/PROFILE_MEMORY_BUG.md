# ⚠️ Profile Memory Bug - Known Issue

## Problem

When using `/v1/memories` endpoint (demo3.py), MemMachine returns **500 errors** with this exception:

```python
AttributeError: 'tuple' object has no attribute 'removeprefix'
```

**Location**: `/memmachine/profile_memory/profile_memory.py` line 418

## Symptoms

```
Response: 500
⏱️  Time: 16.156s  ← Very slow!
```

- HTTP 500 errors on POST `/v1/memories`
- Very slow response times (15-20 seconds)
- MemMachine logs show AttributeError
- Profile memory fails to extract facts

## Root Cause

This is a **bug in MemMachine's profile memory implementation**. The code incorrectly tries to call `.removeprefix()` on a tuple object instead of a string.

## ✅ Solution: Use Demo 2 (Episodic Only)

**Recommended**: Use `demo2.py` which bypasses profile memory entirely:

```bash
cd examples/chatbot
python3 demo2.py
```

### Demo 2 Uses:
- ✅ `/v1/memories/episodic` (store)
- ✅ `/v1/memories/episodic/search` (search)
- ✅ No profile memory = No bug!
- ✅ Fast and stable

## Comparison

| Demo | Endpoint | Profile Memory | Status |
|------|----------|----------------|--------|
| **demo2.py** | `/v1/memories/episodic` | ❌ Not used | ✅ **Works** |
| **demo3.py** | `/v1/memories` | ✅ Used | ❌ **Bug** |

## When Will This Be Fixed?

This is a **MemMachine bug** that needs to be fixed by the MemMachine team. Possible fixes:

1. **MemMachine team fixes the bug** in `profile_memory.py`
2. **Upgrade to a newer version** of MemMachine that has this fixed
3. **Disable profile memory** in `configuration.yml`

## Workaround Options

### Option 1: Use Demo 2 (Recommended)

```bash
python3 demo2.py
```

**Pros**: 
- ✅ Stable and fast
- ✅ Full conversation memory
- ✅ Works with all LLM features

**Cons**:
- ❌ No automatic fact extraction
- ❌ No long-term profile storage

### Option 2: Disable Profile Memory in Config

Edit `configuration.yml`:

```yaml
# Add this to disable profile memory
ProfileMemory:
  enabled: false
```

Then restart MemMachine:

```bash
docker-compose restart memmachine-app
```

### Option 3: Wait for MemMachine Fix

Monitor the MemMachine GitHub repo for updates:
- https://github.com/MemMachine/MemMachine/issues

## Testing If It's Fixed

To test if profile memory is working:

```bash
# Try demo3
cd examples/chatbot
python3 demo3.py

# If you see Response: 200 (not 500), it's fixed!
```

## Expected Behavior (When Fixed)

When profile memory works correctly, you should see:

```
👤 Sarah: Hi! My name is Sarah and I'm a data engineer

   📥 [MemMachine] Storing in episodic + profile memory...
      REST API: POST http://localhost:8080/v1/memories
      Response: 200  ← Should be 200, not 500!
      ⏱️  Time: 0.342s  ← Should be fast!

Later...

   🔍 [MemMachine] Searching episodic + profile memory...
      Found: 3 episodic, 2 profile memories  ← Profile facts extracted!
```

## Additional Context

From our troubleshooting session, we discovered:

1. **Episodic-only endpoints work perfectly** (`/v1/memories/episodic`)
2. **Combined endpoints have a bug** (`/v1/memories`)
3. **The bug is in MemMachine server code**, not our chatbot client
4. **This is a known issue** documented in FIXES_APPLIED.md

## Summary

```
┌─────────────────────────────────────────────────┐
│  Use demo2.py until profile memory is fixed!    │
│                                                  │
│  demo2.py = Stable, fast, episodic memory       │
│  demo3.py = Broken due to MemMachine bug        │
└─────────────────────────────────────────────────┘
```

## Related Files

- `demo2.py` - ✅ Working demo (episodic only)
- `demo3.py` - ❌ Broken demo (profile memory bug)
- `FIXES_APPLIED.md` - Full troubleshooting history
- `TROUBLESHOOTING.md` - General debugging guide
- `DEMO3_README.md` - Profile memory explanation

---

**Last Updated**: September 30, 2025  
**Status**: Bug confirmed in MemMachine v0.x  
**Workaround**: Use demo2.py with episodic-only endpoints

