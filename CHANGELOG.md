# CHANGELOG


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Conventional Commit](https://www.conventionalcommits.org/pt-br/v1.0.0/).

This file was automatically generated for [incolume.py.changelog](https://github.com/development-incolume/incolume.py.changelog/tree/1.3.0)

---


## [Unreleased]	 &#8212; 	2026-10-19:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.11 conformeStatus of Python versions (https://devguide.python.org/versions/#versions);
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-%203.11%20|%203.12%20|%203.13%20|%203.14%20|%203.15-%2332CD32?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.23.0]	 &#8212; 	2026-11-13:
### Added
  - Hook check-manual-version para detectar edicao manual de versao no pyproject.toml;
  - Hook check-manual-changelog para detectar edicao manual do CHANGELOG.md;
  - Hook set-type-from-status para injetar o tipo de commit deduzido do git status;
  - Hook check-type-from-status para bloquear divergencia objetiva de tipo;
  - Gates AST de docstrings Google no src e nos testes;
  - Pyyaml como dependencia de teste.;
### Changed
  - Docstrings de src e testes padronizadas em Google;
  - Documentacao alinhada (mkdocs api, descriptions dos hooks, README).;
### Fixed
  - Redefinicao de tomli no core/__main__.py (mypy no-redef);
  - Validate-message-commit unificado em commit-msg.;

## [1.22.1]	 &#8212; 	2026-11-12:
### Fixed
  - Ruff format aplicado nos arquivos do hook check-commit-footer;
  - Mypy acrescentado ao pre-commit e regras de validacao obrigatorias (ruff check, ruff format, mypy) antes do commit no AGENTS.md (#373).;

## [1.22.0]	 &#8212; 	2026-11-12:
### Added
  - Hook check-commit-footer para validar rodapes de commit (Closes/Refs/Signed-off-by/Co-authored-by/Reviewed-by/Acked-by);
  - Id ativo no .pre-commit-config.yaml local.;
### Changed
  - Sincronizacao do contrato .pre-commit-hooks.yaml e README com os 13 hooks;
  - Documentacao no site mkdocs (hooks, cli, api).;
### Fixed
  - Version.txt dessincronizado do pyproject.toml.;

## [1.21.0]	 &#8212; 	2026-11-12:
### Added
  - Site de documentacao proprio do projeto, com guia de instalacao, uso dos hooks, referencia das ferramentas e regras do projeto, publicado em development-incolume.github.io/incolume.py.githooks;
### Changed
  - Apresentacao do pacote atualizada para deixar claro que ele e um plugin de pre-commit (hooks git prontos para proteger e padronizar os repositorios incolume);
  - Identidade visual oficial do projeto aplicada ao site (logo e favicon);
  - Regras de contribuicao, incluindo como agentes de IA devem trabalhar no repositorio, organizadas e publicadas;
  - Informacoes do pacote (descricao e links) apontando para o site da documentacao.;

## [1.20.0]	 &#8212; 	2026-11-07:
### Changed
  - FatoraÃ§Ã£o performÃ¡tica em diversos trechos de cÃ³digo;
  - Fatorado too-many-arguments (PLR0913) nos scripts CLI;
  - Melhoria de exibiÃ§Ã£o feedback para CLI;

## [1.20.0rc1]	 &#8212; 	2026-10-21:
### Changed
  - FatoraÃ§Ã£o performÃ¡tica em diversos trechos de cÃ³digo;

## [1.19.0]	 &#8212; 	2026-10-19:
### Changed
  - Mapeado hooks desaparecidos;
  - Mapeamento para hooks effort-random-message;
  - CLI `is-valid-msg-commit` argumentos extras inexperados;
  - Corrigido erro IndexError/ValueError para entrada do script;
  - Corrigido dependÃªncias para hooks remotos;
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.11 conformeStatus of Python versions (https://devguide.python.org/versions/#versions);
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-%203.11%20|%203.12%20|%203.13%20|%203.14%20|%203.15-%2332CD32?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);
### Added
  - Acrescentado modo verboso ao script `githook-cli`;

## [1.18.5]	 &#8212; 	2026-10-12:
### Changed
  - Corrigido dependÃªncias para hooks remotos;

## [1.18.4]	 &#8212; 	2026-10-09:
### Changed
  - Corrigido erro IndexError/ValueError para entrada do script;

## [1.18.3]	 &#8212; 	2026-10-08:
### Changed
  - Is-valid-msg-commit argumentos extras inexperados;

## [1.18.2]	 &#8212; 	2026-10-07:
### Changed
  - Mapeamento para hooks effort-random-message;

## [1.18.1]	 &#8212; 	2026-10-07:
### Changed
  - Mapeado hooks desaparecidos;

## [1.18.0]	 &#8212; 	2026-10-07:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Added
  - Adicionado hook `effort-random-msg`;
  - Adicionado suporte parcial a Python 3.15;
### Changed
  - Cobertura de cÃ³digo com testes ampliada a 100%;
### Removed
  - Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-%203.11%20|%203.12%20|%203.13%20|%203.14%20|%203.15-%2332CD32?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.17.0]	 &#8212; 	2026-10-01:
### Added
  - Adicionado suporte completo a Python 3.14;
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Changed
  - Migrado totalmente em todos os hooks `argparse` para `click`;
### Removed
  - Pacote argparse retirados dos script principais;
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-%2332CD32?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.16.0]	 &#8212; 	2026-09-28:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Added
  - Novo hook implementado: effort-ramdon-msg-cli;
### Changed
  - Mensagem para nonexequi acrescentada em todos os hooks;
  - MigraÃ§Ã£o para CLICK em andamento;
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-%2332CD32?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.15.0]	 &#8212; 	2026-09-25:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Added
  - Novo mÃ³dulo utils;
  - Adicionado gadgets de versÃ£o segura de python;
  - Adicionado gadget de validaÃ§Ã£o dos testes unitÃ¡rios;
### Changed
  - FunÃ§Ãµes comuns centralizadas no modulo utils;
### Security
  - [![Python Version: -](https://img.shields.io/badge/%20Python%20Version-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-%23006400?style=flat&labelColor=4444444)](https://devguide.python.org/versions/#versions);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.14.0]	 &#8212; 	2026-09-24:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Added
  - Compatibilidade com Python 3.14;
### Changed
  - Implementado mensagem nonexequi: check_len_first_line_commit_msg_cli;
  - Implementado mensagem nonexequi: check_valid_branchname_cli;
  - Implementado mensagem nonexequi: footer_signedoffby_cli;
  - Implementado mensagem nonexequi: clean_commit_msg_cli;
  - Implementado mensagem nonexequi: set_issue_from_branch_cli;
  - Migrado argparse para click: check_len_first_line_commit_msg_cli;
  - Migrado argparse para click: check_valid_branchname_cli;
  - Migrar argparse para click: footer_signedoffby_cli;
  - Migrado argparse para click: clean_commit_msg_cli;
  - Migrado argparse para click: set_issue_from_branch_cli;
### Security
  - ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolume.py.githooks?color=00FFFF);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.13.0]	 &#8212; 	2026-09-22:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Changed
  - Atualizado pyproject.toml com diretivas gui-script, all, cli, keywords, e lincese-files;
  - Reativado hook check-len-first-line;
  - Reativado hook check-valid-filenames;
  - Reativado hook footer-signed-off-by;
  - Configurado CLI com opÃ§Ã£o de help (-h, --help), versÃ£o (-V --version) e nonexequi (-N, --nonexequi);
### Security
  - ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolume.py.githooks?color=00FFFF);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.12.0]	 &#8212; 	2026-09-16:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Added
  - Criado submodulo para CLI;
### Changed
  - Atualizado `coverage` para aceitar configuraÃ§Ã£o via TOML;
  - Hook desativado: check-precommit-installed;
  - Arquivo de configuraÃ§Ã£o mypy alterado;
  - Arquivo de configuraÃ§Ã£o do ruff alterado;
### Security
  - ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolume.py.githooks?color=00FFFF);
  - [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit);

## [1.11.0]	 &#8212; 	2026-09-04:
### Deprecated
  - SerÃ¡ Descontinuado suporte a Python 3.10 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
  - SerÃ¡ Descontinuado suporte a Python 3.11 conforme Status of Python versions (https://devguide.python.org/versions/#versions);
### Changed
  - Atualizado `pytest` para aceitar configuraÃ§Ã£o via TOML;
  - Migrado configuraÃ§Ã£o pytest.ini -> pytest.toml;
  - Ajustes de execuÃ§Ã£o em CI/CD;
### Security
  - ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolume.py.changelog?color=00FFFF);

## [1.10.0]	 &#8212; 	2026-09-01:
### Added
  - Adicionado decorador para registro rÃ¡pido de logging;
  - Adicionado mypy para validaÃ§Ã£o de tipo;
### Changed
  - Ampliado cobertura de cÃ³digo;
  - Atualizado pacotes excenciais do projeto;
  - Aplicado design partner policy para validaÃ§Ã£o de nomes de arquivos;
### Deprecated
  - Modulo ValidateFilename em conflito tornado obsoleto;
  - Pacote rich serÃ¡ descontinuado no projeto;

## [1.9.0]	 &#8212; 	2025-11-19:
### Added
  - Adicionado ativos de logo, em formato PNG, XCF e AF;
  - Registro rÃ¡pido de logging via decoradores;
  - Logging de eventos detalhados com variÃ¡veis de ambiente do Sistema Operacional;
  - Modo verboso ativado com variÃ¡veis do sistema operacional;
  - Criado modulo `core` com as funcionalidades centrais do pacote;
  - Rules.Status(Enum);
  - Rules.ProtectedBranchName(Enum);
  - Parametro `--nonexequi` para inativar qualquer hook do projeto;
### Changed
  - Melhoria no help CLI;
### Removed
  - Modulo `utils` substituÃ­do pelo modulo `core`;

## [1.8.0]	 &#8212; 	2025-10-20:
### Added
  - Disponibilizado hook check-valid-branchname;

## [1.7.0]	 &#8212; 	2025-10-06:
### Added
  - Disponibilizado hook clean-commit-message;

## [1.6.0]	 &#8212; 	2025-10-05:
### Added
  - Disponibilizado hook check-len-first-line;
### Changed
  - Acrescentado modelo de configuraÃ§Ã£o dos hooks ao README.md;

## [1.5.0]	 &#8212; 	2025-10-04:
### Added
  - Disponibilizado hook insert-diff-commit;

## [1.4.0]	 &#8212; 	2025-10-03:
### Added
  - Disponibilizado hook footer-signed-off-by;
### Changed
  - AlteraÃ§Ã£o no modo verboso;
  - Atualizado README.md;

## [1.4.0rc2]	 &#8212; 	2025-10-03:
### Changed
  - AlteraÃ§Ã£o no modo verboso;

## [1.4.0rc1]	 &#8212; 	2025-10-03:
### Added
  - Disponibilizado hook footer-signed-off-by;

## [1.3.0]	 &#8212; 	2025-10-02:
### Added
  - Hook check-precommit-installed reativado;

## [1.2.0]	 &#8212; 	2025-10-01:
### Added
  - Disponibilizado hook effort-message;
### Changed
  - Interfaces para hooks centralizadas no mÃ³dulo CLI;
### Removed
  - Modulo incolume.py.githooks.pre_commit_installed removido;

## [1.1.0]	 &#8212; 	2025-09-28:
### Added
  - Hook `detect-key` disponibilizado;
### Changed
  - Cobertura total do cÃ³digo implementado;
  - Chamada de hooks com argumentos configurÃ¡veis atravÃ©s do arquivo yaml;

## [1.0.0]	 &#8212; 	2025-09-26:
### Added
  - Hook check-max-len-first-line-commit-msg;
  - Hook check-min-len-first-line-commit-msg;
  - Hook footer-signed-off-by;
  - Hook clean-commit-message;
  - Hook git-diff;
  - LanÃ§amento da release 1.0.0 com apenas 1 hook: check-valid-filenames;
### Changed
  - AmplicaÃ§Ã£o da cobertura para 99% do cÃ³digo;
### Removed
  - Hook check-len-first-line-commit-msg;

## [0.5.0]	 &#8212; 	2025-09-24:
### Added
  - Adicionado hook check-len-first-line-commit-msg;
  - Adicionado Enum para validar tipos do conventional commits;
  - Adicionado hook pre-commit-installed;
  - Testes unitÃ¡rios para CLI;
  - Refactor: Cobertura de testes em cÃ³digo Python ampliada;
  - Estrutura `assets` definida;
  - Modelos de exemplos retirados da estrutura principal;

## [0.5.0rc1]	 &#8212; 	2025-09-22:
### Added
  - Adicionado hook pre-commit-installed;
  - Testes unitÃ¡rios para CLI;
  - Refactor: Cobertura de testes em cÃ³digo Python ampliada;
  - Estrutura `assets` definida;
  - Modelos de exemplos retirados da estrutura principal;

## [0.4.0]	 &#8212; 	2025-09-20:
### Added
  - Badging `pre-commit`;
  - Acrescentado logo do projeto;
  - Acrescentado configuraÃ§Ã£o padrÃ£o para editores de cÃ³digo no projeto;
  - Acrescentado cores em multiplataforma;

## [0.3.0]	 &#8212; 	2025-09-15:
### Added
  - Adicionado hook check-precommit-installed;
  - Adicionado hook effort-message;
  - Adicionado hook de validaÃ§Ã£o para filenames em Python;
  - Acrescentados testes unitÃ¡rios;
  - Acrescentado CHANGELOG.md;
  - Configurado `pre-commit` para gerir e restringir violaÃ§Ã£o de regras;
### Changed
  - Aplicado QA parcialmente ao projeto;
  - Adicionado suite de teste pytest;
  - Refinado a configuraÃ§Ã£o pytest conforme padrÃµes JEDI;
  - Sincronizado versÃ£o do projeto com a versÃ£o do pacote;

## [0.2.1]	 &#8212; 	2025-09-11:
### Changed
  - ConfiguraÃ§Ã£o do hook detected-key;

## [0.2.0]	 &#8212; 	2025-09-11:
### Added
  - Scripts piloto adicionados;
  - Estrutura criada;

## 0.1.0	 &#8212; 	2025-09-11:
### Added
  - Projeto iniciado;

---

[0.2.0]: https://github.com/development-incolume/incolume.py.githooks/compare/0.1.0...0.2.0
[0.2.1]: https://github.com/development-incolume/incolume.py.githooks/compare/0.2.0...0.2.1
[0.3.0]: https://github.com/development-incolume/incolume.py.githooks/compare/0.2.1...0.3.0
[0.4.0]: https://github.com/development-incolume/incolume.py.githooks/compare/0.3.0...0.4.0
[0.5.0rc1]: https://github.com/development-incolume/incolume.py.githooks/compare/0.4.0...0.5.0rc1
[0.5.0]: https://github.com/development-incolume/incolume.py.githooks/compare/0.5.0rc1...0.5.0
[1.0.0]: https://github.com/development-incolume/incolume.py.githooks/compare/0.5.0...1.0.0
[1.1.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.0.0...1.1.0
[1.2.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.1.0...1.2.0
[1.3.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.2.0...1.3.0
[1.4.0rc1]: https://github.com/development-incolume/incolume.py.githooks/compare/1.3.0...1.4.0rc1
[1.4.0rc2]: https://github.com/development-incolume/incolume.py.githooks/compare/1.4.0rc1...1.4.0rc2
[1.4.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.4.0rc2...1.4.0
[1.5.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.4.0...1.5.0
[1.6.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.5.0...1.6.0
[1.7.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.6.0...1.7.0
[1.8.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.7.0...1.8.0
[1.9.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.8.0...1.9.0
[1.10.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.9.0...1.10.0
[1.11.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.10.0...1.11.0
[1.12.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.11.0...1.12.0
[1.13.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.12.0...1.13.0
[1.14.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.13.0...1.14.0
[1.15.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.14.0...1.15.0
[1.16.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.15.0...1.16.0
[1.17.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.16.0...1.17.0
[1.18.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.17.0...1.18.0
[1.18.1]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.0...1.18.1
[1.18.2]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.1...1.18.2
[1.18.3]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.2...1.18.3
[1.18.4]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.3...1.18.4
[1.18.5]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.4...1.18.5
[1.19.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.18.5...1.19.0
[1.20.0rc1]: https://github.com/development-incolume/incolume.py.githooks/compare/1.19.0...1.20.0rc1
[1.20.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.20.0rc1...1.20.0
[1.21.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.20.0...1.21.0
[1.22.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.21.0...1.22.0
[1.22.1]: https://github.com/development-incolume/incolume.py.githooks/compare/1.22.0...1.22.1
[1.23.0]: https://github.com/development-incolume/incolume.py.githooks/compare/1.22.1...1.23.0
[Unreleased]: https://github.com/development-incolume/incolume.py.githooks/compare/1.23.0...Unreleased
