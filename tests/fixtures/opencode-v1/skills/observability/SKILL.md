---
name: observability
description: Design and inspect logging, metrics, tracing, and alerting. Use when adding observability to a system or debugging an incident.
metadata:
  audience: architect, builder, security
---
# Observability

## When to use
- Adding logging/metrics/tracing to a system.
- Investigating incidents (logs, dashboards, alerts).
- Reviewing whether a system can be diagnosed.

## Rules
- Structured logging (JSON) with correlation IDs across services; timestamps UTC.
- Log levels meaningful: DEBUG for detail, INFO for lifecycle, WARN for anomalies, ERROR for failures.
- Never log secrets, tokens, PII, or full request bodies. Redact.
- Metrics: latency (histograms with percentiles), error rate, request rate, saturation (queues, connections, CPU), business-critical counters.
- Tracing for cross-service requests; propagate trace/span IDs.
- Alert on symptoms (error rate, latency SLO) not just causes; alert fatigue kills signal.
- Dashboards answer questions: is it up, is it slow, is it erroring, is it losing data?
- Health endpoints: liveness vs readiness (readiness depends on dependencies).
- Debuggability: each failure should be traceable to an error log with request context.

## Log line sketch
```
{"ts":"2026-09-08T10:28:18Z","level":"error","correlation_id":"a1b2","svc":"billing",
 "event":"charge.failed","charge_id":"c_123","amount_cents":1200,"error":"card_declined","err_detail":"..."}
```

## Checklist
- [ ] Structured logs with correlation IDs
- [ ] No secrets/PII in logs
- [ ] Metrics: latency/error/rate/saturation
- [ ] Tracing across services
- [ ] Alerts on symptoms with SLOs
- [ ] Health endpoints (liveness/readiness)
- [ ] Every failure traceable to a log line