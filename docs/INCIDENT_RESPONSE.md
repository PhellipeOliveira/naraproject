# Incident Response Runbook

## Objective
Define a clear process for triage, containment, communication, and recovery during production incidents.

## Severity Levels
- **SEV-1 (Critical):** Public outage, data breach, or major data corruption.
- **SEV-2 (High):** Major feature degraded for many users, no known workaround.
- **SEV-3 (Medium):** Partial degradation with workaround available.
- **SEV-4 (Low):** Minor issue, no immediate user impact.

## On-Call Flow
1. Detect incident via monitoring/alerts or user report.
2. Open incident channel and assign Incident Commander.
3. Classify severity and start timeline.
4. Contain impact (disable failing endpoint/feature flag/rollback).
5. Recover service and validate health endpoints.
6. Publish post-incident report with root cause and actions.

## First 15 Minutes Checklist
- Confirm scope (`/health`, `/health/detailed`, API smoke tests).
- Identify blast radius (frontend, backend, database, external APIs).
- Freeze non-essential deploys.
- Capture logs and request IDs for affected requests.
- Communicate first status update to stakeholders.

## Containment Playbook
- **Backend errors spike:** rollback latest deployment, keep health checks running.
- **Database issue:** switch to read-only mode if possible, validate migrations.
- **External provider outage (OpenAI/Supabase/Resend):** enable graceful degradation and user-friendly messaging.
- **Abuse traffic:** tighten rate limits and block offending IP ranges at edge.

## Communication Cadence
- SEV-1: updates every 15 minutes.
- SEV-2: updates every 30 minutes.
- SEV-3/4: updates every 60 minutes.

Each update must include:
- Current status
- Impacted user scope
- Mitigation in progress
- Next update ETA

## Recovery Validation
- `/health` and `/health/ready` returning success.
- Core flow validated: start diagnostic -> answer -> finish -> result.
- Error rate and latency returned to baseline.
- No active data integrity issues in Supabase tables.

## Post-Incident (within 48h)
- Build timeline (UTC), trigger, contributing factors.
- Document customer impact and duration.
- Define corrective actions with owners and due dates.
- Track actions in release checklist before next public rollout.
