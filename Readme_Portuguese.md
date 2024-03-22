# Aplicação de Detecção e Captura de Objetos

Este script em Python foi desenvolvido para detecção de movimento e captura de objetos utilizando a biblioteca OpenCV. Ele oferece uma interface gráfica de usuário (GUI) construída com Tkinter para interação e monitoramento fácil.

## Características
- **Detecção de Movimento**: Utiliza técnicas de subtração de fundo e detecção de contornos para identificar movimento no fluxo de vídeo.
- **Captura de Objetos**: Captura quadros contendo objetos detectados e os salva em um diretório especificado.
- **Transmissão de Vídeo em Tempo Real**: Mostra a transmissão de vídeo ao vivo das câmeras conectadas na GUI.
- **Gravação**: Inicia a gravação quando movimento é detectado, salvando o vídeo com marcas de tempo.
- **Interface do Usuário**: Oferece botões para iniciar e parar a detecção, visualizar imagens capturadas e acessar informações de contato.

## Requisitos
- Python 3.x
- OpenCV (`cv2`)
- Tkinter
- PIL (`Image`, `ImageTk`)
- `winsound` (apenas no Windows)

## Uso
1. Certifique-se de que todas as dependências estejam instaladas.
2. Execute o script.
3. Clique em "Buscar Mais Câmeras" para procurar câmeras disponíveis.
4. Após detectar as câmeras, clique em "Iniciar Detecção" para iniciar a detecção de movimento.
5. Os objetos detectados serão destacados, e os quadros contendo-os serão salvos.
6. Clique em "Parar Detecção" para interromper a detecção de movimento.
7. Use "Visualizar Capturas" para abrir o diretório contendo as imagens capturadas.
8. Para obter mais ajuda ou fazer perguntas, clique em "Contato" para visitar o link fornecido.

## Contato
Para suporte ou perguntas, visite nosso [servidor no Discord](https://discord.gg/6kfbMJXKRy).
