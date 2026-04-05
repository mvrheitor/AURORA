## [4.0.0] - 2026-04-05

### Changed
- **Arquitetura do Terminal:** Transição de execuções efêmeras para uma arquitetura stateful.

### Added
- **Tool executar_comando:** Permite enviar instruções diretamente ao shell em execução e aguardar o processamento.
- **Tool enviar_input:** Possibilita a interação com processos em andamento, enviando texto diretamente para a entrada padrão (stdin) de programas que aguardam resposta do usuário.
- **Tool ler_terminal:** Nova capacidade de observação passiva do buffer do terminal.

### Removed
- Tools de sistema restritas e obsoletas (pwd_ls, criar_pasta, criar_arquivo).

### Fixed
- **Path Resolution:** Correção de um erro estrutural de diretório. A aplicação agora resolve o caminho absoluto do arquivo de prompt corretamente, não falhando mais caso a execução seja iniciada fora do diretório raiz do projeto.
