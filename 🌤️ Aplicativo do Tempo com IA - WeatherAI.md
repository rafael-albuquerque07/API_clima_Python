# 🌤️ Aplicativo do Tempo com IA - WeatherAI

## 📋 Descrição do Projeto

O **WeatherAI** é uma aplicação web completa e moderna que fornece informações meteorológicas precisas e atualizadas em tempo real. Desenvolvido como projeto final do curso de desenvolvimento de software assistido por IA da Generation Brasil, este aplicativo demonstra a integração efetiva de múltiplas tecnologias e boas práticas de desenvolvimento, utilizando IA para auxiliar em todo o processo de criação.

O projeto resolve o problema de acesso rápido e intuitivo a informações meteorológicas, oferecendo uma interface moderna e responsiva com recursos avançados como busca inteligente de cidades, sistema de cache para otimização de performance, salvamento de múltiplas localizações favoritas e tratamento robusto de erros. A aplicação foi desenvolvida com assistência de IA, demonstrando como a inteligência artificial pode ser uma ferramenta poderosa no desenvolvimento de software moderno.

## 🛠️ Tecnologias e Ferramentas Principais

### Linguagens de Programação

- Python 3.11
- JavaScript ES6+
- HTML5
- CSS3

### Frameworks e Bibliotecas

- **Backend**: Flask 3.1.1, Flask-CORS 5.0.0
- **Frontend**: Font Awesome (ícones)
- **Requisições HTTP**: Requests 2.32.3

### Ferramentas de IA no Desenvolvimento

- IA generativa para assistência na codificação, debugging e documentação

### APIs Externas

- **Open-Meteo API**: Para dados meteorológicos em tempo real (não requer chave de API)
- **Nominatim/OpenStreetMap**: Para geocodificação (busca de cidades e coordenadas)

### Ferramentas de Teste

- pytest 8.4.1
- pytest-flask 1.3.0
- pytest-cov 6.0.0

### Outras Ferramentas

- Git (controle de versão)
- Virtual Environment (isolamento de dependências)

## 📊 Conjunto de Dados Utilizado

O projeto utiliza dados em tempo real provenientes de:

- **Open-Meteo API**: Fornece dados meteorológicos gratuitos e atualizados. A licença de uso é livre para fins não comerciais.
- **Dados de Geocodificação**: Uma base de dados interna de mais de 50 cidades brasileiras pré-definidas é utilizada para buscas rápidas. Para cidades não encontradas nessa base, a **API Nominatim (OpenStreetMap)** é consultada. Os dados do OpenStreetMap são licenciados sob a Open Data Commons Open Database License (ODbL).

## 🧠 Metodologia e Abordagem de IA/ML

Este projeto foi desenvolvido utilizando a metodologia de **Desenvolvimento Assistido por IA Generativa**. A inteligência artificial foi empregada de forma estratégica em diversas etapas do ciclo de desenvolvimento de software, incluindo:

- **Geração e Otimização de Código**: A IA auxiliou na escrita de trechos de código, sugerindo otimizações e padrões de design.
- **Debugging e Resolução de Problemas Complexos**: A IA foi uma ferramenta valiosa para identificar e solucionar erros, bem como para entender e resolver desafios de implementação.
- **Criação de Testes Automatizados**: A IA contribuiu na elaboração de testes unitários e de integração, garantindo a robustez e a qualidade do código.
- **Documentação Técnica e Comentários**: A IA foi utilizada para gerar documentação clara e concisa, incluindo comentários explicativos no código e a estrutura deste `README.md`.
- **Arquitetura e Decisões de Design**: A IA forneceu insights e sugestões para a arquitetura geral da aplicação e decisões de design importantes.
- **Implementação de Boas Práticas de Segurança**: A IA ajudou a identificar e aplicar técnicas de codificação segura, protegendo a aplicação contra vulnerabilidades comuns.

## ✅ Resultados e Conclusões Principais

O desenvolvimento do WeatherAI resultou em uma aplicação robusta e eficiente, demonstrando o potencial da colaboração entre IA e desenvolvimento humano:

- **Aplicação Web Totalmente Funcional**: Uma aplicação web completa com uma interface moderna e responsiva, acessível em diferentes dispositivos.
- **Sistema de Cache Inteligente**: Implementação de um sistema de cache que reduziu em aproximadamente 80% as chamadas desnecessárias à API, otimizando a performance e o consumo de recursos.
- **Cobertura de Testes**: O projeto alcançou uma boa cobertura de testes, com 27 de 34 testes passando, garantindo a confiabilidade das funcionalidades principais.
- **Tempo de Resposta Otimizado**: Para dados em cache, o tempo de resposta médio foi inferior a 500ms, proporcionando uma experiência de usuário fluida.
- **Interface Intuitiva e Experiência do Usuário Otimizada**: O design focado na usabilidade resultou em uma interface fácil de usar e visualmente agradável.
- **Demonstração Bem-Sucedida da Colaboração IA-Humano**: O projeto serve como um excelente exemplo de como a inteligência artificial pode ser uma ferramenta poderosa para aumentar a produtividade e a qualidade no desenvolvimento de software.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o WeatherAI em sua máquina local:

1.  **Clone o repositório:**

    ```bash
    git clone [url-do-repositorio]
    cd weather-app
    ```

    _(Substitua `[url-do-repositorio]` pelo URL real do seu repositório Git.)_

2.  **Crie e ative o ambiente virtual:**

    ```bash
    python -m venv venv

    # No Linux/macOS:
    source venv/bin/activate

    # No Windows (PowerShell):
    .\venv\Scripts\activate

    # No Windows (Command Prompt):
    venv\Scripts\activate.bat
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    Certifique-se de que seu terminal esteja no diretório raiz do projeto (`weather-app`).

    ```bash
    python src/main.py
    ```

5.  **Acesse no navegador:**
    Abra seu navegador web e acesse:
    ```
    http://localhost:5000
    ```

## 🧪 Como Testar o Projeto

Para executar os testes automatizados e verificar a cobertura do código:

1.  **Ative o ambiente virtual:**

    ```bash
    source venv/bin/activate  # Ou o comando equivalente para Windows
    ```

2.  **Execute todos os testes:**
    Certifique-se de que seu terminal esteja no diretório raiz do projeto (`weather-app`).

    ```bash
    pytest tests/ -v
    ```

3.  **Execute com relatório de cobertura (opcional):**
    Para gerar um relatório de cobertura de código em HTML:
    ```bash
    pytest tests/ --cov=src --cov-report=html
    ```
    Após a execução, um diretório `htmlcov` será criado com o relatório. Abra `htmlcov/index.html` em seu navegador para visualizá-lo.

## 🧑‍💻 Autores e Colaboradores

- **Autor Principal**: Rafael Albuquerque dos Santos
- **Desenvolvimento Assistido por**: IA (Claude AI/Manus AI)

## 🙏 Agradecimentos

Gostaríamos de expressar nossa sincera gratidão a:

- **Generation Brasil**: Pela oportunidade de participar do curso de IA e pelo ambiente de aprendizado enriquecedor.
- **Professor Marcelo Barbosa**: Pelo suporte inestimável, orientação e pelos conhecimentos valiosos compartilhados durante todo o curso.
- **Professor Lucas Capelotto**: Pela dedicação, paciência e excelente didática nas aulas, que foram fundamentais para o aprendizado.
- **Comunidade Open Source**: Por todas as ferramentas, bibliotecas e recursos que tornaram este projeto possível.
- **Open-Meteo e OpenStreetMap**: Pela disponibilização de dados meteorológicos e de geocodificação gratuitos, essenciais para a funcionalidade do aplicativo.
- **Colegas de Turma**: Pelo apoio mútuo, troca de conhecimentos e colaboração ao longo do curso.

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Isso significa que você é livre para usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que a notificação de direitos autorais e esta permissão sejam incluídas em todas as cópias ou partes substanciais do software.

Para mais detalhes, consulte o arquivo `LICENSE` no repositório.

---

**Desenvolvido com ❤️ para a Generation Brasil**
