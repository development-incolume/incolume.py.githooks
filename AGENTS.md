# AGENTS.md — regras do projeto

Regras para qualquer agente, pessoa ou IDE que trabalhe neste repositório.
Valem sobre preferências locais.

## Antes de qualquer ação

Este arquivo é lido antes de agir, não depois. O checklist mínimo:

1. Li este arquivo por inteiro nesta sessão; se ele mudou, reli.
2. Sei qual issue/tarefa estou atendendo e qual é o teste que prova isso.
3. Sei em qual branch e worktree estou; branch de tarefa deriva de `dev`.
4. A identidade local do worktree é `<nome do agente> <dev@incolume.com.br>`.
5. Nenhuma dependência nova entra sem aprovação explícita do usuário.
6. A mudança respeita o escopo da tarefa; tarefa vizinha não se antecipa.

Faltando qualquer item, pare e resolva antes de editar arquivo, rodar comando
que muda estado, commitar ou abrir PR.

## Fonte de verdade

- `README.md`: modelo de `.pre-commit-config.yaml` publicado para os projetos
  consumidores (a revisão citada ali deve refletir a tag publicada).
- `.pre-commit-hooks.yaml`: contrato público dos hooks; mudança de nome, id ou
  argumento é quebra de API e exige cuidado com semver.
- Divergência entre código e documento: o documento ganha; corrija o código ou
  proponha a mudança do documento, nunca silencie a diferença.

## Escopo

- Este repositório é a fonte dos hooks git do time incolume; ele não consome
  decisões de outros projetos, ele as fornece.
- Um hook = um módulo em `incolume/py/githooks/` + comando Click em
  `incolume/py/githooks/cli/cli.py` + entry-point em `[project.scripts]`.
- Toda mudança de hook visível precisa refletir em `.pre-commit-hooks.yaml`,
  `README.md` (modelo) e `examples/` quando aplicável.

## Agentes de IA

- Agente de IA segue todas as regras deste arquivo como qualquer colaborador.
- Pode fazer sozinho, dentro do escopo da issue: escrever/alterar teste, editar
  código e documento, rodar `pytest`, `ruff` e `mypy`.
- Exige decisão humana: aprovar dependência nova, abrir PR, bump de versão
  (`uv version`), merge em `dev`/`main` e fechar issue.
- O agente implementador não mergeia o próprio trabalho; o merge em `dev` é
  **local, feito pelo integrador com aprovação explícita do responsável**;
  sem essa aprovação, o agente para no commit.
- PR não existe para `dev`; existe **somente para `main`, no fechamento da
  release** (`dev` → `main`), com testes verdes e revisão.
- Configurações específicas de cada ferramenta (ex.: Copilot) referenciam este
  arquivo; regras não se duplicam.

## Estrutura

- Pacote: `incolume/py/githooks/`; `core/` para utils, rules, decorators.
- Não mova o pacote para `src/`; o build usa `uv_build` com `module-root = ""`.
- CLI segue o padrão do grupo `githooks-cli` (chain group, `click`), com
  `-N/--nonexequi` e `-V/--version` em todos os comandos.
- Worktrees vivem em `wt/`; builds em `dist/`.

## Toolchain

- Python `>=3.10,<4`; desenvolvimento no interpretador mais novo disponível.
  - Exceção documentada: quando o `uv run` falhar em build nativo (ex.:
    `pyyaml` no 3.15, sem wheel e sem MSVC), execute com o interpretador
    estável: `uv run -p 3.10 <comando>`.
- `uv` para ambiente e dependências: `uv sync --all-packages --all-extras
  --all-groups --locked`.
- Testes: `pytest` com `.pytest.toml` (doctest-modules, strict-markers,
  cobertura obrigatória).

  ```sh
  uv run pytest -m 'not noci' --maxfail=1 --disable-warnings -q
  ```

- Qualidade: `uv run ruff check incolume/ tests/` e
  `uv run ruff format --check incolume/ tests/`. Nenhum outro linter.
- Tipos: `uv run mypy incolume/ tests/` (strict). No CI é
  `continue-on-error`; localmente, trate erro novo como erro.
- Line-length 79 (`.ruff.toml`); aspas simples; target py311.

## Testes

- Cobertura mínima real: `fail_under = 99.7` em `.coveragerc.toml`. Código novo
  sem teste que o cobre não entra.
- Nomes: arquivos `*_test.py` espelhando a estrutura do pacote, classes
  `TestCase*`, funções `test_*`.
- Markers: `fasttest`, `noci`, `slow`, `webtest`. Teste que não roda no CI usa
  `noci` com justificativa.
- Mudança de comportamento entra com teste; correção de bug entra com teste que
  reproduz o bug antes do fix.
- Teste nunca é alterado para a implementação passar. Correção de teste
  defeituoso é commit separado, com justificativa.

## Dependências

- Nenhuma biblioteca é instalada sem aprovação explícita do usuário.
- A aprovação é por biblioteca e fica registrada no PR ou na conversa.
- `uv add` só depois do "aprovado"; o `uv.lock` só muda quando uma dependência
  aprovada entra ou sai, em commit `build(deps): ...`.

## Identidade e autoria

Todo commit tem autor nominal. Nenhum agente commita como anônimo nem com a
identidade de outra pessoa.

- Formato: `<nome do agente> <dev@incolume.com.br>`.
- `user.email` é sempre `dev@incolume.com.br`.
- A identidade é local do worktree, definida antes do primeiro commit; não se
  altera a configuração global da máquina nem a do clone principal.
- Par de programação: o commit leva o nome de quem conduziu a tarefa; o outro
  aparece no corpo como `Co-authored-by: <nome> <dev@incolume.com.br>`.

## Git e entrega

- **Toda alteração tem uma issue** aberta antes do trabalho começar, e a issue
  é encerrada quando a demanda termina. Sem issue, não há branch nem commit.
- Branch de tarefa: `<id>-<slug>`, derivada de `dev`
  (ex.: `332-aplicar-contexto-click`).
- `dev` é a branch de integração; `main` só recebe release estável.
- O merge é `git merge --no-ff`: a branch entra com seus commits e um commit de
  merge explícito. Nunca fast-forward, nunca squash.
- O merge parte sempre do **HEAD de `dev`**; se necessário, `git rebase dev` na
  branch antes do merge. Conflito se resolve no rebase, nunca no commit de
  merge.
- Rebase diário em `dev`; PR com mais de 1 dia sem rebase não entra.
- PR (somente `main`, no fechamento da release) só entra com testes verdes e
  revisão do responsável.
- Remova o worktree após o merge e rode `git worktree prune`.

## Versionamento

Semver. A versão vive em `pyproject.toml` e só muda por `uv version`, nunca à
mão.

- **Cada tarefa concluída em `dev`:** bump de alpha incrementa o alpha
  (`1.20.0a1` → `a2` → `a3`…).
  - Saindo de versão **estável** (ex.: `1.20.0`), `--bump alpha` sozinho
    falha ("didn't increase the version"); combine componente de release
    + alpha: `uv version --bump patch --bump alpha` ou
    `uv version --bump minor --bump alpha`.
- **Fim de ciclo:** `uv version --bump rc` / `--bump stable` promove a versão.
- **O commit de versão fica sempre em `dev`, nunca na branch da tarefa:**

  ```sh
  git ci -m "build: incolume-py-githooks $(uv version --short)"
  ```

- `patch` para correção, `minor` para funcionalidade, `major` para quebra.
- **`CHANGELOG.md` é gerado** por `incolume-py-changelog` a partir das anotações
  das tags (`git tag -n`); nunca é escrito à mão.

## Commits

Commit atômico em
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/),
no padrão do histórico deste repo:

```
<tipo>(escopo-opcional): #<id> <descrição>

[corpo: motivação, evidência de teste]

Refs: #<id>   |   Closes #<id>
```

- Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
  `ci`, `chore`, `revert`.
- Descrição em minúscula, imperativa, sem ponto final.
- Todo commit que **conclui** uma issue leva o rodapé `Closes #<id>`; commits
  intermediários usam `Refs: #<id>` (ou `#<id>` na descrição).
- `chore:`, `docs:` e `refactor:` não fecham issue.
- Dependência aprovada entra como `build(deps): adiciona <lib>`.
- O próprio repo valida a mensagem: os hooks `check-type-commit-msg`,
  `check-len-first-line` e `validate-message-commit` rodam no prepare-commit;
  se o hook reprovar, corrija a mensagem, não contorne o hook.
- `main` e `dev` não recebem commit direto (`no-commit-to-branch`).

## Segurança

- `detect-key` existe para impedir segredo versionado; nunca desative hook de
  segurança para destravar um commit.
- Nenhum segredo no código, no teste, no log ou no fixture.
- Exemplos em `examples/` são didáticos: sem credenciais reais, nunca.

## Documentação

- Docstrings em todos os módulos novos; `--doctest-modules` executa exemplos
  como teste, então exemplo de docstring precisa funcionar.
- Mudança de uso de hook atualiza `README.md` e `CHANGELOG.md` (gerado).
- Não invente número, prazo ou fonte; dado ausente é pendência explícita.
