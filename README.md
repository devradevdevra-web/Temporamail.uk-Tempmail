# TemporaMail Client

A lightweight and efficient Python client that interacts with `temporamail.uk` to programmatically generate random temporary email addresses, poll for incoming messages, and fetch complete email details.

Built using `requests`, this client uses a clean object-oriented design to handle random string generation, REST API endpoint communication, polling timeouts, and detailed message retrieval.

---

## Features

- **Random Email Generation:** Automatically generates unique temporary email addresses using configurable username lengths and domain names.
- **REST API Integration:** Directly queries backend endpoints (`/emails/{address}` and `/inbox/{id}`) for clean, programmatic access without scraping.
- **Configurable Polling Loop:** Periodically checks the inbox at custom intervals with a defined timeout threshold.
- **Detailed Message Fetching:** Automatically iterates through received message summaries and retrieves full email payloads.
- **Structured Logging:** Time-stamped, level-based console logging via Python's built-in `logging` module.

---

## Prerequisites

Make sure you have Python 3.8+ installed along with the required third-party libraries:

```bash
pip install requests
