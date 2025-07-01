# Microsserviço de Aluguel - SCB

Este microsserviço é responsável pela **gestão de ciclistas e seus cartões de crédito, funcionários e operações de aluguel e devolução de bicicletas** no Sistema de Controle de Bicicletário (SCB).

## Arquitetura

Este projeto segue os princípios da **Clean Architecture**, com uma separação clara de responsabilidades em diferentes camadas:

- `domain/` – modelos de entidades e regras de negócio centrais
- `use_cases/` – casos de uso que orquestram regras e validações
- `infra/repositories/` – implementação de repositórios de persistência (ex: fake, banco real)
- `api/` – camada de interface REST com FastAPI
- `dependencies/` – configuração de injeções para os casos de uso
- `tests/` – testes automatizados para cada funcionalidade

## Funcionalidades

### Gestão de Ciclistas

- `POST /ciclista` — Cadastrar um ciclista com seus dados e meio de pagamento
- `GET /ciclista/{idCiclista}` — Consultar dados de um ciclista
- `PUT /ciclista/{idCiclista}` — Alterar dados do ciclista
- `POST /ciclista/{idCiclista}/ativar` — Ativar conta de ciclista
- `GET /ciclista/{idCiclista}/permiteAluguel` — Verifica se o ciclista pode alugar
- `GET /ciclista/{idCiclista}/bicicletaAlugada` — Ver bicicleta atualmente alugada (se houver)
- `GET /ciclista/existeEmail/{email}` — Verifica se um email já está em uso

### Gestão de Funcionários

- `POST /funcionario` — Cadastrar funcionário
- `GET /funcionario` — Listar todos os funcionários
- `GET /funcionario/{idFuncionario}` — Obter dados de um funcionário
- `PUT /funcionario/{idFuncionario}` — Atualizar dados do funcionário
- `DELETE /funcionario/{idFuncionario}` — Remover funcionário

### Cartão de Crédito

- `GET /cartaoDeCredito/{idCiclista}` — Obter dados do cartão de crédito do ciclista
- `PUT /cartaoDeCredito/{idCiclista}` — Atualizar cartão de crédito

### Aluguel e Devolução

- `POST /aluguel` — Realizar aluguel de bicicleta (UC03)
- `POST /devolucao` — Realizar devolução automática (UC04)

### Utilitários

- `GET /restaurarBanco` — Restaurar os dados iniciais do microsserviço para testes ou reset

## Como conectar via ssh no windows

- ssh -i "C:\Users\guite\OneDrive\Documentos\Faculdade\8o Período\ES2 - Paulo\scb-api\scb-api-keys.pem" ubuntu@15.228.164.101

## Como executar localmente

1. Ativar o ambiente virtual com: `venv\Scripts\activate`
2. Rodar com: `uvicorn app.main:app --reload --port 8000 `

**Usando Python diretamente com Docker:**

1. Construa a imagem com: `docker build -t scb-aluguel .`
2. Execute o container com: `docker run -p 8000:8000 scb-aluguel`

## Acesso à API

- API Base: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

- API Base na EC2: http://15.228.249.205:8000/
- Documentação Swagger na EC2: http://15.228.249.205:8000/

## Autor responsável

- Guilherme Freire – responsável pelo microsserviço de **Aluguel**
