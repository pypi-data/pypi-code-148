from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime as dt

import pandas as pd


def encontra_periodo(cod_turma):
    if cod_turma.__contains__('EAD'):
        return 'EAD'
    if not cod_turma.__contains__('-'):
        return ''

    cod_turma = cod_turma.split('-')[1].strip()
    periodo = ''
    for ch in cod_turma:
        if ch in '0123456789':
            periodo += ch
        else:
            break
    return periodo


def encontra_cr(turma):
    if turma.__contains__('EAD') and not (turma.__contains__('LIBRAS') or turma.__contains__('LEA')):
        return 'EAD'
    elif not turma.__contains__('-'):
        return ''
    else:
        if turma.__contains__('LEA') or turma.__contains__('LIBRAS'):
            sigla = turma.split('-')[0].strip()
            validador = sigla
        else:
            turno = turma.split('-')[2].strip()
            sigla = turma.split('-')[0].strip()
            validador = sigla + ' ' + turno
        return dict_sigla_cr.get(validador, '')


def encontra_curso(cod_turma):
    cod_turma = cod_turma.split('-')[0].strip()
    curso = dict_sigla_curso.get(cod_turma, '')
    return curso


def encontra_escola(cod_turma):
    cod_turma = cod_turma.split('-')[0].strip()
    escola = dict_sigla_escola.get(cod_turma, '')
    return escola


def ajusta_usuario(usuario):
    email = usuario
    print(email)
    return email


dict_sigla_cr = {
    'CADI M': '2239',
    'CADM M': '2028', 'CADM N': '2029',
    'CAGR M': '2078', 'CAGR N': '2079',
    'CAMM M': '1031863',
    'CAUR M': '2244', 'CAUR N': '2303',
    'CBAV N': '1031087',
    'CBCS N': '1031080',
    'CBED N': '2311', 'CBED M': '2212',
    'CBHI M': '1031078', 'CBHI N': '1031079',
    'CBIT M': '2074', 'CBJD M': '1031092',
    'CBND M': '1031461', 'CBND N': '1031467',
    'CBNI M': '1031462', 'CBNI N': '1031468',
    'CBSI N': '2250',
    'CCAU M': '1031089', 'CCAU N': '1031090',
    'CCBI M': '2360',
    'CCBS N': '2287',
    'CCCO M': '2245', 'CCCO N': '2345',
    'CCOT M': '2229', 'CCOT N': '2230',
    'CCPP M': '2225', 'CCPP N': '2232',
    'CDDG T': '2342', 'CDDG M': '2342',
    'CDES M': '2271', 'CDES N': '2272',
    'CDIR M': '2022', 'CDIR N': '2023',
    'CEAM M': '2246', 'CEAM N': '2346',
    'CEBI M': '2222', 'CEBI N': '2223',
    'CECA M': '2158', 'CECA N': '2159',
    'CECO M': '2036', 'CECO N': '2035',
    'CECP M': '2248', 'CECP N': '2348',
    'CECV M': '2243', 'CECV N': '2343',
    'CEDF M': '2206', 'CEDF N': '2312',
    'CEEE M': '2355', 'CEEE N': '2359',
    'CEEL M': '2140', 'CEET N': '2351',
    'CEFB M': '1031582', 'CEFB N': '1031583',
    'CEMC M': '2252', 'CEMC N': '2352',
    'CEMT M': '2269', 'CEMT N': '2270',
    'CENF M': '2069',
    'CEPD M': '2241', 'CEPD N': '2341',
    'CESF M': '2263', 'CESF N': '1031864',
    'CFAR M': '2167',
    'CFIL M': '2304', 'CFIS M': '2066',
    'CGAS M': '2072', 'CGAS N': '1060',
    'CHIS M': '2314', 'CHIS N': '2214',
    'CIBP I': '2293',
    'CICH I': '2275',
    'CIS I': '2295',
    'CJDI M': '2344', 'CJDI N': '2145',
    'CJDV N': '1031460',
    'CJOR M': '2236', 'CJOR N': '2237',
    'CLBI M': '1031181', 'CLBI N': '2268',
    'CLFL M': '2202', 'CLFL N': '2302',
    'CLFS M': '1031466', 'CLFS N': '2349',
    'CLPI M': '2301', 'CLPI N': '2203',
    'CMAT M': '1031465', 'CMAT N': '2249',
    'CMED I': '2062',
    'CMKT M': '2129', 'CMKT N': '2128',
    'CMPM N': '2283',
    'CMUS N': '2215',
    'CMVT M': '2076',
    'CNUT M': '2070',
    'CODO I': '2064',
    'CPED M': '2201', 'CPED N': '2210',
    'CPSI M': '2063', 'CPSI N': '2071',
    'CQUE M': '2353', 'CQUE N': '2253',
    'CQUI M': '2121', 'CQUI N': '2350',
    'CRPU M': '2238', 'CRPU N': '1031183',
    'CSOC N': '2221',
    'CSSC': '2120', 'CSSC M': '2120', 'CSSC N': '2220',
    'CTEA N': '2308',
    'CTEO M': '2319', 'CTEO N': '2219',
    'CTSI N': '2289',
    'GBF M': '114165', 'GFL M': '2603',
    'LAD M': '115', 'LAD N': '2501',
    'LCC N': '111',
    'LDI': '2518', 'LDI M': '2518', 'LDI N': '2502',
    'LES N': '111148',
    'LFS M': '111154',
    'LME I': '2530',
    'LPO N': '119',
    'LPS M': '121', 'LPS N': '124',
    'LTO M': '114',
    'TAD N': '2402',
    'TAG M': '2420', 'TAG N': '2424',
    'TCC N': '2429',
    'TDI M': '2430', 'TDI N': '2431',
    'TGI N': '112178',
    'TMV M': '2410', 'TMV N': '112152',
    'TPO N': '2422',
    'TPS': '2423', 'TPS N': '2423', 'TPS M': '112153',
    # Multicom
    'CURIE M': '2304',
    'ELIANE BRUM M': '2236', 'ELIANE BRUM N': '2237',
    'MARCELLO SERPA M': '2225',
    'MARGARIDA KUNSCH M': '2238',
    'PIAGET N': '2214',
    # Eixos
    'ENGENHARIA ADA M': '2248',
    'ENGENHARIA AVILLA N': '2343',
    'ENGENHARIA BABBAGE BOLTZMANN M': '2222',
    'ENGENHARIA BELL M': '2222',
    'ENGENHARIA BENZ M': '2269',
    'ENGENHARIA BERRY N': '2348',
    'ENGENHARIA BROGLIE M': '2252',
    'ENGENHARIA CLARKE M': '2269',
    'ENGENHARIA EASLEY N': '2352',
    'ENGENHARIA FAHRENHEIT N': '2343',
    'ENGENHARIA FEYNMAN M': '2243',
    'ENGENHARIA GOODALL N': '2343',
    'ENGENHARIA GUTEMBERG M': '2243',
    'ENGENHARIA HAMILTON BURNELL M':'2252',
    'ENGENHARIA HYPATIA M': '2353',
    'ENGENHARIA JEMISON M': '2252',
    'ENGENHARIA NICOLELIS N': '2348',
    'ENGENHARIA RUTHERFORD M': '2353',
    'ENGENHARIA SIEMENS M': '2241',
    'ENGENHARIA TELFORD M': '2243',
    # LEA
    'LEA': '2203',
    'LDN': '121',
    'TLD': '2423'
}

dict_sigla_curso = {
    'CADI': 'Administração - Internacional',
    'CADM': 'Administração',
    'CAGR': 'Agronomia',
    'CAMM': 'Administração - Master',
    'CAUR': 'Arquitetura e Urbanismo',
    'CBAV': 'Bacharelado em Artes Visuais',
    'CBCS': 'Bacharelado em Ciências Sociais',
    'CBED': 'Bacharelado em Educação Física',
    'CBHI': 'Bacharelado em História ',
    'CBIT': 'Biotecnologia',
    'CBJD': 'Bacharelado em Jogos Digitais',
    'CBND': 'Bacharelado em Negócios Digitais',
    'CBNI': 'Bacharelado em Negócios Internacionais',
    'CBSI': 'Sistemas de Informação',
    'CCAU': 'Cinema e Audiovisual',
    'CCBI': 'Ciências Biológicas - Bacharelado',
    'CCBS': 'Cibersegurança',
    'CCCO': 'Ciência da Computação',
    'CCOT': 'Ciências Contábeis',
    'CCPP': 'Comunicação Social - Hab. Publicidade e Propaganda',
    'CDDG': 'Design Digital',
    'CDES': 'Design',
    'CDIR': 'Direito',
    'CEAM': 'Engenharia Ambiental',
    'CEBI': 'Engenharia Biomédica',
    'CECA': 'Engenharia de Controle e Automação',
    'CECO': 'Ciências Econômicas',
    'CECP': 'Engenharia de Computação',
    'CECV': 'Engenharia Civil',
    'CEDF': 'Licenciatura em Educação Física',
    'CEEE': 'Engenharia Elétrica - Eixos: Telecomunicações Eletrônica ou Sistema de Potência e Energia',
    'CEEL': 'Engenharia Eletrônica',
    'CEET': 'Engenharia Elétrica (Ênfase em Telecomunicações)',
    'CEFB': 'Educação Física',
    'CEMC': 'Engenharia Mecânica',
    'CEMT': 'Engenharia Mecatrônica',
    'CENF': 'Enfermagem',
    'CEPD': 'Engenharia de Produção',
    'CESF': 'Engenharia de Software',
    'CFAR': 'Farmácia',
    'CFIL': 'Bacharelado em Filosofia',
    'CFIS': 'Fisioterapia',
    'CGAS': 'Superior de Tecnologia em Gastronomia',
    'CHIS': 'Licenciatura em História',
    'CIBP': 'International Business Program IBP',
    'CICH': 'Bacharelado Interdisciplinar em Ciências e Humanidades',
    'CIS': 'Bacharelado Interdisciplinar em Saúde',
    'CJDI': 'Superior de Tecnologia em Jogos Digitais',
    'CJDV': 'Superior de Tecnologia em Jogos Digitais - Virtual',
    'CJOR': 'Jornalismo',
    'CLBI': 'Licenciatura em Ciências Biológicas',
    'CLFL': 'Licenciatura em Filosofia',
    'CLFS': 'Licenciatura em Física',
    'CLPI': 'Letras-Português-Inglês',
    'CMAT': 'Licenciatura em Matemática',
    'CMED': 'Medicina',
    'CMKT': 'Marketing',
    'CMPM': 'Produção Musical',
    'CMUS': 'Licenciatura em Música',
    'CMVT': 'Medicina Veterinária',
    'CNUT': 'Nutrição',
    'CODO': 'Odontologia',
    'CPED': 'Pedagogia',
    'CPSI': 'Psicologia',
    'CQUE': 'Engenharia Química',
    'CQUI': 'Licenciatura em Química',
    'CRPU': 'Relações Públicas',
    'CSOC': 'Licenciatura em Ciências Sociais',
    'CSSC': 'Serviço Social',
    'CTEA': 'Teatro',
    'CTEO': 'Bacharelado em Teologia',
    'CTSI': 'Superior de Tecnologia em Segurança da Informação',
    'GBF': 'Bacharelado em Filosofia',
    'GFL': 'Filosofia',
    'LAD': 'Administração',
    'LCC': 'Ciências Contábeis',
    'LDI': 'Direito',
    'LES': 'Engenharia de Software',
    'LFS': 'Fisioterapia',
    'LME': 'Medicina',
    'LPO': 'Engenharia de Produção',
    'LPS': 'Psicologia',
    'LTO': 'Teologia',
    'TAD': 'Administração',
    'TAG': 'Agronomia',
    'TCC': 'Ciências Contábeis',
    'TDI': 'Direito',
    'TGI': 'Gestão Integrada de Agronegócios',
    'TMV': 'Medicina Veterinária',
    'TPO': 'Engenharia de Produção',
    'TPS': 'Psicologia',
    # Multicom
    'CURIE': 'Bacharelado em Filosofia',
    'ELIANE BRUM': 'Jornalismo',
    'MARCELLO SERPA': 'Comunicação Social - Hab. Publicidade e Propaganda',
    'MARGARIDA KUNSCH': 'Relações Públicas',
    'PIAGET': 'Licenciatura em História',
    # Eixos
    'ENGENHARIA ADA': 'Engenharia de Computação',
    'ENGENHARIA AVILLA': 'Engenharia Civil',
    'ENGENHARIA BABBAGE BOLTZMANN': 'Engenharia Biomédica',
    'ENGENHARIA BELL': 'Engenharia Biomédica',
    'ENGENHARIA BENZ': 'Engenharia Mecatrônica',
    'ENGENHARIA BERRY': 'Engenharia de Computação',
    'ENGENHARIA BROGLIE': 'Engenharia Mecânica',
    'ENGENHARIA CLARKE': 'Engenharia Mecatrônica',
    'ENGENHARIA EASLEY': 'Engenharia Mecânica',
    'ENGENHARIA FAHRENHEIT': 'Engenharia Civil',
    'ENGENHARIA FEYNMAN': 'Engenharia Civil',
    'ENGENHARIA GOODALL': 'Engenharia Civil',
    'ENGENHARIA GUTEMBERG': 'Engenharia Civil',
    'ENGENHARIA HAMILTON BURNELL': 'Engenharia Mecânica',
    'ENGENHARIA HYPATIA': 'Engenharia Química',
    'ENGENHARIA JEMISON': 'Engenharia Mecânica',
    'ENGENHARIA NICOLELIS': 'Engenharia de Computação',
    'ENGENHARIA RUTHERFORD': 'Engenharia Química',
    'ENGENHARIA SIEMENS': 'Engenharia de Produção',
    'ENGENHARIA TELFORD': 'Engenharia Civil',
    # LEA
    'LEA': 'Letras-Português-Inglês',
    'LDN': 'Psicologia',
    'TLD': 'Psicologia'
}

dict_sigla_escola = {
    # EBA
    'CAUR': 'Belas Artes',
    'CBAV': 'Belas Artes',
    'CCAU': 'Belas Artes',
    'CCPP': 'Belas Artes',
    'CDDG': 'Belas Artes',
    'CDES': 'Belas Artes',
    'CJOR': 'Belas Artes',
    'CMPM': 'Belas Artes',
    'CMUS': 'Belas Artes',
    'CRPU': 'Belas Artes',
    'CTEA': 'Belas Artes',
    'ELIANE BRUM': 'Belas Artes',
    'MARCELLO SERPA': 'Belas Artes',
    'MARGARIDA KUNSCH': 'Belas Artes',
    # DIR
    'CDIR': 'Direito',
    # EEH
    'CBCS': 'Educação e Humanidades',
    'CBHI': 'Educação e Humanidades',
    'CEDF': 'Educação e Humanidades',
    'CFIL': 'Educação e Humanidades',
    'CHIS': 'Educação e Humanidades',
    'CICH': 'Educação e Humanidades',
    'CLBI': 'Educação e Humanidades',
    'CLFL': 'Educação e Humanidades',
    'CLFS': 'Educação e Humanidades',
    'CLPI': 'Educação e Humanidades',
    'CMAT': 'Educação e Humanidades',
    'CPED': 'Educação e Humanidades',
    'CQUI': 'Educação e Humanidades',
    'CSOC': 'Educação e Humanidades',
    'CSSC': 'Educação e Humanidades',
    'CTEO': 'Educação e Humanidades',
    'CURIE': 'Educação e Humanidades',
    'LEA': 'Educação e Humanidades',
    'PIAGET': 'Educação e Humanidades',
    # Londrina
    'LAD': 'Londrina',
    'LDI': 'Londrina',
    'LDN': 'Londrina',
    'LES': 'Londrina',
    'LFS': 'Londrina',
    'LME': 'Londrina',
    'LPO': 'Londrina',
    'LPS': 'Londrina',
    'LTO': 'Londrina',
    # Maringá
    'GBF': 'Maringá',
    'GFL': 'Maringá',
    # EMCV
    'CAGR': 'Medicina e Ciências da Vida',
    'CBED': 'Medicina e Ciências da Vida',
    'CBIT': 'Medicina e Ciências da Vida',
    'CCBI': 'Medicina e Ciências da Vida',
    'CEFB': 'Medicina e Ciências da Vida',
    'CENF': 'Medicina e Ciências da Vida',
    'CFAR': 'Medicina e Ciências da Vida',
    'CFIS': 'Medicina e Ciências da Vida',
    'CGAS': 'Medicina e Ciências da Vida',
    'CIS': 'Medicina e Ciências da Vida',
    'CMED': 'Medicina e Ciências da Vida',
    'CMVT': 'Medicina e Ciências da Vida',
    'CNUT': 'Medicina e Ciências da Vida',
    'CODO': 'Medicina e Ciências da Vida',
    'CPSI': 'Medicina e Ciências da Vida',
    # NEG
    'CADI': 'Negócios',
    'CADM': 'Negócios',
    'CAMM': 'Negócios',
    'CBND': 'Negócios',
    'CBNI': 'Negócios',
    'CCOT': 'Negócios',
    'CECO': 'Negócios',
    'CIBP': 'Negócios',
    'CMKT': 'Negócios',
    # Poli
    'CBJD': 'Politécnica',
    'CBSI': 'Politécnica',
    'CCBS': 'Politécnica',
    'CCCO': 'Politécnica',
    'CEAM': 'Politécnica',
    'CEBI': 'Politécnica',
    'CECA': 'Politécnica',
    'CECP': 'Politécnica',
    'CECV': 'Politécnica',
    'CEEE': 'Politécnica',
    'CEMC': 'Politécnica',
    'CEMT': 'Politécnica',
    'CEPD': 'Politécnica',
    'CESF': 'Politécnica',
    'CJDI': 'Politécnica',
    'CQUE': 'Politécnica',
    'ENGENHARIA ADA': 'Politécnica',
    'ENGENHARIA AVILLA': 'Politécnica',
    'ENGENHARIA BABBAGE BOLTZMANN': 'Politécnica',
    'ENGENHARIA BELL': 'Politécnica',
    'ENGENHARIA BENZ': 'Politécnica',
    'ENGENHARIA BERRY': 'Politécnica',
    'ENGENHARIA BROGLIE': 'Politécnica',
    'ENGENHARIA CLARKE': 'Politécnica',
    'ENGENHARIA EASLEY': 'Politécnica',
    'ENGENHARIA FAHRENHEIT': 'Politécnica',
    'ENGENHARIA FEYNMAN': 'Politécnica',
    'ENGENHARIA GOODALL': 'Politécnica',
    'ENGENHARIA GUTEMBERG': 'Politécnica',
    'ENGENHARIA HAMILTON BURNELL': 'Politécnica',
    'ENGENHARIA HYPATIA': 'Politécnica',
    'ENGENHARIA JEMISON': 'Politécnica',
    'ENGENHARIA NICOLELIS': 'Politécnica',
    'ENGENHARIA RUTHERFORD': 'Politécnica',
    'ENGENHARIA SIEMENS': 'Politécnica',
    'ENGENHARIA TELFORD': 'Politécnica',
    # Toledo
    'TAD': 'Toledo',
    'TAG': 'Toledo',
    'TCC': 'Toledo',
    'TDI': 'Toledo',
    'TGI': 'Toledo',
    'TLD': 'Toledo',
    'TMV': 'Toledo',
    'TPO': 'Toledo',
    'TPS': 'Toledo'
}


def trata_relatorio_ch(arquivo):
    # -- CH na Base Ouro --
    # Adiciona ch relogio oficial na base ouro
    # professor - carga horária por disciplina.xlsx
    # validador base ouro = cr disciplina + turma + disciplina
    # validador = cr + turma + disciplina

    df = pd.read_excel(arquivo)
    df = df[['CR Curso', 'Turma', 'Disciplina', 'C.H. Relógio Oficial']]
    df['CR Curso'] = pd.to_numeric(df['CR Curso'], errors='coerce')

    df['CR Curso'] = df['CR Curso'].fillna(0.0).astype(int)

    df.insert(0, 'Validador', '', True)
    df['Validador'] = df.apply(lambda row: f"{str(row['CR Curso']).strip()}    "
                                           f"{str(row['Turma']).strip()}    "
                                           f"{str(row['Disciplina']).strip()}",
                               axis=1)

    df = df[['Validador', 'C.H. Relógio Oficial']]

    return df


def main():
    print('Selecione a Relação de Alunos/Pais Exportação')

    Tk().withdraw()
    relacao_alunos = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione a Relação de Alunos/Pais Exportação')
    print(f'    {relacao_alunos}')

    print('Selecione o relatório de Alunos Matriculados por Disciplina')

    relatorio_disciplinas = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione o relatório de Alunos Matriculados por Disciplina')
    print(f'    {relatorio_disciplinas}')

    print('Selecione o relatório de Professor - Carga Horária por Turma e Disciplina')

    relatorio_ch = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione o relatório de Professor - Carga Horária por Turma e Disciplina')
    print(f'    {relatorio_ch}')
    print('Gerando a base ouro...')

    # Relatório Alunos Pais Exportação
    df_alunos = pd.read_excel(relacao_alunos)
    df_alunos = df_alunos[[
        'Estabelecimento', 'Escola', 'Centro de Resultado', 'Curso', 'Série', 'Matrícula',
        'Nome Completo', 'CPF', 'Data de Nascimento', 'Usuário Internet', 'E-mail', 'Telefone Celular',
        'Situação Acadêmica', 'Tipo de Entrada', 'Tipo de Ingresso', 'Turma', 'Turno', 'Gênero'
    ]]
    df_alunos = df_alunos.loc[df_alunos["Situação Acadêmica"] == 'Matriculado Curso Normal']
    df_alunos = df_alunos.drop_duplicates()

    # Relatóio Disicplinas SQL
    df_disciplinas = pd.read_excel(relatorio_disciplinas)
    df_disciplinas = df_disciplinas[[
        'CODIGO', 'DT_CADASTRO_CONTRATO', 'TURMA_BASE', 'DISCIPLINA', 'TURMA_DISCIPLINA', 'DIVISAO', 'DIVISAO2'
    ]]
    df_disciplinas = df_disciplinas.drop_duplicates()

    # Relatório CH Turma
    df_ch = trata_relatorio_ch(relatorio_ch)

    print('Juntando dados...')

    df_joined = pd.merge(
        left=df_alunos, right=df_disciplinas, left_on=['Matrícula', 'Turma'], right_on=['CODIGO', 'TURMA_BASE']
    )

    # modificando o dataframe
    df_joined = df_joined[['Estabelecimento', 'Escola', 'Centro de Resultado', 'Curso', 'Série', 'Matrícula',
                           'Nome Completo', 'CPF', 'Data de Nascimento', 'Usuário Internet', 'E-mail',
                           'Telefone Celular', 'Situação Acadêmica', 'Tipo de Entrada', 'Tipo de Ingresso',
                           'Turma', 'Turno', 'Gênero',
                           # dados disciplina
                           'DT_CADASTRO_CONTRATO', 'DISCIPLINA', 'TURMA_DISCIPLINA', 'DIVISAO', 'DIVISAO2']]

    df_joined.rename(columns={
        'Série': 'Período Aluno',
        'Turma': 'Turma Aluno',
        'Centro de Resultado': 'CR Aluno',
        'Curso': 'Curso Aluno',
        'Usuário Internet': 'E-mail Institucional',
        'Disciplina': 'DISCIPLINA',
        'Turma Destino': 'TURMA_DISCIPLINA',
    }, inplace=True)

    print('Calculando...')

    df_joined['E-mail Institucional'] = df_joined.apply(
        lambda row: f"{row['E-mail Institucional']}@pucpr.edu.br",
        axis=1)

    df_joined.insert(18, 'Escola Disciplina', '', True)
    df_joined['Escola Disciplina'] = df_joined.apply(
        lambda row: encontra_escola(row['TURMA_DISCIPLINA']),
        axis=1)

    df_joined.insert(19, 'Curso_Disciplina', '', True)
    df_joined['Curso_Disciplina'] = df_joined.apply(
        lambda row: encontra_curso(row['TURMA_DISCIPLINA']),
        axis=1)

    df_joined.insert(20, 'Período_Disciplina', '', True)
    df_joined['Período_Disciplina'] = df_joined.apply(
        lambda row: encontra_periodo(row['TURMA_DISCIPLINA']),
        axis=1)

    df_joined.insert(21, 'CR_Disciplina', '', True)
    df_joined['CR_Disciplina'] = df_joined.apply(
        lambda row: encontra_cr(row['TURMA_DISCIPLINA']),
        axis=1)

    # Remove o início do nome do estabelecimento
    df_joined['Estabelecimento'] = df_joined['Estabelecimento'].str.replace(
        'Pontifícia Universidade Católica do Paraná - ', '')

    # Remove o início do nome da escola
    df_joined['Escola'] = df_joined['Escola'] \
        .str.replace('Escola de ', '') \
        .str.replace('Escola ', '')

    # Corrige Belas Artes
    df_joined['Escola'] = df_joined['Escola'] \
        .str.replace('Comunicação e Artes', 'Belas Artes') \
        .str.replace('Arquitetura e Design', 'Belas Artes')

    # Altera a escola para o nome do campus fora de sede
    df_joined.loc[
        (df_joined['Estabelecimento'] == 'Londrina') |
        (df_joined['Estabelecimento'] == 'Maringá') |
        (df_joined['Estabelecimento'] == 'Toledo'),
        'Escola'] = df_joined['Estabelecimento']

    # No período do aluno deixar só os números
    df_joined['Período Aluno'] = df_joined['Período Aluno'] \
        .str.replace('º Periodo', '') \
        .str.replace('º Período', '')

    # Preenche a coluna Gênero com "Não informado" quando estiver vazia
    df_joined["Gênero"].fillna("Não informado", inplace=True)

    # Remove espaços antes e depois dos nomes
    df_joined['Nome Completo'] = df_joined['Nome Completo'].str.strip()

    # Insere validador para a inclusão da coluna de carga horária
    df_joined.insert(0, 'Validador', '', True)
    df_joined['Validador'] = df_joined.apply(
        lambda row: f"{str(row['CR_Disciplina']).strip()}    "
                    f"{str(row['TURMA_DISCIPLINA']).strip()}    "
                    f"{str(row['DISCIPLINA']).strip()}",
        axis=1)

    df_joined = pd.merge(left=df_joined, right=df_ch, left_on='Validador', right_on='Validador', how='left')
    del df_joined['Validador']

    # Remove linhas duplicadas
    df_joined = df_joined.drop_duplicates()

    print('Criando arquivos de saída...')

    dh = dt.now()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(f'Base_ouro_completa_{dh.strftime("%Y%m%d_%Hh%M")}.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df_joined.to_excel(writer, sheet_name='Sheet1', index=False)

    print('Salvando arquivos...')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print('Geração de arquivos finalizada!')


if __name__ == '__main__':
    main()
