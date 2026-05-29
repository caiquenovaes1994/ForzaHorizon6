# Forza Horizon 6 Car Manager

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![NiceGUI](https://img.shields.io/badge/NiceGUI-3.12.1-2b3a4a?style=flat)
![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-4.14.3-4B8BBE?style=flat)
![Requests](https://img.shields.io/badge/Requests-2.34.2-00599C?style=flat)

Um gerenciador de coleção de carros desenvolvido especialmente para os jogadores de **Forza Horizon 6**. Controle facilmente os veículos que você já adquiriu e os que já fotografou (capturou) no jogo, com uma interface bonita e inspirada no visual do Forza.

## 🏁 Funcionalidades

- **Lista Oficial Completa:** Todos os carros obtidos em tempo real da lista oficial (`forza.net/fh6cars`), classificados em ordem alfabética.
- **Controle de Progresso:** Marque rapidamente quais carros você já possui na sua garagem ("Adquirido") e quais já foram fotografados ("Capturado").
- **Filtro Inteligente:** Filtre facilmente sua coleção por marcas (fabricantes).
- **Interface Imersiva:** Design moderno no estilo *Dark Mode* com toques em rosa magenta, refletindo a estética vibrante do Forza Horizon 6.
- **Salvamento Automático:** Suas alterações são salvas localmente e carregadas instantaneamente sempre que você iniciar o app.

## 🚀 Como Executar

1. Clone o repositório ou baixe os arquivos.
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install nicegui beautifulsoup4 requests
   ```

4. Obtenha a lista atualizada de carros do Forza (isso criará a pasta `data` com o arquivo `cars.json`):

   ```bash
   python scraper.py
   ```

5. Inicie a aplicação:

   ```bash
   python main.py
   ```

6. O aplicativo será aberto automaticamente no seu navegador padrão (geralmente em `http://localhost:8080`).

---

## 👨‍💻 Autor

Desenvolvido por **Caique Novaes**

[![GitHub](https://img.shields.io/badge/GitHub-Perfil-181717?style=flat&logo=github&logoColor=white)](https://github.com/caiquenovaes1994)
[![Gmail](https://img.shields.io/badge/Gmail-Contato-D14836?style=flat&logo=gmail&logoColor=white)](mailto:caiquenovaes1994@gmail.com)

> *"Acelere seus sonhos, gerencie suas conquistas. O horizonte o aguarda!"*
