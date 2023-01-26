ano_inicio = 2012
ano_termino = 2021

arquivos_cvm = ['dfp_cia_aberta_DRE_con_{}.csv','dfp_cia_aberta_DFC_MI_con_{}.csv',
                'dfp_cia_aberta_BPP_con_{}.csv','dfp_cia_aberta_BPA_con_{}.csv',
                'dfp_cia_aberta_DRA_con_{}.csv', 'dfp_cia_aberta_DVA_con_{}.csv']
lista_anos = []
while ano_inicio <= ano_termino:
    lista_anos.append(ano_inicio)
    ano_inicio += 1
google_cloud_link = 'https://storage.googleapis.com/demonstrativosfinanceiros/{}'
links_gcloud_sem_data = []
links_gcloud = []
for arquivo in arquivos_cvm:
    links_gcloud_sem_data.append(google_cloud_link.format(arquivo))

for link in links_gcloud_sem_data:
    for ano in lista_anos:
        links_gcloud.append(link.format(ano))

##-------------------------##

import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_rows', 400)


def gerar_dfp(demonstrativo, ano_analise, empresa):
    link_dfp = [sentence for sentence in links_gcloud if all(w in sentence for w in [demonstrativo, str(ano_analise)])][
        0]
    dfp_dados_brutos = pd.read_csv(link_dfp, encoding='ISO-8859-1', sep=';')

    ultimo = dfp_dados_brutos.loc[dfp_dados_brutos['ORDEM_EXERC'] == 'ÚLTIMO']
    penultimo = dfp_dados_brutos.loc[dfp_dados_brutos['ORDEM_EXERC'] == 'PENÚLTIMO']

    ultimo_ano = ultimo['DT_FIM_EXERC'][1][:4]
    penultimo_ano = penultimo['DT_FIM_EXERC'][0][:4]

    ultimo = ultimo[['DENOM_CIA', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']]
    ultimo.columns = ['DENOM_CIA', 'CD_CONTA', 'DS_CONTA', ultimo_ano]

    penultimo = penultimo[['DENOM_CIA', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']]
    penultimo.columns = ['DENOM_CIA', 'CD_CONTA', 'DS_CONTA', penultimo_ano]

    dfp_geral = pd.merge(penultimo, ultimo)
    dfp_geral = dfp_geral.loc[dfp_geral['DENOM_CIA'] == empresa]

    return dfp_geral

def relatorio_2anos_empresa(dfp, ano, empresa):
    dfp_gerado = gerar_dfp(dfp, ano, empresa)
    return dfp_gerado

def relatorio_4anos_empresa(dfp, ano, empresa):
    dfp_gerado1 = gerar_dfp(dfp, ano-2, empresa)
    dfp_gerado = gerar_dfp(dfp, ano, empresa)
    dfp_geral = pd.merge(dfp_gerado1, dfp_gerado)
    return dfp_geral

#Listar contas
def listar_contas(demonstrativo):
    for conta in demonstrativo['DS_CONTA'].unique():
        print(conta)

#retornar dados conta
def retornar_conta(demonstrativo, conta):
    return demonstrativo.loc[demonstrativo['DS_CONTA'] == conta]

#retornar dados conta
def retornar_valores(demonstrativo, conta):
    a = demonstrativo.loc[demonstrativo['DS_CONTA'] == conta]
    return a.values[0][3:]

#Retornar Tabela com 2 contas
def retornar_tabela(dfc1, conta1, dfc2, conta2):
    a = retornar_conta(dfc1, conta1)
    b = retornar_conta(dfc2, conta2)
    c = a.append(b)
    return c

#Listar total de empresas listadas por Ano
def listar_empresas_ano(ano):
    link_dfp = [sentence for sentence in links_gcloud if all(w in sentence for w in ['BPA', str(ano)])][0]
    dfp_dados_brutos = pd.read_csv(link_dfp, encoding='ISO-8859-1', sep=';')
    for empresa in dfp_dados_brutos['DENOM_CIA'].unique():
        print(empresa)