# Diretrizes Obrigatórias do Projeto

Em toda inicialização e execução neste projeto, o agente DEVE seguir e considerar ativas as regras e instruções dos seguintes arquivos essenciais:

## Arquivos Base e Regras Globais

@[AI/Start-here.md](AI/Start-here.md)

@[AI/Default.md](AI/Default.md)

@[AI/Rules.md](AI/Rules.md)

---

## Instruções de Inicialização (Checklist Padrão)

Toda vez que interagir no projeto:
1. Respeitar o fluxo de [AI/Default.md](AI/Default.md):
   - Solicitar um breve resumo de contexto, se necessário.
   - Perguntar se o usuário deseja uma opinião/sugestão ou uma implementação/correção direta.
   - Se a tarefa envolver design/front-end, consultar `AI/Desing/`.
2. Cumprir integralmente todas as exigências de [AI/Rules.md](AI/Rules.md) (Changelog, README, Documentação, Testes, Diagramas Mermaid/dbdiagram, políticas de commit/branch e não leitura de `.env`).
3. Para procedimentos especializados (git, documentação, banco de dados, linguagens), consultar as skills correspondentes em `AI/GEMINI/skills/` e `.agents/skills/`.
