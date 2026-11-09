# TV Show Database Design

Converted from the hand-drawn sketch.

- The same person can be both an actor and a writer on a show, so there's one `PERSON` table instead of separate `ACTOR` and `WRITER` tables.
- `ACTOR_SHOW` and `WRITER_SHOW` are junction tables that both point to `PERSON` and `TV_SHOW` — a person can have a row in either, or both, for the same show.
- `EPISODE` belongs to exactly one `TV_SHOW` (one show has many episodes).

```mermaid
erDiagram
    TV_SHOW ||--o{ EPISODE : has
    TV_SHOW ||--o{ ACTOR_SHOW : includes
    PERSON ||--o{ ACTOR_SHOW : acts_in
    TV_SHOW ||--o{ WRITER_SHOW : includes
    PERSON ||--o{ WRITER_SHOW : writes

    TV_SHOW {
        int ShowID PK
    }

    EPISODE {
        int EpisodeID PK
        int ShowID FK
    }

    PERSON {
        int PersonID PK
        string Name
        string Nationality
        int BirthYear
    }

    ACTOR_SHOW {
        int PersonID FK
        int ShowID FK
    }

    WRITER_SHOW {
        int PersonID FK
        int ShowID FK
    }
```