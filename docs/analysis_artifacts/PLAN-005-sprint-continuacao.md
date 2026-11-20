# PLAN-005 — Sprint de continuação do PLAN-004

- **Data:** 2026-11-20
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.27.0
- **Status:** Em execução (2026-11-20)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Dr. Nefário OpenBot

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Objetivo

Continuar o PLAN-004 (sprint de QA). O PLAN-004 destravou os bloqueios
(P0-1 e P0-02) mas deixou por fazer o P0-3, o merge da #319, as reservas
P1 e a atualização de documentação (#429). Este plano regista e ordena esse
fecho.

## 2. Fases da sprint

### 2.1 #319 — validações de mensagem emancipadas

| Issue | Tarefa | Artefacto |
|---|---|---|
| #319 | merge da branch `319-emancipa-validacoes` (`1726248`), rebaseada sobre `dev 51eb41d` | `core/rules.py`, hooks, testes |

A abordagem está aprovada pelo Brito. O commit `36b20e7` (abordagem antiga)
segue revertido em `319-validacoes-independentes`.

### 2.2 P0-3 — gates decorativos

| Issue | Tarefa | Artefacto |
|---|---|---|
| #431 | o CI não roda `pre-commit`; `mypy`/`ty` com `continue-on-error: true` | `.github/workflows/python-package.yml` |

Critério: o workflow roda `pre-commit run --all-files` e `mypy`/`ty` passam
a bloquear o merge.

### 2.3 P1 — reservas do Dave (4–11)

| Issue | Reserva |
|---|---|
| #432 | 4 — `check-len-first-line` mente no erro e ignora `max < 50` |
| #433 | 5 — `dev`/`tags` desprotegidos |
| #434 | 6 — hooks inertes por `-N` |
| #435 | 7 — seis hooks publicados não usados |
| #436 | 8 — `detect-key` público com `types` em AND |
| #437 | 9 — `insert-diff-commit` no gancho errado |
| #438 | 10 — bug em `check_valid_branchname_cli` |
| #439 | 11 — `check_type_commit_msg` `IsADirectoryError` |

### 2.4 #429 — atualização de documentação

| Issue | Tarefa |
|---|---|
| #429 | descrição do pacote (fonte → plugin pre-commit) e secção de instalação via pip/uv |

## 3. Ordenação

1. #430 (PLAN-005) — registo deste plano.
2. #431 (P0-3) — gate de CI; destrava a verificação dos restantes.
3. #319 — merge da branch aprovada.
4. P1 (#432–#439) — reservas, na ordem.
5. #429 — documentação.

## 4. Critério de aceite do plano

- `docs/analysis_artifacts/PLAN-005-sprint-continuacao.md` criado;
- as issues das reservas criadas e ligadas a este plano.

## 5. Referências

- PLAN-004 — `docs/analysis_artifacts/PLAN-004-sprint-qa.md`.
- Parecer de QA do Dave sobre `dev 815363a` (`1.26.0a18`).
