# Uso dos hooks

Os hooks são o contrato público deste pacote com o [pre-commit]; os ids
abaixo vêm do arquivo `.pre-commit-hooks.yaml`, que é a fonte de verdade.
Mudança de nome, id ou argumento é quebra de API.

## Lista de hooks

| id | entry | stages | função |
|---|---|---|---|
| `check-commit-footer` | `check-commit-footer` | commit-msg, manual | valida os rodapés do último parágrafo da mensagem de commit (`Closes`, `Refs`, `Signed-off-by`, `Co-authored-by`, `Reviewed-by`, `Acked-by`; referência `#<id>` só em `Closes`/`Refs`) |
| `check-manual-changelog` | `check-manual-changelog` | commit-msg, manual | exige mensagem `build:` quando o `CHANGELOG.md` staged muda (comparado com `HEAD`) |
| `check-manual-version` | `check-manual-version` | commit-msg, manual | exige mensagem `build:` quando a versão staged muda em `[project].version` do `pyproject.toml` ou em `**/version.txt` (compara índice com `HEAD`) |
| `check-len-first-line` | `check-len-first-line` | prepare-commit-msg | valida o comprimento da primeira linha da mensagem de commit |
| `check-precommit-installed` | `is-precommit-installed` | pre-commit, pre-push | garante que o pre-commit está instalado no projeto |
| `check-valid-branchname` | `is-valid-branchname` | pre-commit, pre-push | valida o nome da branch atual (protegidas e padrões válidos) |
| `check-valid-filenames` | `is-valid-filename` | pre-commit, pre-push | valida nomes de arquivo Python (snake_case, comprimento, localização de testes) |
| `clean-commit-message` | `clean-commit-msg` | prepare-commit-msg | limpa o arquivo de mensagem de commit |
| `detect-key` | `detect-key` | commit | detecta a presença de chaves privadas nos arquivos staged |
| `effort-message` | `effort-msg` | post-commit | exibe mensagem de esforço/motivação após o commit |
| `effort-random-message` | `effort-random-msg` | post-commit | exibe mensagem de esforço aleatória após o commit |
| `footer-signed-off-by` | `set-footer-signed-off-by` | prepare-commit-msg | insere rodapé `Signed-off-by` via `git interpret-trailers` |
| `insert-diff-commit` | `insert-diff-commit` | prepare-commit-msg | insere o `git diff --cached` na mensagem de commit |
| `validate-message-commit` | `is-valid-msg-commit` | commit-msg | valida o formato da mensagem de commit (Conventional Commits) |
| `set_issue_from_branch_cli` | `set-issue-from-branch` | prepare-commit-msg | extrai o número da issue do nome da branch e insere na mensagem |
| `set-type-from-status` | `set-type-from-status` | prepare-commit-msg | deduz o tipo Conventional Commits pelos arquivos staged e insere na mensagem (não sobrescreve tipo existente) |
| `check-type-from-status` | `check-type-from-status` | commit-msg | bloqueia divergência objetiva entre o tipo declarado na mensagem e o tipo deduzido dos arquivos staged |

## Argumentos comuns

Todos os comandos aceitam:

- `-N` / `--nonexequi` — não executa o hook (o hook informa que não rodou
  devido à opção).
- `-V` / `--version` — versão do pacote.

Hooks `check-valid-filenames` e `check-len-first-line` também aceitam
limites configuráveis (ex.: `--min-len`, `--max-len`,
`--min-first-line`, `--max-first-line`).

## Modelo completo

O modelo de `.pre-commit-config.yaml` pronto para copiar está no
[README][modelo] — ele é a fonte publicada para projetos consumidores.

[pre-commit]: https://pre-commit.com/
[modelo]: https://github.com/development-incolume/incolume.py.githooks#usage
