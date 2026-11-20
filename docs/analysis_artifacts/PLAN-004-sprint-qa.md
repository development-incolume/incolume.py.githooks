# PLAN-004 — Sprint de QA do incolume.py.githooks

- **Data:** 2026-11-20
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.26.0
- **Status:** Em execução (2026-11-20)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Objetivo

Destravar o gate de QA do repositório. O `pre-commit run` abortava na
inicialização — nenhum hook rodava — e os gates de tipo e de hook eram
decorativos. Esta sprint trata os bloqueios (P0), o redesenho das validações de
mensagem (#319) e regista as reservas de QA (P1) levantadas pelo Dave.

## 2. Fases da sprint

### 2.1 P0 — bloqueiam qualquer gate

| Item | Tarefa | Issue | Artefacto |
|---|---|---|---|
| P0-1 | tirar o hook `mypy` do bloco do `ruff-pre-commit` | #425 | `.pre-commit-config.yaml` |
| P0-2 | alinhar `pre-commit` e git quanto ao `git ls-files --deduplicate` | #426 | `.pre-commit-config.yaml`, `pyproject.toml`, `uv.lock` |
| P0-3 | gates decorativos: nenhum workflow roda `pre-commit`; `mypy`/`ty` com `continue-on-error` | — | `.github/workflows/python-package.yml` |

O P0-3 não virou issue: é reserva para a próxima sprint.

### 2.2 #319 — validações de mensagem emancipadas

| Issue | Tarefa | Artefacto |
|---|---|---|
| #319 | emancipar as validações de tipo e de formato em hooks distintos, com lista única de tipos | `core/rules.py`, hooks, testes |

Estado: **segurada**. O commit `36b20e7` (tornar o `#id` opcional) está
descartado — trata a sintaxe, não o acoplamento. A abordagem definitiva aguarda
confirmação do Brito. A branch `319-validacoes-independentes` fica no
repositório, não se integra.

### 2.3 P1 — hooks que não entregam o que prometem

Origem: parecer de QA do Dave sobre `dev 815363a` (`1.26.0a18`), mensagem
`603000fd`. Não têm issue; ficam como reserva.

| # | Reserva |
|---|---|
| 4 | `check-len-first-line` mente no erro: roda com `--max-first-line=256` e falha dizendo `(min: 10 and max: 50)`; `check_max_len_first_line_commit_msg` faz `max(50, len_line)` e ignora qualquer máximo menor |
| 5 | `dev` e `tags` desprotegidos: `is-valid-branchname` com `args: []` e `no-commit-to-branch` no default; commit em `dev` dá exit 0 |
| 6 | hooks inertes por configuração: `check-type-commit-msg` e `set-issue-from-branch-cli` com `-N` (`--nonexequi`) |
| 7 | seis hooks publicados sem uso neste repositório: `check-manual-version`, `check-manual-changelog`, `check-type-from-status`, `set-type-from-status`, `check-precommit-installed`, `set-issue-from-branch` |
| 8 | `detect-key` público com `types` em AND (só `.py`); o contrato publicado é mais restrito que a config local; o `exclude` esconde o próprio módulo do scanner |
| 9 | `insert-diff-commit`: manifesto e docs dizem `prepare-commit-msg`, a config usa `commit-msg`; injeta o diff inteiro na mensagem |
| 10 | bug de código: `check_valid_branchname_cli` lê `ctx.params.get('commit_msg_file ')` com espaço e instancia `click.ClickException` sem `raise` |
| 11 | `check_type_commit_msg` estoura `IsADirectoryError` quando chamado sem arquivo |

Ressalva do Dave: 8, 10 e 11 são diagnóstico de contrato e de código do pacote,
não só de configuração; se a reserva for homogénea, vale separar «corrigir
hook» de «corrigir contrato publicado».

### 2.4 P1 — melhorias de teste

O buraco é o `.pre-commit-config.yaml`: 31 arquivos e ~190 testes não abrem a
config, e ela apodreceu sem sinal.

| # | Melhoria |
|---|---|
| a | contrato do config: todo `id` declarado existe no repositório; todo hook local tem entry-point em `[project.scripts]` |
| b | paridade config x `.pre-commit-hooks.yaml` para os 18 ids (`stages`, `pass_filenames`, `always_run`, `types`) |
| c | lista explícita de hooks publicados e não usados, com justificativa |
| d | assert de que nenhum hook local recebe `-N` por padrão |
| e | texto de erro do `check-len-first-line` refletindo os parâmetros reais |
| f | `is-valid-branchname` com os args do config contra `dev` e `tags`, esperando falha |
| g | E2E com git temporário: YAML/JSON com chave privada, commit simulado, rejeição |
| h | job de CI com `pre-commit run --all-files` (ubuntu, git recente) |

## 3. Decisões

- O `pre-commit` fica pinado em `4.6.0`, idêntico em `.pre-commit-config.yaml`
  (`minimum_pre_commit_version`) e em `pyproject.toml`. A `4.6.1` passou a
  usar `git ls-files --deduplicate` (git >= 2.31); com git 2.29.2 isso
  responde `unknown option` (exit 129).
- O hook `mypy` sai do bloco do `ruff-pre-commit` para bloco próprio, com
  versão pinada.
- As validações de mensagem seguem para hooks distintos; o `#id` opcional
  fica descartado.
- P0-3 e as reservas P1 não viram issue nesta sprint.

## 4. Pendências e reservas

| Assunto | Estado | Tratamento |
|---|---|---|
| #319 | redesenhada, segurada | aguarda confirmação da abordagem pelo Brito |
| `319-validacoes-independentes` | commit `36b20e7` descartado | branch fica no repositório, não se integra |
| P0-3 | sem issue | gates decorativos; reserva |
| P1 (4–11) | sem issue | hooks que não entregam o que prometem |
| P1 (a–h) | sem issue | melhorias de teste do `.pre-commit-config.yaml` |
| `deprecated 3.0.1` | dependência | marcador `python_full_version >= '3.12'`; o Brito decide se sobe `requires-python` |

## 5. Fora de escopo

- Subir o `requires-python` para `>=3.12`.
- Corrigir as reservas P1 (não são issues nesta sprint).
- Reescrever código fora do necessário para as tarefas.
