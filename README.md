<SKIPPED_HTML_EDIT_MODE></SKIPPED_HTML_EDIT_MODE>
# 📊 PicMoney Analytics Platform

**Plataforma de análise de dados para gestão estratégica de cupons fiscais**

## 🚀 Visão Geral

A PicMoney Analytics é uma solução completa para visualização e análise de dados de cupons fiscais, fornecendo dashboards estratégicos para executivos C-Level (CFO, CEO, CTO) com KPIs específicos para cada função.

## 🛠️ Tecnologias Principais

### Backend
- **Java 17** com **Spring Boot 3.x**
- **MySQL 8.0** (banco de dados principal)
- **Spring Data JPA** (persistência)
- **Spring Web** (API REST)

### Frontend
- **React 18** com TypeScript
- **Chart.js** e **React ChartJS 2** (visualizações)
- **Axios** (chamadas HTTP)
- **Tailwind CSS** (estilização)

### Processamento de Dados
- **Python 3.11**
- **Pandas** (manipulação de dados)
- **Faker** (geração de dados simulados)
- **Requests** (integração com backend)

## 📂 Estrutura do Projeto

O projeto está organizado em três módulos principais:

```
picmoney-analytics/
├── backend/          # Aplicação Spring Boot
├── frontend/         # Aplicação React
└── data-processing/  # Scripts Python para EDA e geração de dados
```

## 🏁 Como Começar

### Pré-requisitos

- Java 17+
- Node.js 18+
- Python 3.11+
- MySQL 8.0+
- Docker (opcional)

### Configuração Inicial

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/picmoney-analytics.git
   cd picmoney-analytics
   ```

2. **Configurar o banco de dados:**
   - Criar database `picmoney_dev`
   - Executar o script SQL em `backend/src/main/resources/schema.sql`

3. **Configurar variáveis de ambiente:**
   - Copiar `.env.example` para `.env` em cada módulo
   - Preencher com suas credenciais e configurações

### Executando Localmente

#### Backend

```bash
cd backend
./mvnw spring-boot:run  # ou use sua IDE favorita
```

Executará na porta 8080 com perfil `dev`.

#### Frontend

```bash
cd frontend
npm install
npm start
```

Executará na porta 3000.

#### Processamento de Dados

```bash
cd data-processing
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows
pip install -r requirements.txt
python scripts/data_generator/generator.py
```

## 🌐 Ambientes

O sistema suporta três ambientes configurados:

| Ambiente     | Backend Profile | Frontend Env | Banco de Dados      |
|--------------|-----------------|--------------|---------------------|
| Development  | dev             | development  | picmoney_dev        |
| Staging      | stage           | staging      | picmoney_stage      |
| Production   | prod            | production   | picmoney_prod       |

## 🐳 Execução com Docker

Para executar todo o ambiente localmente com containers:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Isso criará:
- Container MySQL na porta 3306
- Container Spring Boot na porta 8080
- Container React na porta 3000
- Container Python para geração de dados

## 🔧 Principais Endpoints da API

| Endpoint                   | Método | Descrição                           |
|----------------------------|--------|-------------------------------------|
| `/api/coupons`             | GET    | Lista todos os cupons               |
| `/api/coupons/kpi/cfo/*`   | GET    | KPIs para CFO                       |
| `/api/coupons/kpi/ceo/*`   | GET    | KPIs para CEO                       |
| `/api/coupons/kpi/cto/*`   | GET    | KPIs para CTO                       |
| `/api/alerts`              | GET    | Alertas detectados                  |

## 📊 KPIs Implementados

### CFO (Financeiro)
- Receita Total
- Ticket Médio
- Custo do Cupom
- ROI dos Cupons
- Margem por Transação

### CEO (Estratégico)
- Total de Cupons Capturados
- Usuários Únicos
- Engajamento por Tipo
- Lojas Mais Populares
- Mapa de Atividades

### CTO (Tecnológico)
- Latência de Atualização
- Disponibilidade do Sistema
- Erros de Captura
- Performance Geolocalização

## 🤖 Geração de Dados

O módulo Python inclui:
- Script de EDA (Análise Exploratória)
- Gerador de dados simulados em tempo real
- Detecção de anomalias automática

Execute periodicamente para simular um ambiente de produção:

```bash
python scripts/data_generator/generator.py --interval 30
```

## 🧪 Testes

Para executar testes em cada módulo:

```bash
# Backend
cd backend && ./mvnw test

# Frontend
cd frontend && npm test

# Python
cd data-processing && pytest
```

## 📌 Próximos Passos

1. Implementar autenticação JWT
2. Adicionar previsões usando ML
3. Melhorar dashboards geoespaciais
4. Implementar exportação de relatórios

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Equipe PicMoney Analytics**  
📧 contato@picmoney.com  
🌐 [picmoney.com](https://www.picmoney.com)
