# Sistema de Monitoramento de Planilhas

## Objetivo
Automatizar a verificação de preenchimento diário de planilhas operacionais armazenadas no SharePoint.

O sistema verifica se houve alteração real no conteúdo das abas monitoradas e envia alerta no Microsoft Teams caso não exista atualização.

---

# Tecnologias Utilizadas

- Python
- pandas
- hashlib
- requests
- SharePoint
- OneDrive
- Microsoft Teams Webhook

---

# Funcionamento

O sistema:

1. Acessa a planilha sincronizada pelo OneDrive;
2. Lê abas específicas;
3. Converte o conteúdo em HASH;
4. Compara com o HASH da execução anterior;
5. Detecta se houve alteração;
6. Envia alerta no Teams caso não exista atualização.

---

# Estrutura

```text
Suporte - Documentos/
│
├── telemetria.py
├── monitoramento_18h.bat
├── hashes/
│
├── TELEMETRIA 2025.xlsx
│
├── Frota/
│   ├── pneus.py
│   ├── Movimentação Pneus Entrada Saída Transmoor.xlsx
│   ├── hashes/
