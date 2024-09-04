# Controle Financeiro para Motoristas de Aplicativo

Este repositório contém o código-fonte e a documentação do projeto **Controle Financeiro**, desenvolvido como parte de um projeto de extensão. O objetivo deste projeto é fornecer uma ferramenta simples e eficaz para gerenciar receitas e despesas de motoristas de aplicativos como Uber e 99.

## Funcionalidades

- **Interface Gráfica**: Uma interface intuitiva para registrar entradas e saídas financeiras. O usuário pode adicionar registros com data, descrição, valor, e categoria (como "Uber", "Combustível", "Manutenção", etc.).
- **Relatório Financeiro**: Geração de um relatório financeiro consolidado com total de entradas, saídas, e lucro líquido.
- **Análise de Dados**: Geração de uma análise de dados em PDF que inclui:
  - Gastos por Categoria.
  - Tendências de Receitas e Despesas.
  - Previsão de Gastos.
  - Balanço Mensal.

## Como Utilizar

1. **Registrar Entradas e Saídas**: Utilize a interface para adicionar novos registros financeiros, selecionando a data, categoria, descrição (opcional), e valor. Escolha se é uma entrada ou saída e clique em "Adicionar".
  
2. **Gerar Relatório**: Ao clicar em "Gerar Relatório", o sistema cria um documento PDF que exibe todos os registros financeiros, agrupados por data e com o total consolidado de entradas, saídas, e lucro líquido.

3. **Gerar Análise de Dados**: A opção "Gerar Análise de Dados" cria um PDF com gráficos e tabelas que analisam as finanças ao longo do tempo, ajudando a identificar padrões e prever despesas futuras.

## Exemplo Visual

### Interface Principal
![Interface Principal](https://github.com/pablovvoliveira/controle-financeiro-extensao/blob/main/layout.png)

### Relatório Financeiro
![Relatório Financeiro](https://github.com/pablovvoliveira/controle-financeiro-extensao/blob/main/relatorio.png)

## Como Executar o Projeto

### Requisitos

- Python 3.x
- PyQt5 (para interface gráfica)
- ReportLab (para geração de PDFs)
- Matplotlib (para geração de gráficos)
- Pandas (para manipulação de dados)

### Passos

1. Clone este repositório:
   ```bash
   git clone https://github.com/pablovvoliveira/controle-financeiro-extensao.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd controle-financeiro-extensao
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o projeto:
   ```bash
   python main.py
   ```

## Como Criar um Executável

Para facilitar a distribuição do seu projeto, você pode criar um executável que pode ser executado em qualquer computador com Windows, mesmo que ele não tenha Python instalado. Veja como:

### Passos

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Navegue até o diretório do seu projeto e rode o seguinte comando para criar o executável:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
   - `--onefile`: Gera um único arquivo executável.
   - `--windowed`: Evita que a janela do terminal seja exibida ao rodar o executável (útil para programas com interface gráfica).

3. Após o processo de construção, o executável estará disponível na pasta `dist` dentro do diretório do seu projeto.

4. Distribua o arquivo executável gerado (`main.exe` no Windows) para que outros possam usar seu programa sem precisar instalar Python.

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicia a interface gráfica.
- `ganhos.py`: Módulo para registrar e calcular os ganhos.
- `despesas.py`: Módulo para registrar e calcular as despesas.
- `relatorios.py`: Módulo responsável pela geração do relatório financeiro consolidado.
- `analise_dados.py`: Módulo para gerar o PDF com a análise de dados.

## Licença

Este projeto é licenciado sob a MIT License.
