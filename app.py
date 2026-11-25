import streamlit as st
import dados


def classificar_nota(nota):
    """Classifica a avaliação em uma faixa de texto."""
    if nota >= 4.5:
        return "Excelente"
    elif nota >= 4.0:
        return "Bom"
    elif nota >= 3.5:
        return "Passável"
    elif nota >= 3.0:
        return "Ruim"
    else:
        if nota == 0.0:
            return "NA"
        return "Péssimo"

def arredondar_estrelas(estrelas):
    if estrelas > 0:
        qtd_estrelas = int(round(estrelas))
        if qtd_estrelas < 1:
            qtd_estrelas = 1
        nota_lamen = f"{estrelas:.2f} " + ("🍜" * qtd_estrelas)
    else:
        nota_lamen = "NA"

    return nota_lamen

def arrumar_estilo_null(estilo):
    if not estilo:
        return "NA"
    return estilo

def montar_tabela(lamens):
    """Prepara as linhas para a tabela exibida no Streamlit."""
    tabela = []

    for lamen in lamens:

        linha = {
            "Variedade / Nome": lamen["variedade"],
            "Marca": lamen["marca"],
            "Estilo": arrumar_estilo_null(lamen["estilo"]),
            "País": lamen["pais"],
            "Nota": arredondar_estrelas(lamen["estrelas"]),
            "Avaliação": classificar_nota(lamen["estrelas"]),
        }
        tabela.append(linha)
    return tabela



def buscar_por_termo(nomes, marcas, estilos, paises):
    tabela = []

    for lamen in nomes:
        if lamen in paises and lamen in marcas and lamen in estilos:
            tabela.append(lamen)

    return tabela


def listar_nomes(lamens):
    """Retorna a lista de nomes sem repetição e ordenada."""
    nomes = sorted(list({lamen["variedade"] for lamen in lamens if "variedade" in lamen}))
    return nomes

def listar_marcas(lamens):
    """Retorna a lista de países sem repetição e ordenada."""
    sabores = sorted(list({lamen["marca"] for lamen in lamens if "marca" in lamen}))
    return sabores

def listar_estilos(lamens):
    """Retorna a lista de estilos sem repetição e ordenada."""
    estilos = sorted(list({lamen["estilo"] for lamen in lamens if "estilo" in lamen}))
    return estilos

def listar_paises(lamens):
    """Retorna a lista de países sem repetição e ordenada."""
    paises = sorted(list({lamen["pais"] for lamen in lamens if "pais" in lamen}))
    return paises


def filtrar_por_nome(lamens, nome):
    """Filtra por nome escolhido."""
    if nome == "Todos":
        return lamens
    return [variedade for variedade in lamens if variedade["variedade"] == nome]

def filtrar_por_marca(lamens, sabor):
    """Filtra por país escolhido."""
    if sabor == "Todos":
        return lamens
    return [sabo for sabo in lamens if sabo["marca"] == sabor]

def filtrar_por_estilo(lamens, estilos):
    """Filtra por país escolhido."""
    if estilos == "Todos":
        return lamens
    return [estilo for estilo in lamens if estilo["estilo"] == estilos]

def filtrar_por_pais(lamens, pais):
    """Filtra por país escolhido."""
    if pais == "Todos":
        return lamens
    return [prato for prato in lamens if prato["pais"] == pais]



def main():
    st.set_page_config(page_title="Lámens pelo mundo", page_icon="🍜", layout="wide")
    st.title("Lámens do Mundo")

    lamens = dados.carregar_lamens()

    if not lamens:
        st.error("Nenhum dado encontrado no arquivo CSV.")
        return

    # Métricas Principais em 4 colunas na parte superior
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total de Lámens", len(lamens))

    qtd_top = dados.contar_cinco_estrelas(lamens)
    col3.metric("Lámens nota 5", qtd_top)

    polos = dados.encontrar_polos(lamens)
    if polos:
        col4.metric("Lámen mais bem avaliado", f"{polos[0]['estrelas']:.1f} 🍜")
        col4.caption(f"{polos[0]['marca']} - {polos[0]['variedade']}")
        col5.metric("Lámen mais bem avaliado", f"{polos[1]['estrelas']:.1f} 🍜")
        col5.caption(f"{polos[1]['marca']} - {polos[1]['variedade']}")

    st.divider()

    # Filtros
    col_nome, col_marca, col_estilo, col_pais = st.columns(4)
    nome_selecionado = col_nome.selectbox(
        "Filtrar por Variedade/Nome", ["Todos"] + listar_nomes(lamens)
    )
    marca_selecionada = col_marca.selectbox(
        "Filtrar por Marca", ["Todos"] + listar_marcas(lamens)
    )
    estilo_selecionado = col_estilo.selectbox(
        "Filtrar por Estilo", ["Todos"] + listar_estilos(lamens)
    )
    pais_selecionado = col_pais.selectbox(
            "Filtrar por País", ["Todos"] + listar_paises(lamens)
    )

    # Aplicação dos filtros
    dados_de_nomes = filtrar_por_nome(lamens, nome_selecionado)
    dados_de_marca = filtrar_por_marca(lamens, marca_selecionada)
    dados_de_estilo = filtrar_por_estilo(lamens, estilo_selecionado)
    dados_de_paises = filtrar_por_pais(lamens, pais_selecionado)
    encontrados = buscar_por_termo(dados_de_nomes, dados_de_marca, dados_de_estilo, dados_de_paises)

    # Nota média com a lista dos encontrados
    nota_media = dados.calcular_nota_media(encontrados)
    col2.metric("Nota Média", f"{nota_media:.2f} 🍜")

    qtd_encontrados = len(encontrados)

    if qtd_encontrados == 0:
        st.warning("Nenhum lámen encontrado com os filtros aplicados.")
    else:
        st.write(f"Lámens encontrados: {qtd_encontrados}")
        st.dataframe(montar_tabela(encontrados), use_container_width=True)

if __name__ == "__main__":
    main()
