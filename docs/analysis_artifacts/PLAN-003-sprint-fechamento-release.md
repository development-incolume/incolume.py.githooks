# PLAN-003 — Sprint de fechamento de release do incolume.py.githooks

- **Data:** 2026-11-20
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.26.0
- **Status:** Em execução (2026-11-20)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

Escopo exclusivo do `incolume.py.githooks`; não se aplica a outro projeto.

## 1. Objetivo

Higiene de fecho da release `1.26.0`: alinhar a documentação e as
dependências ao estado publicado e registar o rito para as próximas
releases.

## 2. Tarefas da sprint

| Issue | Tarefa | Artefacto |
|---|---|---|
| #421 | «Versão do projeto» dos artefactos para `1.26.0` | `docs/analysis_artifacts/` |
| #422 | `rev: 1.26.0` no exemplo do hook | `README.md`, `docs/instalacao.md` |
| #423 | passo de documentação no fecho de release | `AGENTS.md` |
| #418 | renomear `.github/copilot-instructions.md` | `.github/instructions.md`, `README.md` |
| #420 | atualizar as dependências do projeto | `pyproject.toml`, `uv.lock` |
| #319 | validações de mensagem independentes | `core/rules.py`, testes |

## 3. Decisões

- A «Versão do projeto» dos artefactos passa a refletir a release
  fechada (`1.26.0`), não a alpha de `dev`.
- O `rev:` do exemplo do hook acompanha a tag publicada.
- O fecho de release passa a incluir a documentação (artefactos, `rev:`
  e `mkdocs.yml`).
- As validações de mensagem passam a aceitar mensagem sem `#id`, de modo
  autónomo.

## 4. Pendências e reservas

| Assunto | Estado | Tratamento |
|---|---|---|
| `#256` | fechada (duplicada de `#257`) | fora do escopo |
| `#175` | fechada | fora do escopo |
| `deprecated`, `incolume-py-changelog`, `pytest-click` | dependências | última versão exige Python >=3.11/3.12; manter enquanto o projeto suportar 3.10 |

## 5. Fora de escopo

- Largar o suporte a Python 3.10.
- Reescrever código fora do necessário para as tarefas.
