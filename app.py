import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dimensionamento Pluvial - NBR 10844", layout="wide")

st.title("Dimensionamento de Instalações Prediais de Águas Pluviais")
st.markdown("**Norma de Referência:** NBR 10844/1989")

tab1, tab2, tab3 = st.tabs([
    "1. Calhas Horizontais", 
    "2. Condutores Verticais", 
    "3. Condutores Horizontais"
])

# ==============================================================================
# ABA 1: CALHAS HORIZONTAIS
# ==============================================================================
with tab1:
    st.header("Dimensionamento de Calhas Horizontais")
    
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        st.subheader("Parâmetros de Entrada")
        
        st.markdown("**Área de Contribuição**")
        area_c1 = st.number_input("Área de contribuição total (A) [m²]:", min_value=0.0, value=150.0, step=10.0, key="area_calha")
        i_pluv1 = st.number_input("Intensidade pluviométrica (I) [mm/h]:", min_value=0.0, value=150.0, step=10.0, key="i_calha")
        
        st.markdown("---")
        st.markdown("**Geometria e Características da Calha (Seção Retangular)**")
        b_calha = st.number_input("Largura da base da calha (b) [m]:", min_value=0.01, value=0.25, step=0.05, format="%.3f")
        h_molhada = st.number_input("Altura da lâmina de água / molhada (h) [m]:", min_value=0.01, value=0.166, step=0.01, format="%.3f")
        n_rug = st.number_input("Coeficiente de rugosidade de Manning (n):", min_value=0.001, value=0.011, step=0.001, format="%.3f", help="Ex: Plástico/Metal = 0.011")
        declividade = st.number_input("Declividade da calha (i) [m/m]:", min_value=0.0001, value=0.0050, step=0.0005, format="%.4f", help="Mínimo de 0,5% (0.0050 m/m) conforme item 5.5.2")

    with col_out:
        st.subheader("Memorial de Cálculo Detalhado")
        
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        st.markdown("> \"A vazão de projeto deve ser calculada pela fórmula: $Q = \\frac{I \\cdot A}{60}$\" — **Página 3, Item 5.3.1**")
        
        q_proj1 = (i_pluv1 * area_c1) / 60.0
        
        st.markdown("**Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv1:.2f}$ mm/h")
        st.markdown(f"- $A = {area_c1:.2f}$ m²")
        st.markdown("**Aplicação:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv1:.2f} \\cdot {area_c1:.2f}}}{{60}}")
        st.markdown(f"**Resultado:** $Q_{{proj}} = {q_proj1:.2f}$ L/min")
        
        st.markdown("---")
        
        st.markdown("#### 2. Capacidade da Calha ($Q_{calha}$)")
        st.markdown("> \"O dimensionamento das calhas deve ser feito através da fórmula de Manning-Strickler... $Q = K \\cdot S \\cdot R^{2/3} \\cdot i^{1/2}$\" — **Página 5, Item 5.5.7**")
        
        S_area = b_calha * h_molhada
        P_perimetro = b_calha + (2 * h_molhada)
        R_hidr = S_area / P_perimetro if P_perimetro > 0 else 0
        K_cte = 60000.0
        
        q_calha_calc = (K_cte * S_area * (R_hidr ** (2/3)) * (declividade ** 0.5)) / n_rug
        
        st.markdown("**Símbolos e Valores:**")
        st.markdown(f"- $b = {b_calha:.3f}$ m (Largura da base)")
        st.markdown(f"- $h = {h_molhada:.3f}$ m (Altura da lâmina)")
        st.markdown(f"- $n = {n_rug:.3f}$ (Coeficiente de rugosidade)")
        st.markdown(f"- $i = {declividade:.4f}$ m/m (Declividade)")
        st.markdown(f"- $S = b \\cdot h = {b_calha:.3f} \\cdot {h_molhada:.3f} = {S_area:.4f}$ m² (Área molhada)")
        st.markdown(f"- $P = b + 2h = {b_calha:.3f} + 2({h_molhada:.3f}) = {P_perimetro:.4f}$ m (Perímetro molhado)")
        st.markdown(f"- $R = \\frac{{S}}{{P}} = \\frac{{{S_area:.4f}}}{{{P_perimetro:.4f}}} = {R_hidr:.4f}$ m (Raio hidráulico)")
        st.markdown(f"- $K = {K_cte:.0f}$ (Fator de conversão para L/min)")
        
        st.markdown("**Aplicação:**")
        st.latex(r"Q_{calha} = \frac{K \cdot S \cdot R^{2/3} \cdot i^{1/2}}{n}")
        st.latex(f"Q_{{calha}} = \\frac{{{K_cte:.0f} \\cdot {S_area:.4f} \\cdot {R_hidr:.4f}^{{2/3}} \\cdot {declividade:.4f}^{{1/2}}}}{{{n_rug:.3f}}}")
        st.markdown(f"**Resultado:** $Q_{{calha}} = {q_calha_calc:.2f}$ L/min")
        
        st.markdown("---")
        
        st.markdown("#### Verificação de Conformidade")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Vazão Solicitada (Q_proj)", value=f"{q_proj1:.2f} L/min")
        with res_col2:
            st.metric(label="Capacidade da Calha (Q_calha)", value=f"{q_calha_calc:.2f} L/min")
            
        if q_calha_calc >= q_proj1:
            st.success("✅ **CONFORMIDADE ATENDIDA:** A capacidade da calha é maior ou igual à vazão de projeto.")
        else:
            st.error("❌ **NÃO ATENDE:** A capacidade da calha é insuficiente para a vazão de projeto calculada. Aumente as dimensões ou a declividade.")

# ==============================================================================
# ABA 2: CONDUTORES VERTICAIS
# ==============================================================================
with tab2:
    st.header("Dimensionamento de Condutores Verticais")
    
    col_v1, col_v2 = st.columns([1, 1.2])
    
    with col_v1:
        st.subheader("Parâmetros de Entrada")
        area_c2 = st.number_input("Área de contribuição para este condutor (A) [m²]:", min_value=0.0, value=150.0, step=10.0, key="area_vert")
        i_pluv2 = st.number_input("Intensidade pluviométrica (I) [mm/h]:", min_value=0.0, value=150.0, step=10.0, key="i_vert")
        
        st.markdown("---")
        st.write("**Seleção do Diâmetro Nominal (DN) via Ábaco:**")
        diametro_escolhido = st.selectbox(
            "Selecione o diâmetro adotado após consulta aos gráficos:",
            ["70 mm (Mínimo permitido)", "75 mm", "100 mm", "125 mm", "150 mm", "200 mm"]
        )

    with col_v2:
        st.subheader("Memorial de Cálculo e Ábacos")
        
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        q_proj2 = (i_pluv2 * area_c2) / 60.0
        
        st.markdown("**Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv2:.2f}$ mm/h")
        st.markdown(f"- $A = {area_c2:.2f}$ m²")
        st.markdown("**Aplicação:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv2:.2f} \\cdot {area_c2:.2f}}}{{60}}")
        st.markdown(f"**Resultado:** $Q_{{proj}} = {q_proj2:.2f}$ L/min")
        
        st.markdown("---")
        st.markdown("#### 2. Verificação por Ábacos (Figura 3)")
        st.markdown("> \"O diâmetro interno mínimo dos condutores verticais de seção circular é 70mm.\" — **Página 7, Item 5.6.3**")
        st.markdown("> \"O diâmetro interno (D) do condutor vertical é obtido através dos ábacos da Figura 3...\" — **Página 7, Item 5.6.4**")
        
        st.markdown("**Símbolos:**")
        st.markdown("- **Q** = Vazão de projeto, em L/min")
        st.markdown("- **H** = altura da lâmina de água na calha, em mm")
        st.markdown("- **L** = comprimento do condutor vertical, em m")
        
        st.markdown("**Procedimento:** levantar uma vertical por Q até interceptar as curvas de H e L correspondentes. No caso de não haver curvas dos valores de H e L, interpolar entre as curvas existentes. Transportar a interseção mais alta até o eixo D. Adotar o diâmetro nominal cujo diâmetro interno seja superior ou igual ao valor encontrado.")
        
        ab_col1, ab_col2 = st.columns(2)
        with ab_col1:
            st.image("Abaco calha com saida em aresta viva.png", caption="Figura 3 (a) - Saída em Aresta Viva")
        with ab_col2:
            st.image("Abaco calha com funil da saida.png", caption="Figura 3 (b) - Saída com Funil")
            
        st.markdown("---")
        st.markdown("#### Alinhamento do Diâmetro Adotado")
        v_res1, v_res2 = st.columns(2)
        with v_res1:
            st.metric(label="Vazão a Escoar", value=f"{q_proj2:.2f} L/min")
        with v_res2:
            st.metric(label="Diâmetro Escolhido", value=diametro_escolhido)

# ==============================================================================
# ABA 3: CONDUTORES HORIZONTAIS
# ==============================================================================
with tab3:
    st.header("Dimensionamento de Condutores Horizontais")
    
    col_h1, col_h2 = st.columns([1, 1.2])
    
    with col_h1:
        st.subheader("Parâmetros de Entrada")
        area_c3 = st.number_input("Área de contribuição (A) [m²]:", min_value=0.0, value=150.0, step=10.0, key="area_horiz")
        i_pluv3 = st.number_input("Intensidade pluviométrica (I) [mm/h]:", min_value=0.0, value=150.0, step=10.0, key="i_horiz")
        
        st.markdown("---")
        st.markdown("**Parâmetros do Trecho Horizontal**")
        declividade_h = st.selectbox("Declividade do tubo (i):", ["0,5%", "1%", "2%", "4%"])
        diametro_tubo = st.selectbox("Diâmetro Nominal (DN) do tubo [mm]:", [75, 100, 125, 150, 200, 250, 300])
        num_tubos = st.number_input("Quantidade de tubos paralelos:", min_value=1, value=1, step=1)

    with col_h2:
        st.subheader("Memorial de Cálculo e Tabela de Referência")
        
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        q_proj3 = (i_pluv3 * area_c3) / 60.0
        
        st.markdown("**Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv3:.2f}$ mm/h")
        st.markdown(f"- $A = {area_c3:.2f}$ m²")
        st.markdown("**Aplicação:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv3:.2f} \\cdot {area_c3:.2f}}}{{60}}")
        st.markdown(f"**Resultado:** $Q_{{proj}} = {q_proj3:.2f}$ L/min")
        
        st.markdown("---")
        st.markdown("#### 2. Capacidade Conforme Tabela 4 (n = 0,011)")
        st.markdown("> \"O dimensionamento dos condutores horizontais de seção circular deve ser feito para escoamento com lâmina de altura igual a 2/3 do diâmetro interno (D) do tubo. As vazões para tubos de vários materiais e inclinações usuais estão indicadas na Tabela 4.\" — **Página 9, Item 5.7.2**")
        
        # Tabela 4 completa para n = 0,011 (Tubos de plástico/ferro fundido, etc.)
        dados_tabela4 = {
            "Diâmetro (mm)": [75, 100, 125, 150, 200, 250, 300],
            "0,5%": [95.0, 204.0, 370.0, 602.0, 1310.0, 2390.0, 3890.0],
            "1%": [133.0, 287.0, 521.0, 847.0, 1840.0, 3370.0, 5490.0],
            "2%": [188.0, 405.0, 735.0, 1190.0, 2600.0, 4770.0, 7760.0],
            "4%": [267.0, 575.0, 1040.0, 1680.0, 3680.0, 6740.0, 10900.0]
        }
        df_tab4 = pd.DataFrame(dados_tabela4)
        
        st.dataframe(df_tab4, hide_index=True)
        
        # Busca a capacidade de um tubo único
        idx_tubo = df_tab4.index[df_tab4['Diâmetro (mm)'] == diametro_tubo].tolist()[0]
        capacidade_unitaria = df_tab4.at[idx_tubo, declividade_h]
        capacidade_total = capacidade_unitaria * num_tubos
        
        st.markdown("---")
        st.markdown("#### Verificação de Conformidade e Alinhamento")
        
        st.write(f"**Capacidade de 1 tubo DN {diametro_tubo} a {declividade_h}:** {capacidade_unitaria:.2f} L/min")
        st.write(f"**Multiplicador:** {num_tubos} tubo(s) selecionado(s)")
        
        h_res1, h_res2 = st.columns(2)
        with h_res1:
            st.metric(label="Vazão Solicitada (Q_proj)", value=f"{q_proj3:.2f} L/min")
            
        with h_res2:
            st.metric(label="Capacidade Total Instalada", value=f"{capacidade_total:.2f} L/min")
                
        if capacidade_total >= q_proj3:
            st.success(f"✅ **CONFORMIDADE ATENDIDA:** A capacidade dos {num_tubos} tubo(s) DN {diametro_tubo} mm é suficiente para a vazão de projeto.")
        else:
            st.error(f"❌ **NÃO ATENDE:** A capacidade dos tubos selecionados ({capacidade_total:.2f} L/min) é inferior à vazão solicitada ({q_proj3:.2f} L/min). Adicione mais tubos, aumente o diâmetro ou a declividade.")