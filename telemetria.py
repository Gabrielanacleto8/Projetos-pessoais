import pandas as pd
import hashlib
import os
import requests

# WEBHOOK DO TEAMS
webhook_url = "nao exebido por seguranca"
# CAMINHO COMPLETO DA PLANILHA
arquivo_excel = r"C:\Users\gabriel.farias\TRANSPORTE RODOVIARIO UPTMOOR LTDA\Suporte - Documentos\TELEMETRIA 2025.xlsx"

# ABAS QUE SERÃO MONITORADAS
abas = [
    "Subida de serra"
]

# CAMINHO DA PASTA DO SCRIPT
pasta_script = r"C:\Users\gabriel.farias\TRANSPORTE RODOVIARIO UPTMOOR LTDA\Suporte - Documentos"

# PASTA HASHES
pasta_hashes = os.path.join(
    pasta_script,
    "hashes"
)

os.makedirs(pasta_hashes, exist_ok=True)

# ALERTAS
alertas = []

# PERCORRE ABAS
for aba in abas:

    try:

        
        df = pd.read_excel(
            arquivo_excel,
            sheet_name=aba
        )

        
        conteudo = df.to_string()

       
        hash_atual = hashlib.md5(
            conteudo.encode()
        ).hexdigest()

       
        # NOME PLANILHA
        nome_planilha = os.path.splitext(
            os.path.basename(arquivo_excel)
        )[0]

        # ARQUIVO HASH
       
        arquivo_hash = os.path.join(
            pasta_hashes,
            f"hash_{nome_planilha}_{aba}.txt"
        )

        
        # COMPARA HASH
        if os.path.exists(arquivo_hash):

            with open(arquivo_hash, "r") as f:
                hash_antigo = f.read()

            if hash_atual == hash_antigo:

                mensagem = (
                    f"⚠ ALERTA\n\n"
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

        # SALVA HASH
        with open(arquivo_hash, "w") as f:
            f.write(hash_atual)

    except Exception as erro:

        mensagem_erro = (
            f"❌ ERRO\n\n"
            f"Planilha: {arquivo_excel}\n"
            f"Aba: {aba}\n"
            f"Erro: {erro}"
        )

        print(mensagem_erro)

        alertas.append(mensagem_erro)

# ENVIA TEAMS
if alertas:

    payload = {
        "text": "\n\n".join(alertas)
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
