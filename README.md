Sobre o projeto
Tradutores tradicionais baseados apenas em OCR (reconhecimento óptico de caracteres) podem apresentar dificuldades ao trabalhar com mídias visuais. Muitas vezes, eles interpretam incorretamente a ordem dos quadros, ignoram expressões e emoções dos personagens ou traduzem referências culturais de maneira literal.

O Tradutor Cultural & Contextual busca resolver esses problemas utilizando o modelo multimodal Mistral Large, por meio da NVIDIA NIM API. Em vez de analisar somente o texto, a aplicação considera a imagem completa — incluindo expressões faciais, linguagem corporal, balões de fala e interfaces de jogos — para produzir traduções mais naturais e contextualizadas.

O objetivo é preservar o significado, o tom e as nuances culturais do conteúdo original, oferecendo uma tradução fluida em português brasileiro.
Funcionalidades
Entrada de imagens
- Captura pela área de transferência: cole diretamente na aplicação capturas de tela ou recortes usando Ctrl+V ou Win+Shift+S, sem precisar salvar os arquivos previamente.
- Envio de imagens: suporte aos formatos .png, .jpg, .jpeg e .webp.
Ordem de leitura adaptada à mídia
A aplicação adapta sua análise de acordo com o tipo de conteúdo:
Tipo de conteúdo	Ordem de leitura / interpretação
Mangás	Da direita para a esquerda, de cima para baixo
HQs ocidentais	Da esquerda para a direita, de cima para baixo
Jogos retrô	Identificação de caixas de diálogo, menus e itens do jogo


Modos de tradução
- Adaptação Natural (Localização): adapta gírias e expressões ao português brasileiro, considerando o tom e as emoções da cena.
- Tradução Fiel + Notas Culturais: preserva honoríficos japoneses (como -san, -kun e -sama) e explica referências culturais relevantes.
- Modo Estudo: apresenta o texto original, sua tradução e explicações sobre o vocabulário-chave.
Acompanhamento do processamento
Um componente de status interativo do Streamlit (st.status) informa ao usuário o andamento das etapas de processamento da imagem e geração da tradução.
Tecnologias utilizadas
Tecnologia	Finalidade
Python	Linguagem principal da aplicação
Streamlit	Construção da interface web interativa
NVIDIA NIM API (Mistral Large)	Compreensão multimodal de imagens e tradução contextual
Pillow (PIL)	Manipulação de imagens, conversão de RGBA/RGB e codificação em Base64
streamlit-paste-button	Integração com a área de transferência
python-dotenv	Gerenciamento de variáveis de ambiente e credenciais da API


Como executar o projeto
Pré-requisitos
- Python instalado na máquina.
- Uma chave de API da NVIDIA, disponível na plataforma NVIDIA Developer.
1. Clone o repositório
git clone git@github.com:Rodrigo0024/Tradutor-de-mangas.git
cd Tradutor-de-mangas
2. Crie um ambiente virtual
python -m venv venv
Ative o ambiente virtual:

Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
3. Instale as dependências
pip install -r requirements.txt
4. Configure sua chave de API
Renomeie o arquivo .env.example para .env e adicione sua chave de API da NVIDIA:
NVIDIA_API_KEY=nvapi-sua-chave-aqui
Mantenha o arquivo .env privado. Não envie chaves de API ou outras credenciais para o controle de versão.
5. Execute a aplicação
streamlit run app.py
O Streamlit disponibilizará um endereço local para acessar a aplicação pelo navegador.
O que aprendi com este projeto
Desenvolver este projeto foi uma oportunidade prática de consolidar conhecimentos importantes sobre desenvolvimento de software e integração com inteligência artificial.
Integração com APIs multimodais e engenharia de payload
- Aprendi a estruturar requisições HTTP POST que enviam simultaneamente instruções textuais e imagens codificadas em Data URL Base64 (image/png e image/jpeg).
- Compreendi por que canais de transparência podem exigir a conversão de imagens de RGBA para RGB com Pillow antes da codificação, evitando problemas de serialização.
Autenticação e segurança de credenciais
- Implementei autenticação baseada em tokens por meio de cabeçalhos HTTP Bearer.
- Apliquei boas práticas de gerenciamento de credenciais utilizando arquivos .env, um modelo .env.example e regras no .gitignore para ajudar a impedir que informações sensíveis sejam publicadas no GitHub.
Tratamento de timeouts e estabilidade de rede
- Trabalhei com erros ReadTimeout, que podem ocorrer devido ao tempo de processamento de modelos grandes.
- Aprendi a configurar o tempo limite das requisições (180 segundos neste projeto) e ajustar parâmetros do modelo, como reasoning_effort, para equilibrar qualidade das respostas e tempo de processamento.
Engenharia de prompts orientada a contexto
- Desenvolvi prompts dinâmicos que adaptam o comportamento do modelo de acordo com o tipo de mídia.
- Estruturei instruções para que a IA analise as expressões visuais antes de traduzir e retorne respostas organizadas e previsíveis.
Experiência do usuário em aplicações com IA
- Utilizei o componente st.status do Streamlit para tornar as etapas de processamento visíveis e melhorar a percepção de agilidade da aplicação.
- Implementei atalhos de produtividade com a área de transferência para facilitar a tradução de capturas de tela e recortes.
Estrutura do projeto
Tradutor-de-mangas/
├── .env.example        # Modelo das variáveis de ambiente
├── .gitignore          # Arquivos ignorados e proteção de credenciais
├── app.py              # Interface Streamlit e integração com a API
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
Próximas melhorias
Ideias para versões futuras:
- [ ] Exportar diálogos traduzidos nos formatos .txt ou .md para estudo de idiomas.
- [ ] Manter um histórico das cenas traduzidas durante a sessão.
- [ ] Adicionar suporte a múltiplos provedores de inteligência artificial.
Contribuições
Sugestões e contribuições são bem-vindas! Fique à vontade para abrir uma issue ou enviar um pull request.
