"""Check commit message footers.

Valida os rodapes da mensagem de commit conforme Conventional Commits
e as regras do AGENTS.md: rodape e o ultimo paragrafo da mensagem;
cada linha deve ser ``<token>: <valor>`` (ou ``<token> <valor>``, para
``Closes``/``Refs``), com token em {Closes, Refs, Signed-off-by,
Co-authored-by, Reviewed-by, Acked-by}; referencia a issue (``#<id>``)
so e aceita em ``Closes`` ou ``Refs``.

(c) Copyright 2026 incolume.com.br. All rights reserved.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

FOOTER_TOKENS: frozenset[str] = frozenset({
    'Closes',
    'Refs',
    'Signed-off-by',
    'Co-authored-by',
    'Reviewed-by',
    'Acked-by',
})
ISSUE_TOKENS: frozenset[str] = frozenset({'Closes', 'Refs'})
ISSUE_REFERENCE: str = r'#\d+'
LINE_COMMENT: str = '#'


def check_commit_footer(filenames: list[str]) -> int:
    """Validate footers of commit message file(s).

    :param filenames: commit message files to validate.
    :return: 0 se todos os rodapes sao validos; 1 caso contrario.

    .. versionadded:: 1.22.0
    """
    status: int = 0
    for filename in filenames:
        file = Path(filename)
        if not file.is_file():
            logging.critical('File %s not found.', file)
            status = 1
            continue

        if not __is_footer_valid(file):
            status = 1

    return status


def __is_footer_valid(file: Path) -> bool:
    """Check footers of a single commit message file.

    :param file: commit message file.
    :return: True se o rodape e valido; False caso contrario.

    .. versionadded:: 1.22.0
    """
    content_lines = [
        line
        for line in file.read_text(encoding='utf-8').splitlines()
        if not line.lstrip().startswith(LINE_COMMENT)
    ]
    footers: list[str] = __extract_footers(content_lines)

    for footer in footers:
        if __is_valid_footer(footer):
            logging.info('Valid footer: %s', footer)
            continue
        if __is_body_line(footer):
            continue
        logging.critical(
            'Invalid footer: %s'
            '\nExpected: <token>: <value> or <token> <value>,'
            ' tokens: %s; issue reference only in Closes/Refs.',
            footer,
            sorted(FOOTER_TOKENS),
        )
        return False

    return True


def __extract_footers(content_lines: list[str]) -> list[str]:
    """Extract the footer block (last non-empty paragraph).

    :param content_lines: commit message lines without comments.
    :return: lines of the last non-empty paragraph.

    .. versionadded:: 1.22.0
    """
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for line in content_lines:
        if line.strip():
            current.append(line)
        elif current:
            paragraphs.append(current)
            current = []
    if current:
        paragraphs.append(current)

    return paragraphs[-1] if paragraphs else []


def __is_valid_footer(footer: str) -> bool:
    """Check a single footer line.

    :param footer: footer line.
    :return: True se o rodape e valido; False caso contrario.

    .. versionadded:: 1.22.0
    """
    match = re.match(
        r'^(?P<token>[A-Za-z-]+):\s*(?P<value>\S.*)$',
        footer,
    )
    if match:
        token: str = match.group('token')
        value: str = match.group('value')

        if token not in FOOTER_TOKENS:
            return False

        return not re.search(ISSUE_REFERENCE, value) or token in ISSUE_TOKENS

    # Forma especial de Conventional Commits: `Closes #<id>` / `Refs #<id>`.
    return bool(re.match(r'^(?:Closes|Refs) #\d+$', footer))


def __is_body_line(line: str) -> bool:
    """Check if a line is a plain body line (not a footer attempt).

    :param line: line of the last paragraph.
    :return: True se a linha e corpo livre (sem padrao de rodape).

    .. versionadded:: 1.22.0
    """
    # Linha com referencia a issue fora das formas validas e rodape invalido.
    # Linha com padrao `<token>:` (ou tentativa proxima) e candidata a rodape.
    return not re.search(ISSUE_REFERENCE, line) and not re.match(
        r'^[A-Za-z-]+\s*:',
        line,
    )
