# Microsserviço de Aluguel - SCB

Este microsserviço é responsável pela **gestão de ciclistas, funcionários, cartões de crédito e operações de aluguel e devolução de bicicletas** no Sistema de Controle de Bicicletário (SCB).

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
- `PUT /funcionario/{idFuncionario}` — Atualizar dados
- `DELETE /funcionario/{idFuncionario}` — Remover funcionário

### Cartão de Crédito

- `GET /cartaoDeCredito/{idCiclista}` — Obter dados do cartão de crédito do ciclista
- `PUT /cartaoDeCredito/{idCiclista}` — Atualizar cartão de crédito

### Aluguel e Devolução

- `POST /aluguel` — Realizar aluguel de bicicleta (UC03)
- `POST /devolucao` — Realizar devolução automática (UC04)

### Utilitários

- `GET /restaurarBanco` — Restaurar os dados iniciais do microsserviço para testes ou reset


## Como executar localmente

**Usando Python diretamente com Docker:**

1. Construa a imagem com: `docker build -t scb-aluguel .`
2. Execute o container com: `docker run -p 8000:8000 scb-aluguel`

## Acesso à API

- API Base: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

> Se estiver rodando via EC2, substitua `localhost` pelo IP público da sua instância.

## Autor responsável

- Guilherme Freire – responsável pelo microsserviço de **Aluguel**