# env file

## App settings

ENVIRONMENT=development
DEBUG="False" # Use for development, False for production (default), during debbug the handler will no be used, and the default FastAPI exception handler will be used instead.
TELEMETRY_TRACING=True
APP_NAME=Sofia-Auth
APP_DESCRIPTION=Authentication service for Sofia
APP_VERSION=0.1.0
CONTACT_NAME=Support Team
CONTACT_URL=<http://www.example.com/support>
CONTACT_EMAIL=<support@example.com>
LICENSE_NAME=Apache 2.0
LICENSE_URL=<http://www.apache.org/licenses/LICENSE-2.0.html>
CORS_ALLOW_ORIGINS=<http://localhost,http://localhost:8080>,*

## Database & Migration

PGSQL_DATABASE_AUTH_MIGRATION_CONNECTION_STRING="postgresql://app_migration_accounts:senhasegUr@127.0.0.1:5432/accounts"
PGSQL_DATABASE_PLATFORM_AUTH_ACCOUNTS_CONNECTION_STRING="postgresql://platform_auth:senhasegUr@127.0.0.1:5432/accounts"
