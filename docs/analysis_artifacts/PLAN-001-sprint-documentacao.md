# PLAN-001 — Sprint de documentação do incolume.py.githooks

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.27.0
- **Status:** Aprovado (2026-11-19)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Tarefas da sprint

| Issue | Tarefa | Artefacto |
|---|---|---|
| #401 | estrutura de artefactos e `exclude_docs` | `docs/analysis_artifacts/` + `mkdocs.yml` |
| #402 | PRD-001 | `docs/analysis_artifacts/PRD-001-githooks.md` |
| #403 | ADR-001 | `docs/analysis_artifacts/ADR-001-githooks.md` |
| #404 | SPEC-001 | `docs/analysis_artifacts/SPEC-001-githooks.md` |
| #405 | PLAN-001 | `docs/analysis_artifacts/PLAN-001-sprint-documentacao.md` |

Critério transversal: `mkdocs build` verde e 0 links quebrados; artefactos
excluídos do site.

## 2. Pendências e reservas futuras

| Issue | Estado | Assunto | Tratamento |
|---|---|---|---|
| #319 | aberta | emancipar as validações de mensagem | reserva futura, fora da sprint |
| #256 | aberta | `Enum.to_tuple()` | reserva futura, fora da sprint |
| #175 | fechada | fatorar regras em design partner policy | fora do escopo |

## 3. Decisões do ciclo 1.25.0

- **#396** — `check-precommit-installed` passa a ler o `INSTALL_PYTHON` do
  script.
- **#397** — hook `set-issue-from-branch` corrigido no contrato público.
- **#398** — regras de autoria do `AGENTS.md` atualizadas.
- **Unreleased** — descontinuar o suporte a Python 3.11, conforme o status de
  versões do Python.

## 4. Fora de escopo

- Reescrita de código fora do necessário para as tarefas.
- Publicação dos artefactos de análise no site.
