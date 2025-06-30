# Guia de Integração com Outros Microsserviços

Este documento descreve como integrar o microsserviço de Aluguel com os outros microsserviços do Sistema de Controle de Bicicletário.

## Visão Geral

O microsserviço de Aluguel precisa se comunicar com:

1. **Microsserviço de Equipamento** - Para gerenciar bicicletas e trancas
2. **Microsserviço Externo** - Para cobranças, emails e validação de cartões

## Arquitetura de Integração

### Repositórios de Interface

Criamos interfaces abstratas para facilitar a integração:

- `ExternoRepository` - Para serviços externos
- `EquipamentoRepository` - Para microsserviço de equipamento

## Configuração

### Variáveis de Ambiente

```bash
# URLs dos microsserviços
EXTERNAL_BASE_URL=http://localhost:8001
EQUIPMENT_BASE_URL=http://localhost:8002

# Configurações de timeout e retry
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1
```

### Alternando entre Fake e Real

Para alternar entre implementações fake e reais, modifique o arquivo `app/infra/repositories/__init__.py`:

```python
# Para desenvolvimento (usando fake)
from .fake_external_repository import FakeExternalRepository, FakeEquipmentRepository
fake_external_repository = FakeExternalRepository()
fake_equipment_repository = FakeEquipmentRepository()

# Para produção (usando real)
from .real_external_repository import RealExternalRepository, RealEquipmentRepository
fake_external_repository = RealExternalRepository()
fake_equipment_repository = RealEquipmentRepository()
```

## Endpoints que Precisam de Integração

### 1. POST /aluguel

**Integrações necessárias:**

- **Equipamento**: Validar tranca, obter bicicleta, alterar status
- **Externo**: Realizar cobrança, enviar email

**Fluxo:**

1. Validar se tranca existe e está ocupada
2. Obter bicicleta da tranca
3. Validar status da bicicleta
4. Realizar cobrança
5. Alterar status da bicicleta para "EM_USO"
6. Alterar status da tranca para "LIVRE"
7. Enviar email de confirmação

### 2. POST /devolucao

**Integrações necessárias:**

- **Equipamento**: Alterar status da bicicleta e tranca
- **Externo**: Enviar email, incluir cobrança extra na fila

**Fluxo:**

1. Calcular valor extra se necessário
2. Alterar status da bicicleta para "DISPONÍVEL"
3. Alterar status da tranca para "OCUPADA"
4. Enviar email de confirmação
5. Incluir cobrança extra na fila (se houver)

### 3. GET /ciclista/{idCiclista}/bicicletaAlugada

**Integrações necessárias:**

- **Equipamento**: Obter dados da bicicleta

### 4. POST /ciclista

**Integrações necessárias:**

- **Externo**: Validar cartão de crédito
