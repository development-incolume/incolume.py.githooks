# SPEC-001 — Plano de execução do incolume.py.githooks

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.25.0a9
- **Status:** Aprovado (2026-11-19)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

## 1. Fases do ciclo

1. **Tarefa.** Branch derivada de `dev`, worktree em `wt/<id>-<slug>`.
2. **Implementação.** TDD quando houver comportamento; teste vermelho antes da
   implementação.
3. **QA local.** `ruff check`, `ruff format`, `mypy`, `pytest` verdes antes do
   commit.
4. **Integração.** Merge em `dev` pelo integrador, com `merge --no-ff`, a
   partir do HEAD de `dev`.
5. **Versionamento.** Bump de alpha em `dev` a cada tarefa concluída.
6. **Fechamento.** `dev` → `tags` (merge `--no-ff`), versão estável na `tags`,
   tag anotada; `main` recebe `tags` por PR.

## 2. Sprint de documentação (ciclo 1.25.0)

| Issue | Entrega |
|---|---|
| #401 | estrutura de artefactos e exclusão no `mkdocs.yml` |
| #402 | `PRD-001-githooks.md` |
| #403 | `ADR-001-githooks.md` |
| #404 | `SPEC-001-githooks.md` |
| #405 | `PLAN-001-sprint-documentacao.md` |

## 3. Critérios de aceite

- Cada issue tem branch derivada de `dev`, commit com a descrição no padrão
  `<tipo>: #<id> <descrição>` e QA verde.
- Documento de análise com cabeçalho (data, versão, status), autor Brito e
  agente como coautor.
- `mkdocs build` verde e 0 links quebrados; artefactos fora do site.
- Nenhuma dependência nova sem aprovação explícita.

## 4. Branches e worktrees

- Nomenclatura: `<id>-<slug>` (ex.: `401-analysis-artifacts`).
- Worktree: `wt/<id>-<slug>`, derivado de `dev`.
- Identidade local do worktree: `Britodfbr <brito@incolume.com.br>`; o agente
  entra como `Co-authored-by`.
- Ambiente do worktree: `uv sync --frozen --python 3.12 --all-groups`
  (interpretação estável quando o mais novo quebra em build nativo).
- Remoção do worktree após o merge e `git worktree prune`.

## 5. Rito de entrega

- Toda alteração tem issue aberta; sem issue, não há branch nem commit.
- Teste do critério antes da implementação (vermelho → verde → refatorar).
- Commit atômico; `docs:`, `chore:` e `refactor:` não fecham issue.
- O agente implementador não mescla o próprio trabalho; o merge em `dev` é
  local, do integrador.
- PR só existe para `main`, no fechamento da release.
- Nenhuma biblioteca instalada sem aprovação explícita.
