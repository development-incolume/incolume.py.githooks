# ADR-001 — Decisões de arquitetura do incolume.py.githooks

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.25.0a4
- **Status:** Proposta (aguardando revisão)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

Este ADR regista as decisões de arquitetura do repositório. Cada decisão
traz contexto, alternativas consideradas, consequências e estado.

## D1 — Um hook é um módulo + comando Click + entry-point

**Contexto.** Os hooks precisam ser descobríveis pelo `pre-commit` e também
executáveis pelo desenvolvedor na linha de comando.

**Decisão.** Cada hook vive em um módulo de `incolume/py/githooks/`, expõe um
comando Click em `incolume/py/githooks/cli/cli.py` e um entry-point em
`[project.scripts]`.

**Alternativas.** Script standalone por hook (duplica CLI e testes); hook
genérico parametrizado (esconde a intenção e complica o contrato).

**Consequências.** Superfície previsível, teste por módulo e CLI único; o
pre-commit consome os entry-points publicados.

**Estado:** Aceita.

## D2 — Contrato público em `.pre-commit-hooks.yaml`

**Contexto.** Os consumidores copiam o modelo do `README.md`; a fonte de
verdade precisa ser única.

**Decisão.** `.pre-commit-hooks.yaml` é o contrato; declara `id`, `entry`,
`language: python`, `stages`, `pass_filenames` e
`additional_dependencies: [click, icecream]`.

**Alternativas.** Contrato gerado em tempo de build (fragiliza o consumidor);
`language: system` (acopla ao ambiente do usuário).

**Consequências.** Quebra de nome, id ou argumento é quebra de API e exige
semver; o ambiente do hook é isolado pelo pre-commit.

**Estado:** Aceita.

## D3 — CLI em grupo chain `githooks-cli`

**Contexto.** São muitos comandos; é preciso agrupá-los sem perder o uso
individual.

**Decisão.** Grupo chain `githooks-cli` agrega todos os comandos; cada um
também é entry-point próprio. `-N/--nonexequi` e `-V/--version` são
transversais.

**Alternativas.** CLI por hook separado (fragmenta a experiência); grupo não
chain (exige comando intermediário).

**Consequências.** `-N` permite desativar qualquer hook sem remover a
configuração; `-V` expõe a versão do pacote.

**Estado:** Aceita.

## D4 — Distribuição com `uv_build`, sem `src/`

**Contexto.** O pacote precisa ser importável como `incolume.py.githooks`.

**Decisão.** Build com `uv_build`, `module-root = ""` e
`module-name = "incolume.py.githooks"`; o pacote não vai para `src/`.

**Alternativas.** Layout `src/` (exige configuração extra de path); backend
setuptools (mais incógnitas de build).

**Consequências.** Import direto e previsível; `uv sync` resolve o pacote
local.

**Estado:** Aceita.

## D5 — Semver e rito `dev` → `tags` → `main`

**Contexto.** O contrato público muda e precisa de versionamento previsível.

**Decisão.** Semver; versão só muda por `uv version`. Fluxo: trabalho em
`dev` (com bumps de alpha), `dev` entra em `tags` por `merge --no-ff`, a
versão estável é definida na `tags` e a tag anotada é criada lá; `main`
recebe `tags` por PR no fechamento da release.

**Alternativas.** Commit direto em `main` (sem revisão); squash (perde o
histórico de merge); fast-forward (não registra a integração).

**Consequências.** Histórico explícito, release revisada e versão rastreável.

**Estado:** Aceita.

## D6 — QA como gate obrigatório

**Contexto.** O repositório é fonte de regras para outros projetos; erro aqui
se propaga.

**Decisão.**Antes de cada commit: `ruff check`, `ruff format`, `mypy` e
`pytest`; cobertura mínima de 99.99%.

**Alternativas.** QA só no CI (feedback tardio); gate apenas por hook
(documentário, fácil de contornar).

**Consequências.** Feedback rápido e release com cobertura 100%.

**Estado:** Aceita.

## D7 — Documentação: site mkdocs + artefactos excluídos

**Contexto.** Decisões e requisitos precisam ser consultáveis, mas não devem
virar página pública do site.

**Decisão.** Site mkdocs para uso (instalação, hooks, CLI, API, regras);
`docs/analysis_artifacts/` para PRD/ADR/SPEC/PLAN, excluída do site via
`exclude_docs` no `mkdocs.yml` e fora da `nav`.

**Alternativas.** Publicar tudo no site (expõe planejamento interno); só o
histórico de commits (não consultável).

**Consequências.** Artefatos versionados e consultáveis no repositório, sem
poluir o site.

**Estado:** Aceita.
