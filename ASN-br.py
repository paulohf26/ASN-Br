#!/usr/bin/env python3

import pandas as pd
import ipaddress
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

asnBase="nicbr-asn-blk-latest.txt"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

def carregar_asn_prefixos(caminho):
    registros = []

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split("|")

            asn = partes[0]
            nome = partes[1]
            cnpj = partes[2]

            prefixos_texto = partes[3:]
            # Converter prefixos para objetos ipaddress
            prefixos_v4 = []
            prefixos_v6 = []
            qpv4=0
            qpv6=0
            qipv4=0
            qpv6_64=0
            for p in prefixos_texto:
                ip = ipaddress.ip_network(p, strict=False)
                try:
                    if (ip.version == 4):
                        prefixos_v4.append(ip)
                        qpv4=qpv4+1
                        qipv4=qipv4+ip.num_addresses
                    else:
                        prefixos_v6.append(ip)
                        d=64 - ip.prefixlen
                        #print(2**d)
                        qpv6_64=qpv6_64+(2**(64 - ip.prefixlen))
                        qpv6=qpv6+1
                except ValueError:
                    print(f"Prefixo inválido ignorado: {p}")

            registros.append({
                "asn": asn,
                "nome": nome,
                "cnpj": cnpj,
                "prefixos_texto": prefixos_texto,
                "prefixos_v4": prefixos_v4,
                "Quantidade_Prefixos_v4": qpv4,
                "Quantidade_Enderecos_v4":qipv4,
                "prefixos_v6": prefixos_v6,
                "Quantiadde_Prefixos_v6":qpv6,
                "Quantidade_Prefixos_v6_64":qpv6_64
            })

    return pd.DataFrame(registros)


def plot1(dfrm):
    plt.figure(figsize=(10, 5))
    # O eixo Y mostra a contagem (valor), e o eixo X é apenas o índice/ranking do ASN
    plt.scatter(dfrm.index, dfrm['Quantidade_Prefixos_v4'], s=5, alpha=0.6, color='skyblue')

    plt.yscale('log') # Usa escala logarítmica para melhor visualização da dispersão
    plt.title('Dispersão da Quantidade de Endereços IPv4 (Base Total)', fontsize=14)
    plt.xlabel('ASN Index (9000 ASNs)', fontsize=12)
    plt.ylabel('Contagem de Endereços IPv4', fontsize=12)
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.tight_layout()
        #plt.show()
    plt.savefig('meu_grafico_plot1.svg',dpi=600,bbox_inches='tight')
    

def plot2(dfrm):
    
    df_top20_v4 = dfrm.nlargest(20, 'Quantidade_Enderecos_v4')
    df_top20_v4['Quantidade_Enderecos_v4'] = df_top20_v4['Quantidade_Enderecos_v4'] / 1000000 
    df_top20_v4_ordenado = df_top20_v4.sort_values(by='Quantidade_Enderecos_v4',ascending=False)
    df_top20_v4_ordenado['LabelGraph'] = df_top20_v4_ordenado['asn'] + '-' + df_top20_v4_ordenado['nome']
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(
            x='LabelGraph',
            y='Quantidade_Enderecos_v4',
            data=df_top20_v4_ordenado,
            palette='viridis' # Esquema de cores
    )

    plt.title('Top 20 ASNs por Contagem de Endereços IPv4\nMilhões', fontsize=16)
    plt.xlabel('ASN', fontsize=10)
    plt.ylabel('Contagem de Endereços IPv4', fontsize=12)
    plt.xticks(rotation=45, ha='right') # Rotaciona rótulos para melhor leitura

    for i,valor in enumerate(df_top20_v4_ordenado['Quantidade_Enderecos_v4']):
        plt.text(i,valor+1,"{:.2f}".format(valor),ha='center',rotation=90,va='bottom',size=8)

    plt.tight_layout()
    plt.savefig('meu_grafico_plot2.svg',dpi=600,bbox_inches='tight')

def plot3(dfrm):
    
    df_top20_v6 = dfrm.nlargest(20, 'Quantidade_Prefixos_v6_64')
    df_top20_v6['Quantidade_Prefixos_v6_64'] = df_top20_v6['Quantidade_Prefixos_v6_64'] / 1000000 
    df_top20_v6_ordenado = df_top20_v6.sort_values(by='Quantidade_Prefixos_v6_64',ascending=False)
    df_top20_v6_ordenado['LabelGraph'] = df_top20_v6_ordenado['asn'] + '-' + df_top20_v6_ordenado['nome']
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(
            x='LabelGraph',
            y='Quantidade_Prefixos_v6_64',
            data=df_top20_v6_ordenado,
            palette='viridis' # Esquema de cores
    )

    plt.title('Top 20 ASNs por Contagem de Prefixos IPv6 /64\nMilhões', fontsize=16)
    plt.xlabel('ASN', fontsize=10)
    plt.ylabel('Contagem de Prefixos v6 /64', fontsize=12)
    plt.xticks(rotation=45, ha='right') # Rotaciona rótulos para melhor leitura

    for i,valor in enumerate(df_top20_v6_ordenado['Quantidade_Prefixos_v6_64']):
        plt.text(i,valor+1,"{:.2f}".format(valor),ha='center',rotation=90,va='bottom',size=8)

    plt.tight_layout()
    plt.savefig('meu_grafico_plot3.svg',dpi=600,bbox_inches='tight')


if __name__ == "__main__":
    print("Iniciando execução...")


    df = carregar_asn_prefixos(asnBase)
    #print(df)
    plot3(df)

    print("Finalizando execução.")
