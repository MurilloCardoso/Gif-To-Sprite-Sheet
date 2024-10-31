# GIF to Sprite Sheet Converter

## Descrição

Este projeto é uma ferramenta simples desenvolvida em Python que permite converter GIFs animados em sprite sheets, facilitando a utilização de animações em jogos. Através de uma interface gráfica amigável, você pode selecionar um GIF, extrair seus frames e salvá-los como uma sprite sheet, tornando o processo de animação mais eficiente e organizado.

## Funcionalidades

- **Selecionar GIFs:** Escolha um arquivo GIF a partir do seu sistema de arquivos.
- **Extrair Frames:** O projeto extrai cada frame do GIF e o salva em uma pasta chamada "sprites".
- **Criar Sprite Sheet:** Os frames extraídos são combinados em uma única imagem (sprite sheet) que pode ser facilmente utilizada em projetos de jogos.
- **Organização:** O projeto cria uma pasta específica para armazenar todos os frames e a sprite sheet, mantendo seu trabalho organizado.

## Pré-requisitos

Antes de executar o projeto, você precisa ter o Python instalado em seu sistema. Recomenda-se usar a versão 3.7 ou superior.

### Dependências

Você precisará das seguintes bibliotecas Python:

- `Pillow`: Para manipulação de imagens.
- `tkinter`: Para a interface gráfica (já incluído na maioria das distribuições Python).

Instale as dependências usando o seguinte comando:

```bash
pip install pillow
