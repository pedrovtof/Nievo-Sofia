
# Template

YYYY-MM-DD - [TYPE] - [GENERAL-DESCRIPTION]

## Details

- [DETAILS] - [IMPACT] - [AUTHOR] - [DATE (YYYY-MM-DD)] - [BOARD-CARD] - [COMMIT-HASH]

## Types

- [NEW] - New feature
- [FIX] - Bug fix
- [CHG] - Change
- [DOC] - Documentation
- [TEST] - Test
- [REFACTOR] - Refactor
- [PERF] - Performance
- [SEC] - Security
- [BREAK] - Breaking change
- [ROLL] - Rollback
- [BUILD] - Build/CI/CD
- [OTHER] - Other

### Changelog

2026-10-30 - [NEW] - Adição de persistência de detalhes do usuário, validação de faixa etária e transação atômica no cadastro

Detalhes:

- Criação da entidade UserDetails e repositório UserDetailsRepository para persistência em member.user_details - Pedro Victor - 2026-10-30 - #9 - pendente
- Implementação de validação de data de nascimento e faixa etária mínima/máxima configurável no fluxo de cadastro - Pedro Victor - 2026-10-30 - #9 - pendente
- Adoção de transação atômica com rollback explícito e método create_without_commit nos repositórios durante o signup - Pedro Victor - 2026-10-30 - #9 - pendente
- Atualização das migrações Alembic para chave primária UUID em user_agreements e ajustes de tamanho de colunas em user_details - Pedro Victor - 2026-10-30 - #9 - pendente
- Atualização completa dos diagramas Mermaid e DBML e portabilidade de links relativos na documentação MkDocs e READMEs - Pedro Victor - 2026-10-30 - #9 - pendente

---

2026-10-29 - [NEW] - Implementação completa do registro de usuário com criptografia bcrypt, aceite de termos e cadastro de dispositivo

Detalhes:

- Implementação do serviço Encryption com validação regex de senha e hash bcrypt, além dos enums EStatusBaseApi e EResponseAuth - Pedro Victor - 2026-10-29 - #9 - a0325fc
- Criação da interface IRepositories, entidades ORM (Device, Terms, UserAgreements), campo password em User e respectivos repositórios - Pedro Victor - 2026-10-29 - #9 - a0325fc
- Implementação das validações de headers, termos ativos, unicidade de e-mail e persistência completa em POST /api/v1/signup/user (HTTP 201) - Pedro Victor - 2026-10-29 - #9 - a0325fc
- Ajustes nas migrações Alembic (member.user, member.device e grants de sequences), README do Auth e sincronização dos diagramas DBML e Mermaid - Pedro Victor - 2026-10-29 - #9 - a0325fc

---

2026-10-28 - [FIX] - Ajustes na entidade User, indentação do repositório e sincronização de diagramas

Detalhes:

- Ajuste do tamanho da coluna email para String(150) na entidade ORM User - Pedro Victor - 2026-10-28 - #9 - 01afc6c
- Correção de indentação no método get_by_mail do UserRepository - Pedro Victor - 2026-10-28 - #9 - 83f497e
- Remoção de variável temporária de teste em SignupService.signup_user e sincronização da documentação - Pedro Victor - 2026-10-28 - #9 - c4576be

---

2026-10-28 - [NEW] - Implementação do SessionManager SQLAlchemy, entidade User, repositório e ajustes de migração

Detalhes:

- Implementação do SessionManager com gerenciamento de ciclo de vida lifespan no FastAPI e pool de conexões - Pedro Victor - 2026-10-28 - #9 - fef7a7e
- Criação da base declarativa ORM, entidade User (member.user) e UserRepository com injeção de dependência - Pedro Victor - 2026-10-28 - #9 - fef7a7e
- Atualização do endpoint de registro para POST /api/v1/signup/user com SignupUserRequest e integração ao UserRepository - Pedro Victor - 2026-10-28 - #9 - fef7a7e
- Correção da tabela signup.country, ampliação de member.user.email nas migrações Alembic e sincronização da documentação e diagramas - Pedro Victor - 2026-10-28 - #9 - fef7a7e

---

2026-10-27 - [NEW] - Estruturação do banco Postgres, migrações de contas e documentação DBML

Detalhes:

- Configuração de infraestrutura PostgreSQL em docker-compose, scripts de inicialização e alvos makefile - Pedro Victor - 2026-10-27 - #9 - fccdfdb
- Implementação das migrações Alembic para schemas signup e member com tabelas, índices e concessão de privilégios para platform_auth - Pedro Victor - 2026-10-27 - #9 - fccdfdb
- Refinamento de schemas de resposta com status booleano, injeção de dependência no controller e tratamento de debug no middleware - Pedro Victor - 2026-10-27 - #9 - fccdfdb
- Elaboração do diagrama de banco relacional em DBML e documentação detalhada de tabelas no MkDocs - Pedro Victor - 2026-10-27 - #9 - fccdfdb

---

2026-10-22 - [REFACTOR] - Migração de contratos de resposta para schemas Pydantic e modularização do serviço de signup

Detalhes:

- Substituição dos contratos genéricos em contracts/ por modelos Pydantic centralizados em schema/default/ - Pedro Victor - 2026-10-22 - #9 - 39344cc
- Reorganização do fluxo de registro para pacote modular sob service/signup/ com controller e service dedicados - Pedro Victor - 2026-10-22 - #9 - 39344cc
- Atualização de diagramas Mermaid (classes e sequência de signup) e documentação de endpoints no MkDocs - Pedro Victor - 2026-10-22 - #9 - 39344cc

---

2026-10-15 - [NEW] - Estruturação do roteador de autenticação e endpoint inicial de signup

Detalhes:

- Criação do APIRouter modular com controller v1 e endpoint de signup - Pedro Victor - 2026-10-15 - #9 - 1c955b7
- Implementação do AuthService e modelo de validação SignupRequest - Pedro Victor - 2026-10-15 - #9 - 1c955b7
- Ajuste dos contratos de resposta para retorno assíncrono em JSONResponse e documentação de arquitetura - Pedro Victor - 2026-10-15 - #9 - 1c955b7

---

2026-10-15 - [NEW] - Padronização de respostas da API, logger customizado e handler de exceções

Detalhes:

- Implementação dos contratos de resposta padrão (BaseApiResponse, BaseApiError, BaseApiSuccess) - Pedro Victor - 2026-10-15 - #9 - c36d519
- Implementação do CustomLogger e do ServerExceptionHandler para captura global de exceções HTTP 500 - Pedro Victor - 2026-10-15 - #9 - c36d519
- Atualização do gatilho do workflow do Gemini para pull_request - Pedro Victor - 2026-10-15 - #9 - c36d519

---

2026-10-15 - [NEW] - Estrutura inicial do microserviço de autenticação e configurações de desenvolvimento

Detalhes:

- Criação do esqueleto da aplicação FastAPI com endpoint de health check, configuração do Alembic e template de ambiente - Pedro Victor - 2026-10-15 - #9 - 565782a
- Inclusão das configurações de debug do VS Code e ajuste no .gitignore - Pedro Victor - 2026-10-15 - #9 - 565782a

---

2026-10-14 - [BUILD] - Alteração do gatilho do workflow do Gemini para execução manual

Detalhes:

- Mudança do evento de disparo de pull_request para workflow_dispatch no workflow gemini-pr-review.yml para execução manual sob demanda - Pedro Victor - 2026-10-14 - Sem card - pendente

---

2026-10-14 - [CHG] - Atualização do design system e paleta de cores para o estilo Cyber-Glassmorphic

Detalhes:

- Definição da estética Cyber-Glassmorphic, paleta de cores cósmica/neon e tokens visuais em DESIGN.md - Pedro Victor - 2026-10-14 - Sem card - f0ab69e
- Inclusão dos protótipos de tela mobile (login) e novos assets de logotipo - Pedro Victor - 2026-10-14 - Sem card - f0ab69e
- Remoção de protótipos legados e brief desatualizado em AI/Desing - Pedro Victor - 2026-10-14 - Sem card - f0ab69e

---

2026-10-14 - [DOC] - Proibição explícita de git pull e git push no fluxo da skill git-commit

Detalhes:

- Adição de diretrizes e checklist proibindo explicitamente operações remotas (git pull e git push) durante o ciclo de commit na skill git-commit - Pedro Victor - 2026-10-14 - Sem card - 862e310

---

2026-10-14 - [BUILD] - Ajuste nas instruções do workflow de code review do Gemini

Detalhes:

- Inclusão de diretriz de concisão e objetividade nas revisões automáticas de PR - Pedro Victor - 2026-10-14 - Sem card - a4af0e9

---

2026-10-14 - [BUILD] - Configuração de normalização de quebras de linha e espaços em branco (.gitattributes e .editorconfig)

Detalhes:

- Criação do .gitattributes para normalização automática de LF e prevenção de conflitos de CRLF entre Windows, Mac e Linux - Pedro Victor - 2026-10-14 - Sem card - 52dd97f
- Criação do .editorconfig para padronização de quebra de linha (LF), encoding (UTF-8) e remoção de espaços em branco nos editores - Pedro Victor - 2026-10-14 - Sem card - 52dd97f
- Atualização do README.md com referências às boas práticas de normalização e editorconfig - Pedro Victor - 2026-10-14 - Sem card - 52dd97f

---

2026-10-14 - [DOC] - Resolução de sugestões do code review (SOLID, DI, logging, performance e formato de data ISO 8601)

Detalhes:

- Inclusão de diretrizes de SOLID (SRP/DIP) nos diagramas de classe - Pedro Victor - 2026-10-14 - Sem card - 6142b48
- Inclusão de diretrizes de DI, logging e monitoramento nos diagramas de sequência - Pedro Victor - 2026-10-14 - Sem card - 6142b48
- Inclusão de diretrizes de performance de queries no DBML - Pedro Victor - 2026-10-14 - Sem card - 6142b48
- Padronização do formato de data para YYYY-MM-DD (ISO 8601) no changelog e skill de commit - Pedro Victor - 2026-10-14 - Sem card - 6142b48

---

2026-10-14 - [DOC] - Atualização de links absolutos para caminhos relativos nas skills de documentação e git

Detalhes:

- Substituição de referências file:// por caminhos relativos nos arquivos de skills para portabilidade do repositório - Pedro Victor - 2026-10-14 - Sem card - ef0247c

---

2026-10-14 - [BUILD] - Configuração de diretrizes de IA, skills de agentes e padronização de documentação

Detalhes:

- Criação e padronização das skills de git, mermaid, dbdiagram e orquestrador de documentação - Pedro Victor - 2026-10-14 - Sem card - 8f12ea7
- Configuração de regras globais em GEMINI.md, AI/Rules.md e AI/Default.md - Pedro Victor - 2026-10-14 - Sem card - 8f12ea7
- Atualização do mkdocs.yml e inclusão da seção de regras de negócio - Pedro Victor - 2026-10-14 - Sem card - 8f12ea7
- Adição do arquivo .gitignore para o repositório - Pedro Victor - 2026-10-14 - Sem card - 8f12ea7

---

2026-07-10 - [BUILD] - Criação dos arquivos base de AI e makefile

Detalhes: 

---

2026-03-22 - [DOC] - Criação do arquivos principais de logs

Detalhes:

- Criação do arquivo de changelog - Pedro Victor - 2026-03-22 - Sem carde - [N/A]
- Criação do serviço de documentação - Pedro Victor - 2026-03-22 - Sem carde - [N/A]
- Atualização do arquivo de readme - Pedro Victor - 2026-03-22 - Sem carde - [N/A]
