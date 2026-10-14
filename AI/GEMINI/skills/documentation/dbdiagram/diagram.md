---
name: dbdiagram-database-diagram
description: Guidelines, syntax standards, and specifications for creating and maintaining DBML (dbdiagram.io) database schema diagrams.
---

# dbdiagram.io (DBML) Database Diagram Skill

## 1. Overview & Purpose

Whenever a database schema change occurs (e.g., migrations, model definitions, new tables, columns, indexes, or foreign key relationships), you must produce or update the corresponding DBML (Database Markup Language) diagram.

DBML is the open standard used by **dbdiagram.io** and **dbdocs.io** to document and visualize relational schemas cleanly and expressively.

## 2. Branch Inspection & Selective Update Protocol

Always orchestrate documentation changes through the master index at [documentation.md](../documentation.md):

1. **Inspect Branch Changes First**:
   Run `git status` and `git diff HEAD` (or compare against base branch) to identify which database migrations, ORM models, tables, columns, constraints, or relational keys were added or modified.
2. **Search Existing References**:
   Query `Documentation/config/docs/database/` and markdown files for mentions of the table or column names (e.g., `grep -rn "Table users" Documentation/config/docs/`).
3. **Selective Schema Update**:
   - Update `Documentation/config/docs/database/schema.dbml` and corresponding markdown doc pages strictly for the modified tables, columns, foreign keys, or enums. Do not alter untouched tables.
4. **Auto-Create Missing Documentation Files**:
   - If a new domain or table group does not have dedicated documentation, create a new `.md` file under `Documentation/config/docs/database/<module>.md`.
   - Embed the relevant DBML code block.
   - Add the new page to `Documentation/config/mkdocs.yml` under `nav:`.

## 3. Storage & Location Conventions

- Master DBML file: Store the consolidated database schema at:
  `Documentation/config/docs/database/schema.dbml`
- Module-specific schemas: When maintaining modular contexts, store sub-schemas at:
  `Documentation/config/docs/database/<module>.dbml`
- Embedding in Markdown documentation: Embed DBML snippets directly into MkDocs pages using fenced code blocks:
  ````markdown
  ```dbml
  Table users {
      id uuid [pk]
      email varchar [unique, not null]
  }
  ```
  ````

---

## 4. DBML Syntax Standards & Rules

### 3.1 Project Header
Declare the project metadata at the top of the master `.dbml` file:
```dbml
Project sofia_core {
  database_type: 'PostgreSQL'
  Note: '''
    # Sofia Core Database Schema
    Production relational database model for Sofia application.
  '''
}
```

### 3.2 Tables & Column Attributes
- Use lowercase snake_case for table and column names.
- Explicitly declare types and constraints for every column.
- Available column settings inside square brackets `[...]`:
  - `pk`: Primary key
  - `increment`: Auto-incrementing integer
  - `not null` / `null`: Nullability constraint
  - `unique`: Unique constraint
  - `default: value`: Default value (use backticks for SQL expressions, e.g., ``default: `now()` ``)
  - `note: '...'`: Descriptive commentary for documentation generation

```dbml
Table users {
  id uuid [pk, default: `gen_random_uuid()`]
  organization_id uuid [not null]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  status user_status [not null, default: 'active']
  created_at timestamp [not null, default: `now()`]
  updated_at timestamp [not null, default: `now()` specifications]

  Note: 'Central user authentication and credentials identity table.'
}
```

### 3.3 Enums
Define all enumerated values explicitly before table definitions:
```dbml
Enum user_status {
  active [note: 'Account is verified and active']
  pending_verification [note: 'Awaiting email confirmation']
  suspended [note: 'Suspended by admin']
  deactivated [note: 'Self-deactivated by user']
}
```

### 3.4 Indexes
Document primary, unique, and performance query indexes inside an `indexes` block at the bottom of the table:
```dbml
Table orders {
  id uuid [pk]
  user_id uuid [not null]
  status varchar(50) [not null]
  created_at timestamp [not null]

  indexes {
    user_id [name: 'idx_orders_user_id']
    (user_id, status) [name: 'idx_orders_user_status']
    created_at [name: 'idx_orders_created_at']
  }
}
```

### 3.5 Relationships & Cardinality
Foreign keys can be specified inline or via standalone `Ref:` declarations. Standalone declarations are preferred for readability.

| Cardinality | Syntax | Description |
| :--- | :---: | :--- |
| **Many-to-One** | `TableA.field > TableB.field` | Many TableA rows reference one TableB row |
| **One-to-Many** | `TableA.field < TableB.field` | One TableA row referenced by many TableB rows |
| **One-to-One** | `TableA.field - TableB.field` | Strict 1-to-1 relationship |
| **Many-to-Many** | `TableA.field <> TableB.field` | Conceptual M:N relationship |

Always define referential cascade actions when applicable:
```dbml
Ref fk_users_organization: users.organization_id > organizations.id [delete: cascade, update: no action]
Ref fk_profiles_user: user_profiles.user_id - users.id [delete: cascade]
```

### 3.6 TableGroup
Organize tables by bounded context or architectural domain:
```dbml
TableGroup identity_and_access {
  users
  user_profiles
  organizations
  sessions
}

TableGroup billing {
  subscriptions
  invoices
  payment_methods
}
```

---

## 4. Complete Schema Reference Example

```dbml
Project sofia_platform {
  database_type: 'PostgreSQL'
  Note: 'Sofia Core Architecture Schema'
}

Enum subscription_tier {
  free
  pro
  enterprise
}

Enum user_role {
  owner
  admin
  member
}

Table organizations {
  id uuid [pk, default: `gen_random_uuid()`]
  name varchar(100) [not null]
  slug varchar(100) [unique, not null]
  tier subscription_tier [not null, default: 'free']
  created_at timestamp [not null, default: `now()`]
  
  Note: 'Tenant organization entity.'
}

Table users {
  id uuid [pk, default: `gen_random_uuid()`]
  organization_id uuid [not null]
  email varchar(255) [unique, not null]
  full_name varchar(150) [not null]
  role user_role [not null, default: 'member']
  is_active boolean [not null, default: true]
  created_at timestamp [not null, default: `now()`]
  updated_at timestamp [not null, default: `now()`]

  indexes {
    organization_id [name: 'idx_users_org_id']
    email [unique, name: 'idx_users_email']
  }
}

Table user_profiles {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [unique, not null]
  avatar_url text
  bio text
  preferences jsonb [not null, default: '{}']
}

Table audit_logs {
  id bigserial [pk]
  organization_id uuid [not null]
  actor_user_id uuid
  action varchar(100) [not null]
  resource_type varchar(50) [not null]
  resource_id varchar(100) [not null]
  metadata jsonb
  created_at timestamp [not null, default: `now()`]

  indexes {
    (organization_id, created_at) [name: 'idx_audit_org_created']
  }
}

// Foreign Key References
Ref: users.organization_id > organizations.id [delete: cascade]
Ref: user_profiles.user_id - users.id [delete: cascade]
Ref: audit_logs.organization_id > organizations.id [delete: cascade]
Ref: audit_logs.actor_user_id > users.id [delete: set null]

// Domain Groups
TableGroup core_auth {
  organizations
  users
  user_profiles
}

TableGroup compliance {
  audit_logs
}
```

---

## 5. Best Practices & Rules

1. **Keep Schema in Sync**: Any database migration (e.g. Alembic, Prisma, Flyway, Knex, or raw SQL migrations) must be accompanied by an update to `Documentation/config/docs/database/schema.dbml`.
2. **Deterministic Naming**: Indexes and foreign keys must have explicit, predictable names (`idx_<table>_<column>`, `fk_<table>_<target>`).
3. **Descriptive Comments**: Add `note:` on non-obvious business columns (e.g. status flags, JSON payload shapes, soft-delete fields).
4. **No Sensitive Data**: Never put credentials, seeds with real passwords, or private encryption keys in diagram files.

## 6. Verification Checklist

- [ ] Valid DBML syntax accepted by [dbdiagram.io](https://dbdiagram.io).
- [ ] Primary keys (`pk`) specified on every table.
- [ ] Foreign keys and relationships (`Ref: ...`) have cardinality and cascade rules.
- [ ] Custom enums defined for all discrete status/role columns.
- [ ] TableGroups organized by domain context.
