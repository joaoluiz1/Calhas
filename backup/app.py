import streamlit as st
import pandas as pd
import math
import os
import plotly.graph_objects as go
from PIL import Image

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
        st.markdown("**Geometria e Características da Calha (Valores em mm)**")
        
        tipo_calha = st.radio("Selecione o formato da calha:", ["Retangular", "Semicircular"])
        
        if tipo_calha == "Retangular":
            b_calha_mm = st.number_input("Largura da base da calha (b) [mm]:", min_value=10.0, value=250.0, step=10.0)
            h_total_calha_mm = st.number_input("Altura total da calha (H) [mm]:", min_value=10.0, value=250.0, step=10.0)
            prop_selecionada = st.selectbox("Proporção para a altura molhada:", ["50%", "66%", "75%"])
            
            b_calha = b_calha_mm / 1000.0
            h_total_calha = h_total_calha_mm / 1000.0
            
            mapa_proporcoes = {"50%": 0.50, "66%": 0.66, "75%": 0.75}
            fator_prop = mapa_proporcoes[prop_selecionada]
            h_molhada = h_total_calha * fator_prop
            
        else:
            d_calha_mm = st.number_input("Diâmetro interno da calha semicircular (D) [mm]:", min_value=10.0, value=150.0, step=10.0)
            
            d_calha = d_calha_mm / 1000.0
            r_calha = d_calha / 2.0
            h_molhada = r_calha 
            
        n_rug = st.number_input("Coeficiente de rugosidade de Manning (n):", min_value=0.001, value=0.011, step=0.001, format="%.3f")
        declividade = st.number_input("Declividade da calha (i) [m/m]:", min_value=0.0001, value=0.0050, step=0.0005, format="%.4f")

    with col_out:
        st.subheader("Memorial de Cálculo Detalhado")
        
        # ---------------------------------------------------------
        # MEMORIAL 1: VAZÃO DE PROJETO
        # ---------------------------------------------------------
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        q_proj1 = (i_pluv1 * area_c1) / 60.0
        
        st.markdown("**1. Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv1:.2f}$ mm/h (Intensidade pluviométrica)")
        st.markdown(f"- $A = {area_c1:.2f}$ m² (Área de contribuição)")
        
        st.markdown("**2. Fórmula:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        
        st.markdown("**3. Substituição na Fórmula:**")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv1:.2f} \\cdot {area_c1:.2f}}}{{60}}")
        
        st.markdown("**4. Resultado:**")
        st.success(f"$Q_{{proj}} = {q_proj1:.2f}$ L/min")
        
        st.markdown("---")
        
        # ---------------------------------------------------------
        # MEMORIAL 2: CAPACIDADE DA CALHA
        # ---------------------------------------------------------
        st.markdown(f"#### 2. Capacidade da Calha ({tipo_calha}) ($Q_{{calha}}$)")
        K_cte = 60000.0
        
        if tipo_calha == "Retangular":
            S_area = b_calha * h_molhada
            P_perimetro = b_calha + (2 * h_molhada)
            R_hidr = S_area / P_perimetro if P_perimetro > 0 else 0
            
            st.markdown("**1. Símbolos, Geometria e Valores:**")
            st.markdown(f"- $b = {b_calha_mm:.1f}$ mm $= {b_calha:.3f}$ m (Largura da base)")
            st.markdown(f"- $H_{{total}} = {h_total_calha_mm:.1f}$ mm $= {h_total_calha:.3f}$ m (Altura da calha)")
            st.markdown(f"- $h = H_{{total}} \\cdot {fator_prop:.2f} = {h_molhada:.3f}$ m (Altura da lâmina d'água)")
            st.markdown(f"- $S = b \\cdot h = {b_calha:.3f} \\cdot {h_molhada:.3f} = {S_area:.4f}$ m² (Área molhada)")
            st.markdown(f"- $P = b + 2h = {b_calha:.3f} + 2({h_molhada:.3f}) = {P_perimetro:.4f}$ m (Perímetro molhado)")
        else:
            cos_metade_theta = (r_calha - h_molhada) / r_calha
            theta = 2 * math.acos(cos_metade_theta)
            S_area = (r_calha**2 / 2) * (theta - math.sin(theta))
            P_perimetro = r_calha * theta
            R_hidr = S_area / P_perimetro if P_perimetro > 0 else 0
            
            st.markdown("**1. Símbolos, Geometria e Valores:**")
            st.markdown(f"- $D = {d_calha_mm:.1f}$ mm $= {d_calha:.3f}$ m (Diâmetro interno)")
            st.markdown(f"- $R = {d_calha_mm/2:.1f}$ mm $= {r_calha:.3f}$ m (Raio e Altura máxima da calha)")
            st.markdown(f"- $h = \\frac{{2}}{{3}} \\cdot R = {h_molhada:.3f}$ m (Altura da lâmina d'água)")
            st.markdown(f"- $\\theta = 2 \\cdot \\arccos\\left(\\frac{{R - h}}{{R}}\\right) = 2 \\cdot \\arccos({cos_metade_theta:.3f}) = {theta:.4f}$ rad (Ângulo central)")
            st.markdown(f"- $S = \\frac{{R^2}}{{2}} \\cdot (\\theta - \\sin(\\theta)) = \\frac{{{r_calha:.3f}^2}}{{2}} \\cdot ({theta:.4f} - {math.sin(theta):.4f}) = {S_area:.4f}$ m² (Área molhada)")
            st.markdown(f"- $P = R \\cdot \\theta = {r_calha:.3f} \\cdot {theta:.4f} = {P_perimetro:.4f}$ m (Perímetro molhado)")

        st.markdown(f"- $R_h = \\frac{{S}}{{P}} = \\frac{{{S_area:.4f}}}{{{P_perimetro:.4f}}} = {R_hidr:.4f}$ m (Raio hidráulico)")
        st.markdown(f"- $n = {n_rug:.3f}$ (Rugosidade de Manning)")
        st.markdown(f"- $i = {declividade:.4f}$ m/m (Declividade)")
        st.markdown(f"- $K = {K_cte:.0f}$ (Constante da fórmula)")

        q_calha_calc = (K_cte * S_area * (R_hidr ** (2/3)) * (declividade ** 0.5)) / n_rug

        st.markdown("**2. Fórmula (Manning-Strickler):**")
        st.latex(r"Q_{calha} = \frac{K \cdot S \cdot R_h^{2/3} \cdot i^{1/2}}{n}")
        
        st.markdown("**3. Substituição na Fórmula:**")
        st.latex(f"Q_{{calha}} = \\frac{{{K_cte:.0f} \\cdot {S_area:.4f} \\cdot {R_hidr:.4f}^{{2/3}} \\cdot {declividade:.4f}^{{1/2}}}}{{{n_rug:.3f}}}")
        
        st.markdown("**4. Resultado:**")
        st.success(f"$Q_{{calha}} = {q_calha_calc:.2f}$ L/min")
        
        st.markdown("---")
        
        if q_calha_calc >= q_proj1:
            st.info(f"✅ **CONFORMIDADE ATENDIDA:** A capacidade ({q_calha_calc:.2f} L/min) superou a demanda ({q_proj1:.2f} L/min).")
        else:
            st.error(f"❌ **NÃO ATENDE:** A capacidade ({q_calha_calc:.2f} L/min) é inferior à demanda ({q_proj1:.2f} L/min).")

        txt_calha = f"""MEMORIAL DE CALCULO - CALHAS HORIZONTAIS
Norma de Referencia: NBR 10844/1989

--------------------------------------------------
1. VAZAO DE PROJETO (Q_proj)
--------------------------------------------------
--- Simbolos ---
I = {i_pluv1:.2f} mm/h
A = {area_c1:.2f} m2

--- Formula ---
Q_proj = (I * A) / 60

--- Substituicao ---
Q_proj = ({i_pluv1:.2f} * {area_c1:.2f}) / 60

--- Resultado ---
Q_proj = {q_proj1:.2f} L/min


--------------------------------------------------
2. CAPACIDADE DA CALHA (Q_calha)
--------------------------------------------------
--- Simbolos ---
Formato: {tipo_calha}
Area Molhada (S) = {S_area:.4f} m2
Perimetro Molhado (P) = {P_perimetro:.4f} m
Raio Hidraulico (Rh) = {R_hidr:.4f} m
Rugosidade (n) = {n_rug:.3f}
Declividade (i) = {declividade:.4f} m/m
K = 60000

--- Formula ---
Q_calha = (K * S * Rh^(2/3) * i^(1/2)) / n

--- Substituicao ---
Q_calha = (60000 * {S_area:.4f} * {R_hidr:.4f}^(2/3) * {declividade:.4f}^(1/2)) / {n_rug:.3f}

--- Resultado ---
Q_calha = {q_calha_calc:.2f} L/min

Status Final: {"ATENDE" if q_calha_calc >= q_proj1 else "NAO ATENDE"}
"""
        st.download_button("📄 Baixar Memorial de Calhas (TXT)", data=txt_calha, file_name="memorial_calhas.txt")

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
        
        q_proj2 = (i_pluv2 * area_c2) / 60.0
        
        st.markdown("---")
        diametro_escolhido = st.selectbox(
            "Após realizar a leitura livre no ábaco ao lado, selecione o Diâmetro Nominal (DN) adotado:",
            ["70 mm (Mínimo)", "75 mm", "100 mm", "125 mm", "150 mm", "200 mm"]
        )

    with col_v2:
        st.subheader("Memorial de Cálculo e Ábacos")
        
        # ---------------------------------------------------------
        # MEMORIAL 1: VAZÃO DE PROJETO
        # ---------------------------------------------------------
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        st.markdown("**1. Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv2:.2f}$ mm/h")
        st.markdown(f"- $A = {area_c2:.2f}$ m²")
        
        st.markdown("**2. Fórmula:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        
        st.markdown("**3. Substituição na Fórmula:**")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv2:.2f} \\cdot {area_c2:.2f}}}{{60}}")
        
        st.markdown("**4. Resultado:**")
        st.success(f"$Q_{{proj}} = {q_proj2:.2f}$ L/min")
        
        st.markdown("---")
        st.markdown("#### 2. Ábaco Interativo (Figura 3)")
        
        tipo_abaco = st.radio("Selecione o tipo de saída para o gráfico:", ["Saída em Aresta Viva", "Saída com Funil"])
        
        if tipo_abaco == "Saída em Aresta Viva":
            st.markdown("**Figura 3 (a) - Saída em Aresta Viva**")
            arquivo_img = "Abaco calha com saida em aresta viva.png"
        else:
            st.markdown("**Figura 3 (b) - Saída com Funil**")
            arquivo_img = "Abaco calha com funil da saida.png"
            
        # Placeholder para renderizar o gráfico ACIMA dos controles
        grafico_placeholder = st.empty()
        
        st.markdown("---")
        st.markdown("**Controles Livres (Totalmente Visuais)**")
        st.info("Deslize as bolinhas abaixo para mover as linhas e cruzar os valores na imagem.")
        
        # Sliders embaixo do gráfico controlando apenas a posição percentual X e Y (0 a 100)
        pos_x = st.slider("Mover Linha Vertical (Esquerda ↔ Direita)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
        pos_y = st.slider("Mover Linha Horizontal (Baixo ↕ Cima)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
        
        # Plotagem do gráfico baseada exclusivamente nas bolinhas
        fig = go.Figure()
        
        if os.path.exists(arquivo_img):
            img = Image.open(arquivo_img)
            fig.add_layout_image(
                dict(
                    source=img, xref="x", yref="y",
                    x=0, y=100, sizex=100, sizey=100,
                    sizing="stretch", opacity=1, layer="below"
                )
            )
        
        fig.update_xaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)
        fig.update_yaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)
        
        fig.add_shape(type="line", x0=pos_x, y0=0, x1=pos_x, y1=100, 
                      line=dict(color="red", width=2, dash="dash"))
        fig.add_shape(type="line", x0=0, y0=pos_y, x1=100, y1=pos_y, 
                      line=dict(color="blue", width=2))
        
        fig.update_layout(height=650, margin=dict(l=0, r=0, t=10, b=0), template="plotly_white")
        
        # Injeta o gráfico pronto no placeholder criado acima dos botões
        grafico_placeholder.plotly_chart(fig, use_container_width=True)

        txt_vert = f"""MEMORIAL DE CALCULO - CONDUTORES VERTICAIS
Norma de Referencia: NBR 10844/1989

--------------------------------------------------
1. VAZAO DE PROJETO (Q_proj)
--------------------------------------------------
--- Simbolos ---
I = {i_pluv2:.2f} mm/h
A = {area_c2:.2f} m2

--- Formula ---
Q_proj = (I * A) / 60

--- Substituicao ---
Q_proj = ({i_pluv2:.2f} * {area_c2:.2f}) / 60

--- Resultado ---
Q_proj = {q_proj2:.2f} L/min


--------------------------------------------------
2. LEITURA PELO ABACO (FIGURA 3)
--------------------------------------------------
Saida adotada: {tipo_abaco}
Analise realizada visualmente e de forma livre atraves do abaco.

RESULTADO FINAL ADOTADO: {diametro_escolhido}
"""
        st.download_button("📄 Baixar Memorial dos Verticais (TXT)", data=txt_vert, file_name="memorial_verticais.txt")

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
        
        opcoes_mat = {
            "Plástico, fibrocimento, aço galvanizado (n = 0,011)": 0.011,
            "Ferro fundido, concreto alisado (n = 0,012)": 0.012,
            "Cerâmica, concreto não alisado (n = 0,013)": 0.013
        }
        escolha_material = st.selectbox("Selecione o material para aplicar o fator de correção:", list(opcoes_mat.keys()))
        n_escolhido = opcoes_mat[escolha_material]
        fator_correcao = 0.011 / n_escolhido
        
        declividade_h = st.selectbox("Declividade do tubo (i):", ["0,5%", "1%", "2%", "4%"])
        diametro_tubo = st.selectbox("Diâmetro Nominal (DN) do tubo [mm]:", [50, 75, 100, 125, 150, 200, 250, 300], index=1)
        num_tubos = st.number_input("Quantidade de tubos paralelos:", min_value=1, value=1, step=1)

    with col_h2:
        st.subheader("Memorial de Cálculo e Tabela de Referência")
        
        # ---------------------------------------------------------
        # MEMORIAL 1: VAZÃO DE PROJETO
        # ---------------------------------------------------------
        st.markdown("#### 1. Vazão de Projeto ($Q_{proj}$)")
        q_proj3 = (i_pluv3 * area_c3) / 60.0
        
        st.markdown("**1. Símbolos e Valores:**")
        st.markdown(f"- $I = {i_pluv3:.2f}$ mm/h")
        st.markdown(f"- $A = {area_c3:.2f}$ m²")
        
        st.markdown("**2. Fórmula:**")
        st.latex(r"Q_{proj} = \frac{I \cdot A}{60}")
        
        st.markdown("**3. Substituição na Fórmula:**")
        st.latex(f"Q_{{proj}} = \\frac{{{i_pluv3:.2f} \\cdot {area_c3:.2f}}}{{60}}")
        
        st.markdown("**4. Resultado:**")
        st.success(f"$Q_{{proj}} = {q_proj3:.2f}$ L/min")
        
        st.markdown("---")
        
        # ---------------------------------------------------------
        # MEMORIAL 2: CAPACIDADE TABELA 4 E CORREÇÃO
        # ---------------------------------------------------------
        st.markdown(f"#### 2. Capacidade Corrigida (Item 5.7.2.2)")
        
        dados_tabela4_base = {
            "Diâmetro (mm)": [50, 75, 100, 125, 150, 200, 250, 300],
            "0,5%": [32.0, 95.0, 204.0, 370.0, 602.0, 1310.0, 2390.0, 3890.0],
            "1%": [45.0, 133.0, 287.0, 521.0, 847.0, 1840.0, 3370.0, 5490.0],
            "2%": [64.0, 188.0, 405.0, 735.0, 1190.0, 2600.0, 4770.0, 7760.0],
            "4%": [90.0, 267.0, 575.0, 1040.0, 1680.0, 3680.0, 6740.0, 10900.0]
        }
        df_tab4 = pd.DataFrame(dados_tabela4_base)
        
        df_exibicao = df_tab4.copy()
        for col in ["0,5%", "1%", "2%", "4%"]:
            df_exibicao[col] = (df_exibicao[col] * fator_correcao).round(2)
            
        st.markdown(f"**Tabela Exibida:** Valores já multiplicados pelo fator de ajuste do material ($n = {n_escolhido:.3f}$).")
        st.dataframe(df_exibicao, hide_index=True)
        
        idx_tubo = df_tab4.index[df_tab4['Diâmetro (mm)'] == diametro_tubo].tolist()[0]
        q_base_tabela = df_tab4.at[idx_tubo, declividade_h]
        
        q_corrigida = q_base_tabela * fator_correcao
        capacidade_total = q_corrigida * num_tubos
        
        st.markdown("**1. Símbolos e Valores Adotados:**")
        st.markdown(f"- $DN = {diametro_tubo}$ mm (Diâmetro)")
        st.markdown(f"- $i = {declividade_h}$ (Declividade)")
        st.markdown(f"- $n = {n_escolhido:.3f}$ (Rugosidade do material)")
        st.markdown(f"- $Q_{{base}} = {q_base_tabela:.2f}$ L/min (Vazão original da Tabela 4 para $n=0,011$)")
        st.markdown(f"- $\\text{{Tubos}} = {num_tubos}$ (Quantidade de tubos paralelos)")
        
        st.markdown("**2. Fórmulas:**")
        st.latex(r"Q_{corrigida} = Q_{base} \cdot \left(\frac{0,011}{n}\right)")
        st.latex(r"Q_{total} = Q_{corrigida} \cdot \text{Tubos}")
        
        st.markdown("**3. Substituição nas Fórmulas:**")
        st.latex(f"Q_{{corrigida}} = {q_base_tabela:.2f} \\cdot \\left(\\frac{{0,011}}{{{n_escolhido:.3f}}}\\right) = {q_corrigida:.2f} \\text{{ L/min}}")
        st.latex(f"Q_{{total}} = {q_corrigida:.2f} \\cdot {num_tubos}")
        
        st.markdown("**4. Resultado Final:**")
        st.success(f"$Q_{{total}} = {capacidade_total:.2f}$ L/min")
        
        st.markdown("---")
        
        if capacidade_total >= q_proj3:
            st.info(f"✅ **CONFORMIDADE ATENDIDA:** A capacidade instalada ({capacidade_total:.2f} L/min) é suficiente.")
        else:
            st.error(f"❌ **NÃO ATENDE:** A capacidade instalada ({capacidade_total:.2f} L/min) é inferior à vazão ({q_proj3:.2f} L/min).")

        txt_horiz = f"""MEMORIAL DE CALCULO - CONDUTORES HORIZONTAIS
Norma de Referencia: NBR 10844/1989

--------------------------------------------------
1. VAZAO DE PROJETO (Q_proj)
--------------------------------------------------
--- Simbolos ---
I = {i_pluv3:.2f} mm/h
A = {area_c3:.2f} m2

--- Formula ---
Q_proj = (I * A) / 60

--- Substituicao ---
Q_proj = ({i_pluv3:.2f} * {area_c3:.2f}) / 60

--- Resultado ---
Q_proj = {q_proj3:.2f} L/min


--------------------------------------------------
2. CAPACIDADE DOS CONDUTORES (TABELA 4)
--------------------------------------------------
--- Simbolos ---
Diametro Adotado (DN): {diametro_tubo} mm
Declividade (i): {declividade_h}
Material (n): {n_escolhido:.3f}
Q_base (Tabela 4 p/ n=0.011): {q_base_tabela:.2f} L/min
Quantidade de tubos: {num_tubos}

--- Fórmulas ---
Q_corrigida = Q_base * (0.011 / n)
Q_total = Q_corrigida * Quantidade

--- Substituicao ---
Q_corrigida = {q_base_tabela:.2f} * (0.011 / {n_escolhido:.3f}) = {q_corrigida:.2f}
Q_total = {q_corrigida:.2f} * {num_tubos}

--- Resultado ---
Q_total = {capacidade_total:.2f} L/min

Status Final: {"ATENDE" if capacidade_total >= q_proj3 else "NAO ATENDE"}
"""
        st.download_button("📄 Baixar Memorial dos Horizontais (TXT)", data=txt_horiz, file_name="memorial_horizontais.txt")