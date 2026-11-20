# PRD-001 — Produto: incolume.py.githooks

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.26.0
- **Status:** Aprovado (2026-11-19)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

## 1. Propósito

O `incolume.py.githooks` é a fonte dos hooks git do time incolume: um
plugin de `pre-commit` que publica, em `.pre-commit-hooks.yaml`, o contrato
público de hooks que os projetos consumidores copiam para o seu
`.pre-commit-config.yaml`. O repositório fornece as regras; ele não consome
decisões de outros projetos.

## 2. Público-alvo

- Projetos Python do ecossistema incolume (ex.: `incolume.py.changelog`).
- Equipes que adotam `pre-commit` e Conventional Commits.
- Agentes de IA que atuam como colaboradores, regidos pelo `AGENTS.md`.

## 3. Problemas resolvidos

- Padronizar mensagem de commit (tipo, comprimento da primeira linha,
  rodapés e referência de issue).
- Impedir o versionamento de segredos (`detect-key`).
- Garantir o rito de branch, de versionamento e de changelog.
- Automatizar a montagem da mensagem (issue, tipo, diff, signed-off).
- Dar feedback pós-commit (`effort-message`, `effort-random-message`).

## 4. Objetivos

- Um hook = um módulo em `incolume/py/githooks/` + comando Click em
  `incolume/py/githooks/cli/cli.py` + entry-point em `[project.scripts]`.
- Contrato público estável e versionado (semver).
- Qualidade mensurável: ruff, format, mypy e pytest verdes, cobertura
  mínima de 99.99%.
- Documentação consultável: `README.md`, site mkdocs e artefactos de
  análise (`docs/analysis_artifacts/`).

## 5. Não-objetivos

- Não é framework de CI nem substituto do `pre-commit`.
- Não gerencia releases de outros projetos.
- Não impõe políticas fora do ecossistema incolume.
- Não publica os artefactos de análise no site (pasta excluída no
  `mkdocs.yml`).

## 6. Requisitos funcionais

Contrato público (`.pre-commit-hooks.yaml`), 17 hooks:

| id | stages | função |
|---|---|---|
| `check-commit-footer` | commit-msg, manual | valida rodapés do último parágrafo |
| `check-len-first-line` | prepare-commit-msg | valida o comprimento da primeira linha |
| `check-manual-changelog` | commit-msg, manual | exige `build:` quando `CHANGELOG.md` staged muda |
| `check-manual-version` | commit-msg, manual | exige `build:` quando a versão staged muda |
| `check-precommit-installed` | pre-commit, pre-push | garante o pre-commit instalado |
| `check-type-from-status` | commit-msg | bloqueia divergência de tipo em relação aos staged |
| `check-valid-branchname` | pre-commit, pre-push | valida o nome da branch |
| `check-valid-filenames` | pre-commit, pre-push | valida nomes de arquivo Python |
| `clean-commit-message` | prepare-commit-msg | limpa o arquivo de mensagem |
| `detect-key` | commit | detecta chaves privadas |
| `effort-message` | post-commit | mensagem de esforço pós-commit |
| `effort-random-message` | post-commit | mensagem de esforço aleatória |
| `footer-signed-off-by` | prepare-commit-msg | insere `Signed-off-by` |
| `insert-diff-commit` | prepare-commit-msg | insere o `git diff --cached` |
| `set-issue-from-branch` | prepare-commit-msg | extrai a issue do nome da branch |
| `set-type-from-status` | prepare-commit-msg | deduz o tipo Conventional Commits |
| `validate-message-commit` | commit-msg, manual | valida o formato da mensagem |

## 7. Requisitos não-funcionais

- Python `>=3.11,<4`; dependências enxutas (`click`, `colorama`,
  `deprecated`, `icecream`, `tqdm`, `tomli` em `<3.11`).
- CLI em grupo chain `githooks-cli`, com `-N/--nonexequi` e `-V/--version`
  em todos os comandos.
- Cobertura mínima real de 99.99% (`.coveragerc.toml`).
- Estilo: line-length 79, aspas simples, target py311.
- Verificação de tipos em paralelo: `mypy` (obrigatório) e `ty`
  (`uv run ty check`, config em `ty.toml`), este informativo.

## 8. Critérios de aceite

- Contrato `.pre-commit-hooks.yaml`, `README.md` e `docs/` coerentes.
- QA verde antes de cada commit (ruff check, ruff format, mypy, pytest).
- Rito de entrega `dev` → `tags` → `main`, sempre com `merge --no-ff`.

## 9. Dependências

- Runtime: `click>=8.2.1`, `colorama>=0.4.6`, `deprecated>=1.3.1`,
  `icecream>=2.1.7`, `tomli>=2.2.1` (`<3.11`), `tqdm>=4.67.1`.
- Dev: `incolume-py-changelog`, `mypy`, `pre-commit`, `pyyaml`, `pytest`,
  `pytest-click`, `pytest-cov`, `pytest-env`, `pytest-mock`, `ruff`.
- Docs: `mkdocs`, `mkdocs-material`, `mkdocs-static-i18n`, `mkdocstrings`,
  `mkdocstrings-python`.
- Build: `uv_build>=0.8.9,<0.9.0`.

## 10. Restrições

- Nenhuma dependência nova sem aprovação explícita do usuário.
- Mudança de nome, id ou argumento de hook é quebra de API (semver).
- Em divergência entre código e documento, o documento ganha.
- Nenhum segredo em código, teste, log ou fixture.

## 11. Levantamento (fontes)

- Código: `incolume/py/githooks/` e `incolume/py/githooks/cli/cli.py`.
- Contrato: `.pre-commit-hooks.yaml`.
- Modelo publicado: `README.md`.
- Documentação: `docs/hooks.md`, `docs/cli.md`, `docs/api.md`.
- Histórico: `CHANGELOG.md` e anotações das tags (`git tag -n`).
- Regras: `AGENTS.md` e `docs/regras.md`.
