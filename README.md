# Microsserviço de Aluguel - SCB

Este microsserviço faz parte do Sistema de Controle de Bicicletário (SCB) e é responsável pelas operações relacionadas ao **aluguel de bicicletas**.

## Funcionalidades

- POST /aluguel – Realiza o aluguel de uma bicicleta
- (em breve) POST /devolucao – Devolve uma bicicleta ao sistema
- (em breve) POST /cobranca-atrasada – Cobra taxas extras por atraso

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