import pandas as pd
import numpy as np

def processar_dados_techlog(caminho_entrada, caminho_saida=None):
    """
    Pipeline completo de ETL para a TechLogistics.
    Carrega dados brutos, remove duplicadas, imputa nulos
    por grupo e gera métricas de negócio.
    """
    print("🔄 Carregando dados brutos da TechLogistics...")
    df = pd.read_csv(caminho_entrada)
    
    # 1. Remover registros duplicados
    df = df.drop_duplicates()

    # 2. Imputação inteligente de 'PesoPacote' por 'TipoProduto' (mediana)
    df['PesoPacote'] = df['PesoPacote'].fillna(
        df.groupby('TipoProduto')['PesoPacote'].transform('median')
    )
    
    # 3. Imputação inteligente de 'CidadeDestino' por 'Regiao' (moda)
    df['CidadeDestino'] = df['CidadeDestino'].fillna(
        df.groupby('Regiao')['CidadeDestino'].transform(
            lambda x: x.mode().iloc[0] if not x.mode().empty else 'Desconhecido'
        )
    )

    # 4. Tratamento de datas e texto
    df['DataPostagem'] = pd.to_datetime(df['DataPostagem'])
    df['DataEntrega'] = pd.to_datetime(df['DataEntrega'])
    df['CidadeDestino'] = df['CidadeDestino'].str.upper().str.strip()

    # 5. Métricas de negócio
    df['DiasEmTransito'] = (df['DataEntrega'] - df['DataPostagem']).dt.days
    df['Atrasado'] = (df['DiasEmTransito'] > 5).astype(int)

    # 6. Salvar arquivo tratado (opcional)
    if caminho_saida:
        df.to_csv(caminho_saida, index=False)
        print(f"✅ Arquivo limpo salvo em: '{caminho_saida}'")

    return df

# --- Execução Principal ---
if __name__ == "__main__":
    df_limpo = processar_dados_techlog('techlog_bruto.csv', 'techlog_tratado.csv')
    print("\n--- Primeiras linhas dos dados limpos ---")
    print(df_limpo.head())

