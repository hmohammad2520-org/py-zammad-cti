# Zammad CTI Client (Python)

A lightweight, typed Python client for interacting with **Zammad’s Generic CTI API**.
This module allows telephony systems (PBX, SIP servers, dialers, etc.) to notify Zammad about call lifecycle events such as **new calls**, **answers**, and **hangups**.

📖 Official Zammad CTI documentation:
[https://docs.zammad.org/en/latest/api/generic-cti/index.html](https://docs.zammad.org/en/latest/api/generic-cti/index.html)

---

## Features

* Simple and clean API for Zammad CTI events
* Fully typed (using `typing` and custom type aliases)
* Automatic environment-based configuration via `ENVMod`
* Structured logging via `logwrap`
* Minimal dependencies
* Explicit control over SSL verification
* Designed for backend / PBX integrations

---

## Installation

```bash
pip install py-zammad-cti
```

This module also depends on:

* `classmods`
* `requests`
* `python-dotenv` (Optional)

Make sure those are available in your environment.

---

## Basic Usage

```python
from zammad_cti import CTIClient

client = CTIClient(
    url="https://zammad.example.com/api/v1/cti/<TOKEN>",
    verify_ssl=False,
)
```

Once initialized, you can send CTI events to Zammad.

---

## Environment Configuration (ENVMod)

The `CTIClient` constructor is registered with `ENVMod`:

```python
@ENVMod.register(section_name='ZammadCTI')
```

This allows configuration via environment variables or `.env` files (depending on your `ENVMod` setup), for example:

```env
ZammadCTI_URL=https://zammad.example.com/api/v1/cti/<TOKEN>
ZammadCTI_VERIFY_SSL=false
```

This makes the client easy to configure in containerized or production environments.

Later you can load env with python-dotenv and classmod easily:

```python
from zammad_cti import CTIClient
from classmods import ENVMod

client = CTIClient(**ENVmod.load_args(CTIClient.__init__))
```

Read classmods documentations for more info and usage:

📖 Official Zammad CTI documentation:
[https://github.com/hmohammad2520-org/classmods](https://github.com/hmohammad2520-org/classmods)

---

## Call Lifecycle Methods

### 1. New Call

Notify Zammad that a new call has started.

```python
client.new_call(
    _from="+491234567",
    to="+498765432",
    direction=CallDirection.IN,
    call_id="call-uuid-123",
    user="John Doe",
    queue="Support",
)
```

**Parameters**

| Name        | Type            | Description                   |                 |
| ----------- | --------------- | ----------------------------- | --------------- |
| `_from`     | `str`           | Caller number                 |                 |
| `to`        | `str`           | Destination number            |                 |
| `direction` | `CallDirection` | Call direction (`in` / `out`) |                 |
| `call_id`   | `str`           | Unique call identifier        |                 |
| `user`      | `Optional[str   | List[str]]`                   | Related user(s) |
| `queue`     | `Optional[str]` | Queue name                    |                 |

---

### 2. Answer Call

Notify Zammad that a call has been answered.

```python
client.answer(
    _from="+491234567",
    to="+498765432",
    direction=CallDirection.IN,
    call_id="call-uuid-123",
    answering_number="+498765432",
    user="Agent Smith",
)
```

**Parameters**

| Name               | Type            | Description                                |                  |
| ------------------ | --------------- | ------------------------------------------ | ---------------- |
| `_from`            | `str`           | Caller number                              |                  |
| `to`               | `str`           | Destination number                         |                  |
| `direction`        | `CallDirection` | Call direction                             |                  |
| `call_id`          | `str`           | Unique call ID                             |                  |
| `answering_number` | `Optional[str]` | Number used to identify the answering user |                  |
| `user`             | `Optional[str   | List[str]]`                                | User(s) involved |

---

### 3. Hangup Call

Notify Zammad that a call has ended.

```python
client.hangup(
    _from="+491234567",
    to="+498765432",
    direction=CallDirection.IN,
    call_id="call-uuid-123",
    cause=HangupCause.NORMAL_CLEARING,
    answering_number="+498765432",
)
```

**Parameters**

| Name               | Type            | Description        |
| ------------------ | --------------- | ------------------ |
| `_from`            | `str`           | Caller number      |
| `to`               | `str`           | Destination number |
| `direction`        | `CallDirection` | Call direction     |
| `call_id`          | `str`           | Unique call ID     |
| `cause`            | `HangupCause`   | Reason for hangup  |
| `answering_number` | `Optional[str]` | User lookup hint   |

Zammad uses the hangup cause to determine missed calls, answered calls, etc.

---

## Logging

This module uses `logwrap` decorators to automatically log:

* Outgoing HTTP requests
* Call lifecycle transitions
* Returned results

Example logged message:

```
Changed call state to hangup: {...}, result: {...}
```

Logging behavior can be controlled centrally via `logwrap`.

---

## HTTP Behavior

* Uses a persistent `requests.Session`
* Sends data as `application/json`
* Automatically removes `None` values from payloads
* Raises exceptions on HTTP errors (`response.raise_for_status()`)

Most CTI responses are empty unless the call is rejected or blocked in Zammad. Read Zammad CTI system documentation for more info.

---

## Type Safety

The client relies on explicit type aliases:

* `CallDirection`
* `HangupCause`

This helps prevent invalid CTI payloads and improves IDE autocomplete and static analysis.

---

## Typical Use Case

This client is ideal for:

* PBX → Zammad integrations
* SIP servers (Asterisk, FreeSWITCH, Kamailio)
* Custom softphones
* Call monitoring services
* Telephony middleware

---

## Error Handling

* All HTTP errors raise `requests.HTTPError`
* Validation is delegated to Zammad
* Invalid payloads will be rejected server-side

You should wrap calls in your own retry / error-handling logic if required.

---

## License

MIT (or your preferred license)