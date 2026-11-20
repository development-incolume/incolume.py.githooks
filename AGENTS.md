# AGENTS.md — regras do projeto

Regras para qualquer agente, pessoa ou IDE que trabalhe neste repositório.
Valem sobre preferências locais.

## Antes de qualquer ação

Este arquivo é lido antes de agir, não depois. O checklist mínimo:

1. Li este arquivo por inteiro nesta sessão; se ele mudou, reli.
2. Sei qual issue/tarefa estou atendendo e qual é o teste que prova isso.
3. Sei em qual branch e worktree estou; branch de tarefa deriva de `dev`.
4. A identidade local do worktree é `Britodfbr <brito@incolume.com.br>` (o `Author:`); o agente entra como `Co-authored-by`.
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
  release**, com testes verdes e revisão.
- **Ordem de fechamento da release: `dev` → `tags` → `main`.**
  1. Trabalho concluído em `dev` (commits + bumps de alpha).
  2. `dev` entra na branch **`tags`** por `merge --no-ff` (a partir do HEAD de
     `dev`); a versão estável é definida **na `tags`**
     (`uv version --bump stable`) com o commit `build:` também lá.
  3. Tag anotada criada **na branch `tags`**, apontando para o commit de
     versão; mensagem em linha única, com seções `added:`/`changed:`/`fixed:`
     (o gerador de CHANGELOG lê a anotação linha a linha).
  4. Por fim, `main` recebe `tags` (PR), já contendo a versão e a tag.
  5. Documentação de fecho: antes de criar a tag, atualizar
     - a «Versão do projeto» em `docs/analysis_artifacts/`;
     - o `rev:` do hook em `README.md` e nos yaml de configuração
       (`.pre-commit-config.yaml`, `.pre-commit-hooks.yaml`);
     - as referências de versão em `mkdocs.yml`.
- **Procedimentos verificados no fechamento da `1.21.0`** (rito `dev` → `tags`
  → `main`):
  - Antes de publicar, conferir ancestralidade: `git merge-base --is-ancestor`
    de `origin/dev` no tip de `dev` e de `origin/tags` no tip de `tags` — só
    push fast-forward, sem reescrever o que já está no remoto.
  - Ordem de publicação: push de `dev`, push de `tags`, depois a tag anotada;
    se a tag antiga já estiver no remoto apontando para outro commit,
    `git push -f origin <tag>` **e conferir** com `git ls-remote origin`.
  - O `CHANGELOG.md` é regenerado **na branch `dev`** durante o fechamento da
    release: `uv run gcl CHANGELOG.md`, seguido de commit `docs:` (ou incluso
    no commit `build:` da versão), **antes** do merge `dev` → `tags`; a `tags`
    recebe o changelog pelo merge, a partir das anotações das tags já
    existentes.
  - PR é **de `tags` para `main`**; CI verde antes do merge; `main` termina
    contendo a versão estável, a tag e o changelog.
  - Durante o fechamento, `dev` **não recebe** novos commits de tarefa; o
    próximo ciclo reabre com `uv version --bump minor --bump alpha` em `dev`
    (funcionalidade nova) — `patch --bump alpha` somente se a sprint trouxe
    apenas correção de bugs/fix/bugfix.
- Configurações específicas de cada ferramenta (ex.: Copilot) referenciam este
  arquivo; regras não se duplicam.

## Estrutura

- Pacote: `incolume/py/githooks/`; `core/` para utils, rules, decorators.
- Não mova o pacote para `src/`; o build usa `uv_build` com `module-root = ""`.
- CLI segue o padrão do grupo `githooks-cli` (chain group, `click`), com
  `-N/--nonexequi` e `-V/--version` em todos os comandos.
- Worktrees vivem em `wt/`; builds em `dist/`.

## Toolchain

- Python `>=3.11,<4`; desenvolvimento no interpretador mais novo disponível.
  - Exceção documentada: quando o `uv run` falhar em build nativo (ex.:
    `pyyaml` no 3.15, sem wheel e sem MSVC), execute com o interpretador
    estável: `uv run -p 3.11 <comando>`.
- `uv` para ambiente e dependências: `uv sync --all-packages --all-extras
  --all-groups --locked`.
- Testes: `pytest` com `.pytest.toml` (doctest-modules, strict-markers,
  cobertura obrigatória).

  ```sh
  uv run pytest -m 'not noci' --maxfail=1 --disable-warnings -q
  ```

- Antes de commitar, com `d='tests/ incolume/'`:
  `ruff check --fix $d`, `ruff format $d`, `mypy $d`, `ty check $d`,
  `pytest -vvv $d`.
- Cobertura mínima de 99.99% (`.coveragerc.toml`).
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

Todo commit tem autor nominal. O `Author:` é o **Brito**
(`Britodfbr <brito@incolume.com.br>`), a identidade global da máquina, resetada
no worktree antes de commitar; o agente que executou é creditado como coautor.

- `Author:` fixo: `Britodfbr <brito@incolume.com.br>`.
- `Co-authored-by: OpenBot <335604065+openbotgit[bot]@users.noreply.github.com>`
  em todo commit de agente OpenBot.
- `Co-authored-by: <nome do agente> <dev@incolume.com.br>` com o agente que
  executou (ou o par de programação).
- A identidade é local do worktree, resetada antes do primeiro commit
  (`git config user.name "Britodfbr"`,
  `git config user.email "brito@incolume.com.br"`); não se altera a configuração
  global da máquina nem a do clone principal.
- Documento de análise usa `Autor: Brito (Britodfbr)` e o agente como coautor.

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
- PR (somente `main`, no fechamento da release, **após a tag na branch
  `tags`**) só entra com testes verdes e revisão do responsável.
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
- **O commit de versão fechando release fica na branch `tags`, nunca na branch
  da tarefa; bumps intermediários (alpha/rc) ficam em `dev`:**

  ```sh
  git ci -m "build: incolume-py-githooks $(uv version --short)"
  ```

- `patch` para **correção de bugs/fix/bugfix apenas**; `minor` para
  funcionalidade nova; `major` para quebra. O componente do próximo ciclo é
  escolhido pelo conteúdo da sprint, nunca por conveniência da ferramenta.
- **`CHANGELOG.md` é gerado** por `incolume-py-changelog` a partir das anotações
  das tags (`git tag -n`); nunca é escrito à mão. A mensagem da tag é
  **linha única** — o gerador trunca mensagens multilinha.

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
- O rodapé `Closes #<id>` é obrigatório mesmo em `docs:`, `chore:` e
  `refactor:` quando o commit conclui a issue; nunca feche issue à mão.
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
