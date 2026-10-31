# Ajude-se

## Bancos

É necessário gerar as credenciais da role do migration e dos integrantes por database nas instancias manualmente.
Para os serviços é necessário criar a role, tambem é recomendado trocar a senha do usuário pois a presente são somente exemplos.

Para padronização, o migration sempre deve possuir uma role e ter um usuário atrelado a role.

```sql
create role role_migration with NOSUPERUSER NOCREATEDB CREATEROLE INHERIT NOLOGIN NOREPLICATION NOBYPASSRLS;
```

Defina as permissões na database como abaixo
Altere o XXXX pelo nome da database, assim como nos exemplos: `app_migration_accounts`, `accounts`

```sql
create user app_migration_XXXX with login password'senhasegUr' IN ROLE role_migration;
grant app_migration_XXXX to role_migration;
```

```sql
GRANT ALL ON SCHEMA public TO app_migration_XXXX;
GRANT CONNECT ON DATABASE XXXX TO app_migration_XXXX;
GRANT CREATE ON DATABASE XXXX TO app_migration_XXXX;
```

### Auth service

gere a database assim que docker estiver online.

```sql
create database accounts;
create user app_migration_accounts with login password'senhasegUr' IN ROLE role_migration;
CREATE USER platform_auth with password'senhasegUr' login;
grant role_migration to app_migration_accounts;

GRANT ALL ON SCHEMA public TO app_migration_accounts;
GRANT CONNECT ON DATABASE accounts TO app_migration_accounts;
GRANT CREATE ON DATABASE accounts TO app_migration_accounts;
```
