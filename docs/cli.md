# Referência do CLI

O grupo `githooks-cli` agrega todos os comandos do pacote; cada um também é
publicado como entry-point em `[project.scripts]` do `pyproject.toml`,
consumível diretamente pelo pre-commit.

## Comandos

| comando | função |
|---|---|
| `githooks-cli` | grupo chain com todos os comandos |
| `check-len-first-line` | valida o comprimento da primeira linha da mensagem |
| `check-type-commit-msg` | valida o tipo da mensagem (Conventional Commits) |
| `clean-commit-msg` | limpa o arquivo de mensagem de commit |
| `detect-key` | detecta chaves privadas nos arquivos informados |
| `effort-msg` | exibe mensagem de esforço pós-commit |
| `effort-random-msg` | exibe mensagem de esforço aleatória (`--fixed` fixa a mensagem) |
| `insert-diff-commit` | insere o `git diff --cached` na mensagem de commit |
| `is-precommit-installed` | verifica se o pre-commit está instalado |
| `is-valid-branchname` | valida o nome da branch atual |
| `is-valid-filename` | valida nomes de arquivo Python |
| `is-valid-msg-commit` | valida o formato da mensagem de commit |
| `set-footer-signed-off-by` | insere rodapé `Signed-off-by` |
| `set-issue-from-branch` | extrai a issue do nome da branch para a mensagem |

## Opções

- `-N` / `--nonexequi` — presente em todos os comandos: reporta que o hook
  não executou devido à opção.
- `-V` / `--version` — versão do pacote.
- `-h` / `--help` — ajuda do comando.
