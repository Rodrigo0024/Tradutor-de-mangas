Tradutor Cultural & Contextual (Mangás, HQs & Jogos Retrô)

Um tradutor e localizador inteligente alimentado por IA Multimodal projetado para compreender não apenas o texto, mas todo o contexto visual e cultural de páginas de mangás, histórias em quadrinhos ocidentais e telas de jogos retrô.

O Problema vs. A Solução

Tradutores tradicionais baseados apenas em OCR (reconhecimento de texto) costumam falhar em mídias visuais porque:

Ignoram a ordem de leitura: Confundem a leitura oriental (direita para esquerda) com a ocidental.

Perdem o contexto emocional: Não sabem se um personagem está gritando de raiva, sussurrando ou sendo irônico, resultando em traduções robóticas.

Não adaptam nuances culturais: Honoríficos japoneses, gírias de época e trocadilhos acabam sendo traduzidos ao pé da letra.

A Solução: Este aplicativo utiliza o modelo multimodal Mistral Large via NVIDIA NIM API para analisar a cena completa — expressões faciais, postura, interface do jogo e balões — entregando uma localização natural, respeitando a direção de leitura e oferecendo notas culturais.

Funcionalidades Principais

Captura Rápida via Área de Transferência (Ctrl+V / Win+Shift+S): Recorte trechos de qualquer aba do navegador ou emulador e cole diretamente na interface, sem precisar salvar arquivos no computador.

Suporte a Upload de Imagens: Envio tradicional de arquivos .png, .jpg, .jpeg e .webp.

Adaptação à Ordem de Leitura:

Mangá: Direita para a esquerda, de cima para baixo.

HQ / Comic: Esquerda para a direita, de cima para baixo.

Jogos Retrô: Identificação inteligente de caixas de diálogo, menus e itens.

Três Modos de Tradução:

Adaptação Natural (Localização): Gírias e expressões adaptadas ao português brasileiro de acordo com a emoção da cena.

Fiel ao Original + Notas Culturais: Preserva honoríficos (-san, -kun, -sama) e explica referências.

Modo Estudo: Transcreve o texto original, exibe a tradução e detalha o vocabulário-chave.

Feedback Visual em Tempo Real: Barra de status interativa (st.status) acompanhando cada etapa do processamento da imagem até a resposta final.

Tecnologias Utilizadas

Python: Linguagem base da aplicação.

Streamlit: Framework para construção rápida da interface web interativa.

NVIDIA NIM API (Mistral Large): Motor de inferência multimodal responsável pela visão computacional e tradução contextual.

Pillow (PIL): Manipulação, conversão de canais de cor (RGBA/RGB) e codificação de imagens em Base64.

streamlit-paste-button: Integração nativa com a área de transferência do sistema operacional.

python-dotenv: Gerenciamento seguro de variáveis de ambiente e credenciais.

Como Executar o Projeto

1. Clone o repositório

git clone https://github.com/seu-usuario/tradutor-contextual.git
cd tradutor-contextual


2. Crie um ambiente virtual e instale as dependências

python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt


3. Configure sua Chave de API

Renomeie o arquivo .env.example para .env e insira sua chave obtida gratuitamente no portal NVIDIA Build:

NVIDIA_API_KEY=nvapi-sua-chave-aqui


4. Inicie a aplicação

streamlit run app.py


O Que Eu Aprendi Construindo Este Projeto

Desenvolver este aplicativo foi uma experiência prática fundamental para consolidar conceitos essenciais de engenharia de software e integração com Inteligência Artificial:

Integração com APIs Multimodais & Engenharia de Payload:

Aprendi como estruturar requisições HTTP (POST) enviando simultaneamente instruções textuais e imagens codificadas em Data URL Base64 (image/png e image/jpeg).

Compreendi a importância de tratar canais de transparência (RGBA para RGB) com a biblioteca Pillow antes da codificação para evitar falhas de serialização.

Autenticação e Segurança de Credenciais:

Dominei o padrão de autenticação via cabeçalhos HTTP utilizando tokens Bearer.

Implementei boas práticas de segurança utilizando arquivos .env para isolar chaves sensíveis, acompanhados de .env.example e .gitignore devidamente configurados para evitar vazamento de credenciais no GitHub.

Tratamento de Timeouts e Estabilidade de Rede:

Lidei na prática com erros de ReadTimeout causados pelo tempo de raciocínio de modelos grandes. Aprendi a calibrar o timeout das requisições (180s) e ajustar hiperparâmetros do modelo (como o reasoning_effort) para equilibrar velocidade e qualidade de resposta.

Engenharia de Prompt Orientada a Contexto:

Estruturei prompts dinâmicos que alteram o comportamento da IA conforme o tipo de mídia, forçando o modelo a analisar expressões visuais antes de gerar a tradução e formatando a saída de maneira limpa e previsível.

Experiência do Usuário (UX) em Aplicações de IA:

Entendi como melhorar a percepção de espera do usuário utilizando componentes de status (st.status) e atalhos de produtividade (como colar recortes direto da área de transferência) para tornar o fluxo de uso fluido no dia a dia.

Estrutura de Arquivos

tradutor-contextual/
├── .env.example        # Modelo de configuração das variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git (proteção de chaves e venv)
├── app.py              # Código principal da interface Streamlit e integração com a API
├── requirements.txt    # Lista de dependências do projeto
└── README.md           # Documentação do projeto


Contribuições e Próximos Passos

Sinta-se à vontade para abrir issues ou enviar pull requests! Algumas ideias para futuras versões:

[ ] Exportação dos diálogos traduzidos em formato .txt ou .md para estudos de idiomas.

[ ] Histórico de cenas traduzidas na mesma sessão.

[ ] Suporte para seleção de múltiplos provedores de IA.