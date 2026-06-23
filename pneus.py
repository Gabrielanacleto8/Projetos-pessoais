import pandas as pd
import hashlib
import os
import requests


# WEBHOOK DO TEAMS
webhook_url = "não exibido por segurança"

# NOME DA PLANILHA
arquivo_excel = "Movimentação Pneus Entrada Saída Transmoor.xlsx"

# ABAS QUE SERÃO MONITORADAS
abas = [
    "MOVIMENTAÇÕES",
    "PLACAS"
]

# CRIA PASTA DOS HASHES
os.makedirs("hashes", exist_ok=True)

# LISTA DE ALERTAS
alertas = []

# PERCORRE AS ABAS
for aba in abas:

    try:
        # LÊ A ABA
        df = pd.read_excel(
            arquivo_excel,
            sheet_name=aba
        )
      
        # CONVERTE CONTEÚDO EM TEXTO
        conteudo = df.to_string()

        # GERA HASH
        hash_atual = hashlib.md5(
            conteudo.encode()
        ).hexdigest()

        # NOME DO HASH
        nome_planilha = os.path.splitext(
            arquivo_excel
        )[0]

        arquivo_hash = (
            f"hashes/hash_{nome_planilha}_{aba}.txt"
        )

        # VERIFICA HASH ANTIGO
        if os.path.exists(arquivo_hash):

            with open(arquivo_hash, "r") as f:
                hash_antigo = f.read()

            # COMPARA HASH
            if hash_atual == hash_antigo:

                mensagem = (
                    f"⚠ ALERTA:\n"
                    f"Planilha: {nome_planilha}\n"
                    f"Aba: {aba}\n"
                    f"Status: Sem alterações."
                )

                print(mensagem)

                alertas.append(mensagem)

            else:

                print(
                    f"✅ {nome_planilha} -> "
                    f"Aba '{aba}' foi alterada."
                )

        else:

            print(
                f"🟡 Primeira execução: "
                f"{nome_planilha} -> "
                f"Aba '{aba}'."
            )

        # SALVA HASH NOVO
        with open(arquivo_hash, "w") as f:
            f.write(hash_atual)

    except Exception as erro:

        mensagem_erro = (
            f"❌ ERRO\n"
            f"Planilha: {arquivo_excel}\n"
            f"Aba: {aba}\n"
            f"Erro: {erro}"
        )

        print(mensagem_erro)

        alertas.append(mensagem_erro)

# ENVIA ALERTA TEAMS
if alertas:

    texto_alerta = "\n\n".join(alertas)

    payload = {
        "text": texto_alerta
    }

    requests.post(
        webhook_url,
        json=payload
    )

    print("📨 Alerta enviado ao Teams.")

else:

    print(
        "✅ Todas as abas tiveram alterações."
    )
