# Instalação

O consumo do pacote se dá, em geral, pelo [pre-commit] no projeto
consumidor — o pacote não precisa ser instalado diretamente na maioria dos
casos.

## Via pre-commit (recomendado)

Adicione ao `.pre-commit-config.yaml` do projeto consumidor:

```yaml
- repo: https://github.com/development-incolume/incolume.py.githooks
  rev: 1.20.0
  hooks:
    - id: check-len-first-line
    - id: detect-key
    # demais hooks: consulte o modelo no README
```

!!! warning "Revisão publicada"

    A `rev` citada acima deve refletir a última tag publicada; o modelo
    completo e atualizado está no [README do repositório][modelo].

## Via pip/uv (a partir do repositório)

```sh
pip install git+https://github.com/development-incolume/incolume.py.githooks.git
```

ou, com `uv`:

```sh
uv tool install git+https://github.com/development-incolume/incolume.py.githooks.git
```

[pre-commit]: https://pre-commit.com/
[modelo]: https://github.com/development-incolume/incolume.py.githooks#usage
