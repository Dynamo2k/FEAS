# 🌐 URL Acquisition Setup Guide

This guide explains how to configure FEAS for URL-based evidence acquisition from social media platforms.

## Supported Platforms

FEAS supports acquiring evidence from the following platforms:

| Platform | Supported URLs | Status |
|----------|---------------|--------|
| **Twitter/X** | `twitter.com`, `x.com` | ✅ Full Support |
| **YouTube** | `youtube.com`, `youtu.be` | ✅ Full Support |
| **Facebook** | `facebook.com`, `fb.watch`, `fb.com` | ✅ Full Support |
| **Instagram** | `instagram.com` | ✅ Full Support |

## Environment Configuration

### Required Settings

Add the following to your `.env` file in the `backend/` directory:

```env
# Allowed Domains for URL Acquisition
# List of domains that FEAS will accept for URL evidence acquisition
ALLOWED_URL_DOMAINS=["twitter.com","x.com","youtube.com","youtu.be","facebook.com","fb.watch","fb.com","instagram.com"]
```

### Processing Mode Configuration

FEAS supports two processing modes for background jobs:

#### Option 1: Celery + Redis (Recommended for Production)

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Enable Celery for background processing
USE_CELERY=true
```

**Requirements:**
- Redis server running on the configured host/port
- Celery worker running: `celery -A app.workers.celery_app.celery worker --loglevel=info`
- Celery beat for scheduled tasks: `celery -A app.workers.celery_app.celery beat --loglevel=info`

#### Option 2: FastAPI BackgroundTasks (Simple Development Setup)

```env
# Disable Celery for simple development
USE_CELERY=false
```

**Benefits:**
- No Redis required
- No Celery worker required
- Jobs processed directly by FastAPI
- Simpler setup for local development

**Note:** This mode processes jobs synchronously in background threads, which may affect performance under heavy load. Use Celery mode for production.

## How URL Acquisition Works

1. **Submit URL**: User submits a URL from a supported platform
2. **Validation**: System validates the URL against the whitelist
3. **Download**: Content is downloaded using `yt-dlp`
4. **Processing**: The unified forensic pipeline processes the content:
   - SHA-256 hashing
   - Metadata extraction (EXIF, platform-specific)
   - Evidence storage
   - PDF report generation
5. **Chain of Custody**: All actions are logged for legal admissibility

## Example URLs

### Twitter/X
```
https://twitter.com/user/status/1234567890123456789
https://x.com/user/status/1234567890123456789
```

### YouTube
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

### Facebook
```
https://www.facebook.com/watch/?v=123456789
https://fb.watch/abcdefgh/
```

### Instagram
```
https://www.instagram.com/p/ABC123xyz/
https://www.instagram.com/reel/ABC123xyz/
```

## Troubleshooting

### Jobs Stuck at 0% / Pending

**Cause**: Background processing is not running properly.

**Solutions:**

1. **If using Celery mode (`USE_CELERY=true`)**:
   - Ensure Redis is running: `redis-cli ping` should return `PONG`
   - Ensure Celery worker is running: Check logs for errors
   - Restart Celery: `docker-compose restart celery-worker`

2. **Switch to BackgroundTasks mode**:
   - Set `USE_CELERY=false` in your `.env` file
   - Restart the backend server

### URL Not Accepted

**Cause**: URL domain is not in the allowed list.

**Solution**: Add the domain to `ALLOWED_URL_DOMAINS` in your `.env` file.

### Download Fails

**Cause**: `yt-dlp` cannot access the content.

**Solutions:**
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check if the content is publicly accessible
- Check internet connectivity
- Some content may require authentication (not currently supported)

## Security Considerations

1. **URL Validation**: All URLs are validated against a whitelist before processing
2. **Domain Matching**: Secure domain matching prevents bypass via subdomains
3. **Content Isolation**: Downloaded content is stored in isolated directories
4. **Chain of Custody**: All actions are logged with timestamps and investigator IDs

## API Endpoints

### Submit URL Job

```bash
POST /api/v1/jobs/url
Content-Type: application/json

{
    "url": "https://twitter.com/user/status/1234567890",
    "investigator_id": "INV-001",
    "case_number": "CASE-2024-001",
    "notes": "Evidence for investigation"
}
```

### Check Job Status

```bash
GET /api/v1/jobs/{job_id}/status
```

### Get Job Details

```bash
GET /api/v1/jobs/{job_id}/details
```

### Download Report

```bash
GET /api/v1/jobs/{job_id}/report
```

## Further Reading

- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [README.md](README.md) - Full documentation
- [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) - Authentication setup
