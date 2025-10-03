# CHANGELOG


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Conventional Commit](https://www.conventionalcommits.org/pt-br/v1.0.0/).

This file was automatically generated for [incolume.py.changelog](https://github.com/development-incolume/incolume.py.changelog/-/tree/0.17.0)

---


## [Unreleased]	 &#8212; 	2025-10-02:
### Added
  - Disponibilizar hook check-len-first-line-commit-msg;
  - Disponibilizar Hook footer-signed-off-by;
  - Disponibilizar Hook clean-commit-message;
  - Disponibilizar Hook git-diff;
### Changed
  - Acrescentado modelo de configuração dos hooks ao README.md;

## [1.4.0rc2]	 &#8212; 	2025-10-03:
### Changed
  - Alteração no modo verboso;

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
  - Interfaces para hooks centralizadas no módulo CLI;
### Removed
  - Modulo incolume.py.githooks.pre_commit_installed removido;

## [1.1.0]	 &#8212; 	2025-09-28:
### Added
  - Hook `detect-key` disponibilizado;
### Changed
  - Cobertura total do código implementado;
  - Chamada de hooks com argumentos configuráveis através do arquivo yaml;

## [1.0.0]	 &#8212; 	2025-09-26:
### Added
  - Hook check-max-len-first-line-commit-msg;
  - Hook check-min-len-first-line-commit-msg;
  - Hook footer-signed-off-by;
  - Hook clean-commit-message;
  - Hook git-diff;
  - Lançamento da release 1.0.0 com apenas 1 hook: check-valid-filenames;
### Changed
  - Amplicação da cobertura para 99% do código;
### Removed
  - Hook check-len-first-line-commit-msg;

## [0.5.0]	 &#8212; 	2025-09-24:
### Added
  - Adicionado hook check-len-first-line-commit-msg;
  - Adicionado Enum para validar tipos do conventional commits;
  - Adicionado hook pre-commit-installed;
  - Testes unitários para CLI;
  - Refactor: Cobertura de testes em código Python ampliada;
  - Estrutura `assets` definida;
  - Modelos de exemplos retirados da estrutura principal;

## [0.5.0rc1]	 &#8212; 	2025-09-22:
### Added
  - Adicionado hook pre-commit-installed;
  - Testes unitários para CLI;
  - Refactor: Cobertura de testes em código Python ampliada;
  - Estrutura `assets` definida;
  - Modelos de exemplos retirados da estrutura principal;

## [0.4.0]	 &#8212; 	2025-09-20:
### Added
  - Badging `pre-commit`;
  - Acrescentado logo do projeto;
  - Acrescentado configuração padrão para editores de código no projeto;
  - Acrescentado cores em multiplataforma;

## [0.3.0]	 &#8212; 	2025-09-15:
### Added
  - Adicionado hook check-precommit-installed;
  - Adicionado hook effort-message;
  - Adicionado hook de validação para filenames em Python;
  - Acrescentados testes unitários;
  - Acrescentado CHANGELOG.md;
  - Configurado `pre-commit` para gerir e restringir violação de regras;
### Changed
  - Aplicado QA parcialmente ao projeto;
  - Adicionado suite de teste pytest;
  - Refinado a configuração pytest conforme padrões JEDI;
  - Sincronizado versão do projeto com a versão do pacote;

## [0.2.1]	 &#8212; 	2025-09-11:
### Changed
  - Configuração do hook detected-key;

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
[Unreleased]: https://github.com/development-incolume/incolume.py.githooks/compare/1.4.0rc2...Unreleased
