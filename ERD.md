# UVote ERD

This document describes the core entities and relationships for the UVote microservices. The schema reflects the current implementation across user-service, poll-service, and vote-service.

## Diagram (Mermaid)
```mermaid
erDiagram
    USERS ||--o{ POLLS : creates
    POLLS ||--o{ POLL_OPTIONS : has
    POLLS ||--o{ VOTES : receives
    POLL_OPTIONS ||--o{ VOTES : chosen_by

    USERS {
        uuid id PK
        string username UK
        string password_hash
        datetime created_at
    }

    POLLS {
        uuid id PK
        string question
        string url UK  // unique public URL slug
        uuid creator_id FK  // references USERS.id
        datetime created_at
    }

    POLL_OPTIONS {
        uuid id PK
        uuid poll_id FK  // references POLLS.id
        string text
        int order_index
    }

    VOTES {
        uuid id PK
        uuid poll_id FK  // references POLLS.id
        uuid option_id FK  // references POLL_OPTIONS.id
        string ip_address
        datetime created_at
        // Constraint: unique (poll_id, ip_address)
    }
```

## Entities
- **Users**: Accounts that authenticate and create polls.
  - Key fields: `id`, `username` (unique), `password_hash`.
- **Polls**: Poll definitions with a unique public `url` and a `question`.
  - Key fields: `id`, `question`, `url` (unique), `creator_id` (FK to Users).
- **Poll Options**: Individual options belonging to a poll.
  - Key fields: `id`, `poll_id` (FK), `text`, `order_index`.
- **Votes**: A single vote selecting one option of a poll.
  - Key fields: `id`, `poll_id` (FK), `option_id` (FK), `ip_address`.
  - Constraint: One vote per IP per poll → unique `(poll_id, ip_address)`.

## Relationships
- A `User` creates many `Polls`.
- A `Poll` has many `Poll Options`.
- A `Poll` receives many `Votes`.
- A `Poll Option` is chosen by many `Votes`.

## Notes
- Authentication uses JWT (issued by user-service). Tokens are not stored.
- Each microservice maintains its own database; FK relationships are logical across services.
- The `url` in `Polls` is a unique, human-friendly identifier for sharing polls.
