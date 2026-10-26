"""Example for collection.ChainMap.

## Casos de Uso Comuns

- **Simulação de Escopos**: Modelar variáveis locais e globais, onde o
nome local tem precedência sobre o global.

- **Configurações de Aplicação**: Gerar prioridade explícita entre
argumentos de linha de comando, variáveis de ambiente e valores padrão.

- **Inventários Múltiplos**: Acessar vários inventários separados como
se fossem um único banco de dados.
"""

from collections import ChainMap
from typing import Any

from icecream import ic

defaults = {'theme': 'light', 'timeout': 30}
user = {'theme': 'dark'}

# O primeiro argumento tem precedência na busca, mas é onde as escritas ocorrem
config = ChainMap(user, defaults)


def main(config: dict[str, Any] = config) -> None:
    """Run this."""
    ic(config)
    ic(config['theme'])  # Saída: 'dark' (busca em 'user' primeiro)
    ic(
        config['timeout']
    )  # Saída: 30 (busca em 'defaults' se não estiver em 'user')

    config['theme'] = 'blue'  # Atualiza o primeiro mapeamento ('user')
    ic(user)  # Saída: {'theme': 'blue'}


if __name__ == '__main__':
    main()
