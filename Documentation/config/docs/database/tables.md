# Sofia Accounts Database Schema & Tables

## 1. Overview
The **Sofia Accounts Database** (`accounts`) stores identity, membership profiles, device tracking, and legal terms agreements for the authentication microservice. The database uses PostgreSQL and is partitioned into two core schemas:
- **`signup`**: Manages registration terms, country references, and user agreements.
- **`member`**: Stores user identity, personal details, and client device tracking.

---

## 2. Relational Schema Diagram (DBML)

The following DBML diagram represents the complete relational structure, keys, indexes, and constraints for the `accounts` database:

```dbml
Project accounts_service {
  database_type: 'PostgreSQL'
  Note: '''
    # Sofia Accounts & Auth Database Schema
    Production relational database model for accounts, member profiles, devices, and signup terms.
  '''
}

// ----------------------------------------------------
// Schema: signup
// ----------------------------------------------------

Table signup.terms {
  id serial [pk, increment]
  name varchar(150) [not null, note: 'Name or title of the terms document']
  tag varchar(50) [not null, note: 'Identifier tag for terms categorization']
  content text [not null, note: 'Full text/markdown content of terms']
  version int [not null, default: 1, note: 'Terms version number']
  active boolean [not null, default: false, note: 'Whether this terms version is active']
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  indexes {
    (tag, version) [unique, name: 'un_idx_signup_terms']
  }

  Note: 'Platform legal terms and conditions versions.'
}

Table signup.country {
  id serial [pk, increment]
  tag varchar(10) [not null, note: 'ISO country code or identifier']
  name varchar(150) [note: 'Country name']
  active boolean [not null, default: true]
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  indexes {
    tag [unique, name: 'un_idx_signup_country']
  }

  Note: 'Supported countries directory for onboarding.'
}

Table signup.user_agreements {
  id serial [pk, increment]
  user_id uuid [not null, note: 'Foreign key to member.user']
  term_id int [not null, note: 'Foreign key to signup.terms']
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  indexes {
    (user_id, term_id) [unique, name: 'un_idx_signup_user_agreements']
  }

  Note: 'Audit log of user acceptance for specific terms versions.'
}

// ----------------------------------------------------
// Schema: member
// ----------------------------------------------------

Table member.user {
  id uuid [pk, note: 'Unique user identifier']
  full_name varchar(150) [note: 'Legal full name of user']
  nick_name varchar(150) [note: 'Public display nickname']
  email varchar(150) [note: 'User email address']
  phone varchar(50) [note: 'Contact phone number']
  active boolean [not null, default: true, note: 'Active account status flag']
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  indexes {
    email [unique, name: 'un_idx_members_email']
    phone [unique, name: 'un_idx_members_phone']
  }

  Note: 'Core member identity table in accounts database.'
}

Table member.user_details {
  id uuid [pk, note: 'Primary key for user detail record']
  user_id uuid [not null, note: 'Foreign key to member.user']
  born_date date [not null, note: 'Date of birth']
  country_id int [note: 'Foreign key to signup.country']
  validated_email boolean [not null, default: false]
  validated_phone boolean [not null, default: false]
  address varchar(50) [note: 'User street address']
  document varchar(50) [not null, note: 'Official document / tax ID']
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  indexes {
    user_id [unique, name: 'un_idx_members_detail_user_id']
    document [unique, name: 'un_idx_members_detail_user_document']
  }

  Note: 'Extended user personal details and verification state.'
}

Table member.device {
  id uuid [pk, note: 'Primary key for device record']
  user_id uuid [not null, note: 'Foreign key to member.user']
  x_device_id varchar(50) [not null, note: 'Unique device hardware/fingerprint identifier']
  ip_list "varchar[]" [note: 'Array of known IP addresses']
  active boolean [not null, default: true]
  created_at timestamp [not null, default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [not null, default: `CURRENT_TIMESTAMP`]

  Note: 'Registered client devices and associated IP histories.'
}

// Foreign Key References
Ref fk_user_agreements_term: signup.user_agreements.term_id > signup.terms.id
Ref fk_user_agreements_user: signup.user_agreements.user_id > member.user.id
Ref fk_member_user_details: member.user_details.user_id - member.user.id
Ref fk_member_user_details_contry: member.user_details.country_id > signup.country.id
Ref fk_member_user_device: member.device.user_id > member.user.id

// Domain Groups
TableGroup signup_domain {
  signup.terms
  signup.country
  signup.user_agreements
}

TableGroup member_domain {
  member.user
  member.user_details
  member.device
}
```

---

## 3. Data Dictionary & Specifications

### 3.1 Schema `signup`
- **`signup.terms`**: Legal agreements and terms of use. Indexed uniquely by `(tag, version)`.
- **`signup.country`**: List of eligible nations with unique country code `tag`.
- **`signup.user_agreements`**: Junction table auditing when each user agreed to specific terms versions. Indexed uniquely by `(user_id, term_id)`.

### 3.2 Schema `member`
- **`member.user`**: Core account entity mapped by the SQLAlchemy `User` ORM model. Enforces unique indexes on `email` (`varchar(150)`) and `phone` (`varchar(50)`).
- **`member.user_details`**: 1-to-1 extension containing demographic and verification attributes (unique on `user_id` and `document`).
- **`member.device`**: Device audit and multi-factor tracking records linked to users via `user_id`.

### 3.3 Database Roles & Privileges
- **Migration Role (`role_migration` / `app_migration_accounts`)**: Dedicated migration role with schema creation and DDL administration rights.
- **Application User (`platform_auth`)**: Dedicated least-privilege runtime user with `SELECT`, `INSERT`, `UPDATE` grants on domain tables and sequence usage privileges.

---

## 4. Related Migration Files
- [`1e54206ef92a_create_schema_signup.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/1e54206ef92a_create_schema_signup.py)
- [`22e629197d2b_create_schema_member.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/22e629197d2b_create_schema_member.py)
- [`dab5b850a8db_create_tables_for_schema_member.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/dab5b850a8db_create_tables_for_schema_member.py)
- [`7172f95175c9_create_tables_for_schema_signup.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/7172f95175c9_create_tables_for_schema_signup.py)
- [`bb147f4b4e5c_create_index_and_references_in_members.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/bb147f4b4e5c_create_index_and_references_in_members.py)
- [`7312727d435c_create_index_and_references_in_signup.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/7312727d435c_create_index_and_references_in_signup.py)
- [`a1ec85b0f442_set_grant_for_auth_user_in_accounts.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/alembic/versions/a1ec85b0f442_set_grant_for_auth_user_in_accounts.py)
- [`docker-compose.yml`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Infra/auth/docker-compose.yml)
- [`schema.dbml`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Documentation/config/docs/database/schema.dbml)
