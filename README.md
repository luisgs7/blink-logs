<p align="center">
  <img src="https://raw.githubusercontent.com/luisgs7/blink-logs/main/blink-logs.jpg" alt="BlinkLogs Logo" width="280">
</p>

# BlinkLogs ⚡

A high-performance, developer-centric log management and observability platform designed to aggregate, compress, and visualize logs in real-time. 

> ⚠️ **Project Status: Under Active Development**
> This project is currently in its initial development phase. Features and architecture are being rolled out incrementally.

---

## The Problem

Modern distributed applications generate millions of log lines daily. Managing these logs introduces three major engineering challenges:
1. **Application Bottlenecks:** Sending logs directly from the application code via synchronous HTTP requests introduces latency and degrades core app performance.
2. **Storage and Infrastructure Costs:** Traditional relational databases (like PostgreSQL) or document stores (like MongoDB) scale poorly for massive text indexing, leading to skyrocketing storage costs.
3. **Data Privacy Risks:** Logs often accidentally leak sensitive information (passwords, tokens, PII). Transporting and storing this data raw violates compliance standards like GDPR and LGPD.

---

## The Solution: How BlinkLogs Resolves It

**BlinkLogs** addresses these challenges by decoupling data ingestion from the application lifecycle and leveraging a column-oriented analytical database designed for scale.

### 1. Zero-Footprint Log Shipping (The Sidecar Pattern)
Instead of forcing applications to make network requests, applications simply write logs to a local file. A lightweight **BlinkLogs Docker Agent** runs alongside the app, tails the log file, accumulates lines, and ships them asynchronously.

### 2. High-Throughput & Optimized Network Layer
* **Batching & Compression:** The Docker agent groups logs and compresses them using **Gzip** before shipping, reducing bandwidth usage by up to 85%.
* **Stateless Fast Ingestion:** A **FastAPI** backend receives the compressed batches, validates the API key via a **Redis** cache layer, and pushes the payload straight into a Redis queue in milliseconds.

### 3. Columnar Storage for Sub-Millisecond Queries
Logs are pulled from the Redis queue by background workers and batch-inserted into **ClickHouse**. Because ClickHouse stores data in columns and compresses text aggressively, it allows lightning-fast full-text searches across billions of rows while using a fraction of the disk space required by traditional databases.

### 4. Real-Time Observability Dashboard
Built with **Vue.js & Quasar Framework**, the administrative panel connects to FastAPI via **WebSockets** to provide a "Live Tail" feature, letting developers see errors and info logs arriving in real-time.

---

## Technical Architecture & Polyglot Persistence

BlinkLogs uses the right tool for the right job (**Polyglot Persistence**):

* **FastAPI:** High-performance, asynchronous Python framework handling data ingestion and query APIs.
* **ClickHouse:** The analytical core, optimized for massive log storage and ultra-fast log aggregation.
* **PostgreSQL:** Handles transactional data (user authentication, teams, API Key management).
* **Redis:** Acts both as a high-speed volatile cache for API Keys and an in-memory message queue for incoming log streams.
* **Vue.js + Quasar:** SPA frontend providing smooth virtual pagination for rendering thousands of log streams seamlessly.

---

## Planned Architecture Flow

```text
[ App Container ] ──(Writes to file)──► [ Shared Volume ]
                                               │
                                               ▼
                                    [ BlinkLogs Docker Agent ]
                                               │
                                               │ (HTTP POST + Gzip Batch)
                                               ▼
[ Quasar Admin ] ◄──(WebSockets)──► [ FastAPI Ingest/Admin ] ──(Auth Cache)──► [ Redis Cache ]
                                               │
                                               │ (Enqueue)
                                               ▼
                                        [ Redis Queue ]
                                               │
                                               ▼
                                     [ Background Worker ]
                                               │
                                               │ (Bulk Insert)
                                               ▼
         [ PostgreSQL ]                  [ ClickHouse ]
     (Users, Teams, Keys)               (Raw Log Data)

```

## Upcoming Roadmap

* [ ] **Milestone 1:** Basic FastAPI ingestion endpoint paired with ClickHouse standalone storage.
* [ ] **Milestone 2:** Redis-backed queue implementation and asynchronous background workers.
* [ ] **Milestone 3:** Vue.js + Quasar administrative dashboard with historical query search.
* [ ] **Milestone 4:** Docker log-shipper agent for edge log streaming.
* [ ] **Milestone 5:** WebSocket integration for Live Tail functionality.
