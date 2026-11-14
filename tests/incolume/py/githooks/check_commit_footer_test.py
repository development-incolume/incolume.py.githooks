"""Module test check_commit_footer hook."""

from __future__ import annotations

import incolume.py.githooks.check_commit_footer as pkg
from incolume.py.githooks.cli.cli import check_commit_footer_cli
import pytest
import tempfile
import inspect
from pathlib import Path
import shutil


class TestCaseCheckCommitFooter:
    """Test class for check_commit_footer module."""

    test_dir: Path = Path(tempfile.gettempdir(), inspect.stack()[0][3])

    @classmethod
    def setup_class(cls) -> None:
        """Set class."""
        cls.test_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class. Remove generated files."""
        shutil.rmtree(cls.test_dir)

    def commit_file(self, content: str) -> Path:
        """Write a commit message temp file and return its path."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            dir=self.test_dir,
            suffix='.txt',
            delete=False,
            encoding='utf-8',
        ) as tf:
            tf.write(content)
        return Path(tf.name)

    def test_sem_rodape_ok(self) -> None:
        """Commit sem rodape: aceito."""
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'feat: nova funcionalidade\n\ncorpo da mensagem\n'
                    )
                )
            ])
            == 0
        )

    def test_closes_valido(self) -> None:
        """Rodape Closes #<id>: aceito."""
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'feat: nova funcionalidade\n\nCloses #42\n'
                    )
                )
            ])
            == 0
        )

    def test_refs_valido(self) -> None:
        """Rodape Refs: #<id>: aceito."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('docs: ajusta texto\n\nRefs: #7\n'))
            ])
            == 0
        )

    def test_signedoffby_e_coauthored_validos(self) -> None:
        """Rodapes Signed-off-by e Co-authored-by: aceitos."""
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'feat: algo\n\n'
                        'Signed-off-by: Brito <dev@incolume.com.br>\n'
                        'Co-authored-by: OpenBot <dev@incolume.com.br>\n'
                    )
                )
            ])
            == 0
        )

    def test_reviewedby_ackedby_validos(self) -> None:
        """Rodapes Reviewed-by e Acked-by: aceitos."""
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'fix: corrige algo\n\n'
                        'Reviewed-by: Fulano <dev@incolume.com.br>\n'
                        'Acked-by: Sicrano <dev@incolume.com.br>\n'
                    )
                )
            ])
            == 0
        )

    def test_comentarios_ignorados(self) -> None:
        """Linhas de comentario do git nao contam como rodape."""
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'feat: algo\n\nCloses #1\n\n'
                        '# Please enter the commit message\n'
                    )
                )
            ])
            == 0
        )

    def test_token_desconhecido_rejeitado(self) -> None:
        """Rodape com token fora da lista: rejeitado."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('feat: algo\n\nCloses-by: #42\n'))
            ])
            == 1
        )

    def test_issue_fora_de_closes_refs_rejeitada(self) -> None:
        """Referencia a issue em token que nao seja Closes/Refs: rejeitada."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('feat: algo\n\nReviewed-by: #42\n'))
            ])
            == 1
        )

    def test_rodape_no_ultimo_paragrafo_apenas(self) -> None:
        """Texto parecido com rodape no corpo nao rejeita.

        So o ultimo paragrafo e tratado como rodape.
        """
        assert (
            pkg.check_commit_footer([
                str(
                    self.commit_file(
                        'feat: algo\n\nSigned-off-by: vale so no fim\n\nCloses #9\n'
                    )
                )
            ])
            == 0
        )

    def test_rodape_sem_valor_rejeitado(self) -> None:
        """Rodape sem valor apos o separador: rejeitado."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('feat: algo\n\nCloses:\n'))
            ])
            == 1
        )

    def test_verso_closes_sem_espaco_rejeitado(self) -> None:
        """Closes#42 sem espaco/separador: rejeitado."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('feat: algo\n\nCloses#42\n'))
            ])
            == 1
        )

    def test_arquivo_inexistente(self) -> None:
        """Arquivo inexistente: falha."""
        assert (
            pkg.check_commit_footer([str(self.test_dir / 'nao_existe.txt')])
            == 1
        )

    def test_espaco_em_branco_consecutivo(self) -> None:
        """Linhas vazias consecutivas sao ignoradas."""
        assert (
            pkg.check_commit_footer([
                str(self.commit_file('\n\nfeat: algo\n\nCloses #1\n'))
            ])
            == 0
        )

    @pytest.mark.parametrize(
        'entry',
        [
            '',
            'feat: msg\nCloses #1\n',
        ],
    )
    def test_naoexequi(self, entry: str) -> None:
        """Flag -N nao executa o hook."""
        arq = self.commit_file(f'{entry}')
        assert (
            check_commit_footer_cli(
                args=['-N', str(arq)], standalone_mode=False
            )
            == 0
        )
