# PLAN-002 — Sprint ty do incolume.py.githooks

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.27.0
- **Status:** Em aprovação (2026-11-19)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Kevin OpenBot

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Objetivo

Adicionar o `ty` ao fluxo de QA do repositório, em paralelo ao `mypy`, e
registrar a substituição futura do `mypy` por `ty` no `Unreleased`.

O `mypy` não sai nesta sprint. Ele permanece com a configuração atual em
`.mypy.ini` e no fluxo de QA.

## 2. Decisões confirmadas com o Brito

| # | Decisão | Efeito |
|---|---|---|
| D1 | `ty` entra em paralelo; `mypy` permanece | duas checagens de tipo no QA |
| D2 | CI em modo informativo (`continue-on-error: true`) | `ty` não falha o build no CI |
| D3 | `ty.toml` traduz só o que tem equivalente; `extra-paths = ["incolume", "tests"]` | `.mypy.ini` intocado |
| D4 | `#256` é duplicata da `#257` (já entregue) | tarefa de fechamento |
| D5 | tag `Unreleased` recriada; `CHANGELOG.md` regenerado no fechamento | rito de release mantido |
| D6 | 5 issues granulares | uma tarefa = uma issue |

## 3. Tarefas da sprint

| Issue | Tarefa | Artefacto |
|---|---|---|
| #409 | `ty` como dependência de desenvolvimento | `pyproject.toml` |
| #410 | configuração do mypy portada para `ty.toml` | `ty.toml` |
| #411 | `ty` no fluxo de QA | `.github/workflows/python-package.yml`, `.pre-commit-config.yaml`, `AGENTS.md`, `PRD-001`, `ADR-001`, `SPEC-001` |
| #412 | `ADR-002` + tag `Unreleased` | `docs/analysis_artifacts/ADR-002-ty.md`, tag `Unreleased` |
| #408 | `PLAN-002` | `docs/analysis_artifacts/PLAN-002-sprint-ty.md` |
| #413 | registar `#256` como duplicata da `#257` | `PLAN-002` |
| #415 | `[project-manager]` com `script = "uv"` no `ty.toml` | `ty.toml` |
| #416 | `root = ["./"]` no `[environment]` do `ty.toml` | `ty.toml` |

### 3.1 Dependência

- `ty>=0.0.107` no grupo `dev` de `pyproject.toml`.
- Aprovação do `ty` registrada na issue da tarefa.
- Commits: `build(deps): adiciona ty`.

### 3.2 Configuração do ty

- Novo arquivo `ty.toml` (não `[tool.ty]` no `pyproject.toml`).
- Ambiente: `python-version = "3.11"`, `extra-paths = ["incolume", "tests"]`.
- `src.include` com `incolume` e `tests`.
- Regras: equivalente ao estrito do mypy, dentro do que o ty suporta.
- Flags do `.mypy.ini` sem equivalente no ty: registadas no `ADR-001` como
  diferença de semântica, não silenciadas.

### 3.3 Fluxo de QA

- CI `.github/workflows/python-package.yml`: passo `Check with ty`, com
  `continue-on-error: true`, `uv run ty check`.
- `.pre-commit-config.yaml`: hook de `https://github.com/astral-sh/ty-pre-commit`,
  rev `v0.0.107`.
- `AGENTS.md`: toolchain e QA passam a citar o `ty`.
- `PRD-001`, `ADR-001` e `SPEC-001`: QA cita o `ty`.

### 3.4 Registro Unreleased

- Recriar a tag anotada `Unreleased` com a anotação nova, local e remota
  (`git push -f origin Unreleased`).
- A anotação informa a substituição futura do `mypy` por `ty`.
- A regeneração do `CHANGELOG.md` fica para o fechamento da release, como manda
  o rito.

### 3.5 Fechamento da #256

- Conferir que `Enum.to_tuple()` e o teste existente atendem.
- Commit com `Closes #256`.

## 4. Critérios de aceite

- `ty` no grupo `dev`, aprovação registrada na issue.
- `ty.toml` com ambiente e regras equivalentes; pendências no `ADR-001`.
- CI com o passo `Check with ty` (`continue-on-error: true`).
- Hook do `ty` no `.pre-commit-config.yaml`.
- `AGENTS.md`, `PRD-001`, `ADR-001` e `SPEC-001` citam o `ty`.
- Tag `Unreleased` recriada com a substituição futura.
- `#256` fechada por commit com `Closes #256`.
- QA verde: `ruff check`, `ruff format --check`, `mypy`, `pytest` e cobertura
  mínima de 99,99 (`.coveragerc.toml`).

## 5. Pendências e reservas futuras

| Assunto | Estado | Tratamento |
|---|---|---|
| `gcl` falha no Windows (`UnicodeDecodeError`) | bloqueador | regeneração do `CHANGELOG.md` no fechamento; correção no `incolume.py.changelog` em issue própria |
| flags do mypy sem equivalente no ty | pendência | registadas no `ADR-001` |
| `#319` | aberta | fora da sprint |
| `#256` | fechada (duplicada de `#257`) | fechada por commit com `Closes #256`; fora do escopo |

## 6. Fora de escopo

- Remover o `mypy` do QA (a substituição é futura).
- Corrigir o `incolume.py.changelog`.
- Reescrever código fora do necessário para as tarefas.

## 7. Riscos

- `ty` é beta (`0.0.x`); a API e os diagnósticos podem mudar entre versões.
- `ty` não reproduz 1:1 o estrito do mypy; o `ADR-001` regista as diferenças.
