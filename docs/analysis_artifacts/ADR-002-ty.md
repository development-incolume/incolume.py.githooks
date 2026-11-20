# ADR-002 — ty em paralelo ao mypy

- **Data:** 2026-11-19
- **Projeto:** incolume.py.githooks
- **Versão do projeto:** 1.27.0
- **Status:** Aprovado (2026-11-19)
- **Autor:** Brito (Britodfbr)
- **Coautor:** Otto OpenBot

## Contexto

O `mypy` é o verificador de tipos do projeto, com configuração em
`.mypy.ini`. O `ty` (Astral) é mais rápido, mas ainda beta (`0.0.x`) e com
semântica própria; ele não reproduz 1:1 o modo estrito do `mypy`.

## Decisão

Adotar o `ty` em paralelo ao `mypy`: `ty>=0.0.107` no grupo `dev`,
configuração em `ty.toml` (só o equivalente), passo informativo no CI
(`continue-on-error: true`) e hook em `stages: [manual]` no pre-commit. A
substituição futura do `mypy` pelo `ty` fica registrada na tag `Unreleased`.

## Alternativas consideradas

- Substituir o `mypy` pelo `ty` já nesta sprint: descartado, pois os 158
  diagnósticos atuais e as diferenças de semântica ainda não foram tratados.
- Não adotar o `ty`: descartado, pois o ganho de velocidade e a
  convergência com o ecossistema Astral são desejados.
- Ativar o `ty` bloqueante no CI/pre-commit: descartado na adoção, para não
  impedir commits até a substituição.

## Consequências

- Duas checagens de tipo no QA, com o `ty` informativo.
- Os diagnósticos do `ty` são dívida técnica a tratar na substituição.
- A tag `Unreleased` passa a registrar a substituição futura.

## Estado

Aceita (em adoção).
