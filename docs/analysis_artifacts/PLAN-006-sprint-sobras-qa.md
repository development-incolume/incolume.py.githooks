# PLAN-006 — Sprint de sobras de QA do PLAN-004

- **Data:** 2026-11-21
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.28.0a10
- **Status:** Em aprovação (2026-11-21)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Qwen Code

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Objetivo

Transportar as sobras do PLAN-004 que nunca viraram issue: as melhorias
de teste **a, b, d, g**, a pendência de decisão do `deprecated 3.0.1` e a
limpeza da branch `319-validacoes-independentes`. Por decisão do Brito
(2026-11-21), o escopo «somente as sobras do plano 4» fica ampliado com o
transporte da **#437** (evolução do `insert-diff-commit`), fechada sem
implementação no PLAN-005.

## 2. Reservas

### 2.1 Melhorias de teste do `.pre-commit-config.yaml` (PLAN-004 §2.4)

| # | Melhoria |
|---|---|
| a | contrato do config: todo `id` declarado existe no repositório; todo hook local tem entry-point em `[project.scripts]` |
| b | paridade config x `.pre-commit-hooks.yaml` para os 18 ids (`stages`, `pass_filenames`, `always_run`, `types`) |
| d | assert de que nenhum hook local recebe `-N` por padrão |
| g | E2E com git temporário: YAML/JSON com chave privada, commit simulado, rejeição |

### 2.2 Evolução do `insert-diff-commit` (transporte da #437)

A #437 foi fechada como «not planned» por decisão explícita do Brito
(2026-11-21); as mudanças ficam como evolução neste plano. Formato alvo
escolhido: **1b — `git diff --cached --stat`** (estatística de linhas por
arquivo, substituindo o `--name-status -r` atual).

Diagnóstico verificado (2026-11-21, `dev ec0eed8`, `1.28.0a10`):

- Config local usa `stages: [commit-msg, manual]`; o manifesto público e
  o `docs/hooks.md` dizem `prepare-commit-msg`. Documento ganha: corrigir
  o config. No `commit-msg` o editor já fechou e o diff chega tarde para
  o autor.
- `get_git_diff()` (`incolume/py/githooks/core/utils.py`) roda
  `git diff --cached --name-status -r` desde o porte original (#61) —
  nunca houve «diff parcial» no histórico; a reserva do Dave («diff
  inteiro») não procede contra o código atual.
- O teste atual (`core_test.py::test_get_diff`) mocka a saída sem conferir
  o comando git — nada trava o formato.
- `docs/hooks.md` exagera: diz «insere o `git diff --cached`» sem
  qualificar o formato.

Etapas (issue própria abre quando a tarefa começar):

1. Branch/worktree `<id>-insert-diff-evolucao` a partir de `dev`,
   identidade local do rito.
2. Testes vermelhos: (a) contrato de stages — config == público ==
   `[prepare-commit-msg, manual]`; (b) `get_git_diff` chama git com
   `--stat` (comando conferido no mock, não só a saída); (c) CLI insere o
   resultado na mensagem antes da primeira linha `#`.
3. Fixes: stages do `insert-diff-commit` no `.pre-commit-config.yaml` →
   `prepare-commit-msg`; `get_git_diff` → `git diff --cached --stat`.
4. Docs: linha do `insert-diff-commit` em `docs/hooks.md` e docstrings
   descrevem o `--stat`; README não fixa stages/formato (nada a mudar lá).
5. Semver: o formato do conteúdo inserido é comportamento visível ao
   consumidor — avaliar o componente do bump no fecho do ciclo.
6. QA canônica verde (ruff, mypy, ty, pytest) → commit `fix:` com
   `Closes` da nova issue.
7. Merge `--no-ff` / bump / push somente com aprovação explícita do
   Brito.

### 2.3 `deprecated 3.0.1` / `requires-python`

Pendência de decisão do Brito: o marcador `python_full_version >= '3.12'`
da dependência `deprecated 3.0.1` justifica subir o `requires-python`
para `>=3.12` (3.10 já caiu na #420). A decisão é humana; a tarefa abre
issue quando começar.

### 2.4 Limpeza da branch `319-validacoes-independentes`

Branch nunca integrada; o commit `36b20e7` (tornar o `#id` opcional) está
descartado — a abordagem definitiva da #319 seguiu por
`319-emancipa-validacoes` (PLAN-005). O worktree
`wt/319-validacoes-independentes` ainda existe. A remoção da branch e do
worktree exige aprovação do Brito na execução.

## 3. Ordenação

1. **a** — contrato do config (ids + entry-points).
2. **b** — paridade config x contrato público (18 ids).
3. **d** — nenhum hook local com `-N` por padrão.
4. **g** — E2E do `detect-key` com git temporário.
5. **Evolução da #437** — `insert-diff-commit` (stages + `--stat` + docs).
6. **deprecated** — decisão do `requires-python >=3.12`.
7. **Branch 319** — limpeza de `319-validacoes-independentes`.

## 4. Política de issues

Decisão do Brito (2026-11-21): «abrir por tarefa, quando a tarefa
começar». As reservas ficam **sem issue** neste plano; cada issue abre
quando a sua tarefa começar. Só o documento do plano tem issue prévia:
**#444**.

## 5. Já coberto — não retransportar

| Melhoria PLAN-004 | Issue que cobriu |
|---|---|
| c — hooks publicados não usados, com justificativa | #435 |
| e — texto de erro do `check-len-first-line` | #432 |
| f — `is-valid-branchname` contra `dev` e `tags` | #433 |
| h — job de CI com `pre-commit run --all-files` | #431 |

## 6. Fora de escopo

- #438 e #439 — seguem no PLAN-005.
- Achados da auditoria de 2026-11-21 (#440–#443).
- Qualquer implementação neste commit — este plano só regista e ordena.

## 7. Critério de aceite do plano

- `docs/analysis_artifacts/PLAN-006-sprint-sobras-qa.md` criado, com
  cabeçalho (data, versão, status), autor Brito e agente como coautor;
- PLAN-004 §4 atualizado com nota de transporte para este plano;
- cada reserva executada com issue própria, TDD e QA canônica verde;
- merge `--no-ff`, bump e push somente com aprovação explícita do Brito.

## 8. Referências

- PLAN-004 — `docs/analysis_artifacts/PLAN-004-sprint-qa.md` (§2.4 e §4).
- PLAN-005 — `docs/analysis_artifacts/PLAN-005-sprint-continuacao.md`.
- Issue #444 e comentário de transporte da #437
  (issuecomment-7074469919, 2026-11-22).
- Parecer de QA do Dave sobre `dev 815363a` (`1.26.0a18`).