# -*- coding: utf-8 -*-
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
D=json.load(open("dados.json")); META=D["meta"]; R=json.load(open("ref.json"))
COMPS=[m["competencia"] for m in META]
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=14,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); AZ=Font(name=F,size=10,color="0000FF")
VM=Font(name=F,size=10,bold=True,color="C00000")
ALERT=PatternFill("solid",fgColor="FCE4E4"); OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC")
THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; R4='R$ 0.0000'; KW='#,##0;[Red](#,##0);-'; PC='0.0%'
BL=R["base_last"]; B="Base_Lancamentos!"; TR=R["tot_rel"]; CT=R["clientes_tot"]; IF_,IL=R["inad_first"],R["inad_last"]
NM=len(META)
FATCOL=get_column_letter(6+NM); STATCOL=get_column_letter(5+NM)
def head(ws,t,s=None):
    ws["A1"]=t; ws["A1"].font=TIT
    if s: ws["A2"]=s; ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
    return 4
def hrow(ws,r,cols,widths=None):
    for i,c in enumerate(cols,1):
        c_=ws.cell(r,i,c); c_.font=H; c_.fill=HF; c_.border=THIN
        c_.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    if widths:
        for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w

# ===================== INDICADORES =====================
ws=wb.create_sheet("Indicadores")
r0=head(ws,"Indicadores do período (jan a out/2026, série completa)",
        "Tudo calculado a partir da aba Base_Lancamentos. Nenhum número digitado.")
hrow(ws,r0,["Indicador","Valor","Como é calculado / o que significa"],[46,18,78])
ind=[("Faturamento bruto emitido no período (competência corrente)",
      f'=SUMIFS({B}$K$5:$K${BL},{B}$D$5:$D${BL},"corrente")',R2,
      "Soma dos boletos do próprio mês nos 9 relatórios. Exclui recobrança de meses anteriores."),
     ("Faturamento médio mensal",f"=B5/{NM}",R2,"Base de comparação para medir a queda que vem pela frente."),
     ("kWh compensados no período",f"=SUM({B}$F$5:$F${BL})",KW,"Energia que efetivamente abateu conta de cliente."),
     ("Preço médio cobrado por kWh compensado","=IFERROR(B5/B7,0)",R4,"Receita por unidade de energia entregue."),
     ("Recebido no período (caixa)",f"=SUM({B}$L$5:$L${BL})",R2,"Inclui recuperação de meses anteriores e juros."),
     ("Taxa de recebimento sobre tudo que foi cobrado",f"=IFERROR(B9/SUM({B}$K$5:$K${BL}),0)",PC,
      "Faturado aqui inclui recobranças, por isso o indicador é conservador."),
     ("Administração paga à Bro",f"=Relatorios!$J${TR}",R2,"10,0% do valor pago, confirmado nos 9 meses."),
     ("Administração sobre o caixa recebido","=IFERROR(B11/B9,0)",PC,"Confirma a alíquota efetiva de 10%."),
     ("Fatura da concessionária deduzida",f"=Relatorios!$K${TR}",R2,"Valor retido antes do repasse."),
     ("REPASSE LÍQUIDO RECEBIDO PELA LF",f"=Relatorios!$L${TR}",R2,"O que de fato entrou na LF Agropastoril em 9 meses."),
     ("Repasse médio mensal",f"=B14/{NM}",R2,"Ritmo atual de geração de caixa."),
     ("Repasse por kWh compensado","=IFERROR(B14/B7,0)",R4,"Margem líquida por unidade de energia."),
     ("Juros e acréscimos recebidos por atraso",f"=SUM(Inadimplencia!$H${IF_}:$H${IL})",R2,
      "Receita que só existe porque há inadimplência — não é performance comercial."),
     ("Desconto médio concedido ao cliente (ponderado por kWh)",
      f"=IFERROR(1-SUMPRODUCT({B}$J$5:$J${BL},{B}$F$5:$F${BL})/SUMPRODUCT({B}$I$5:$I${BL},{B}$F$5:$F${BL}),0)",PC,
      "Quanto o cliente economiza contra a tarifa CEMIG. É o custo comercial do negócio."),
     ("Concentração do maior cliente no faturamento",
      f"=IFERROR(MAX(Clientes_Comparativo!${FATCOL}$5:${FATCOL}${CT})/SUM(Clientes_Comparativo!${FATCOL}$5:${FATCOL}${CT}),0)",PC,
      "Risco de carteira: perder esta UC derruba o negócio."),
     ("UCs ativas em jan/26",f'=COUNTIFS({B}$A$5:$A${BL},"2026-01",{B}$D$5:$D${BL},"corrente")','0',"Tamanho inicial da carteira."),
     ("UCs ativas em out/26",f'=COUNTIFS({B}$A$5:$A${BL},"2026-10",{B}$D$5:$D${BL},"corrente")','0',"Tamanho final da carteira."),
     ("Variação da carteira no período","=IFERROR(B20/B19-1,0)",PC,"Zero entradas, duas saídas."),
     ]
r=r0+1
for nome,f_,fmt,expl in ind:
    ws.cell(r,1,nome).font=NB if "REPASSE" in nome else N
    cc=ws.cell(r,2,f_); cc.number_format=fmt
    cc.font=VM if "REPASSE" in nome else N
    if "REPASSE" in nome: cc.fill=OKF
    ws.cell(r,3,expl).font=Font(name=F,size=9,color="404040")
    r+=1

# ===================== PERGUNTAS À BRO =====================
ws=wb.create_sheet("Perguntas_Bro")
r0=head(ws,"Perguntas para a vendedora/gestora de energia (Bro)",
        "Cada pergunta nasce de um número desta planilha. A coluna 'Evidência' é o que sustenta a cobrança.")
hrow(ws,r0,["#","Prioridade","Pergunta","Evidência nos relatórios","O que muda na decisão"],[5,12,62,56,52])
P=[("CRÍTICA","Qual a geração medida em cada inversor, mês a mês, contra a energia alocada nos relatórios?","O relatório mostra alocação por UC, nunca a geração da usina.","Um inversor ficou parado e isso não aparece em nenhum relatório. Hoje não há como auditar perda de geração."),
   ("CRÍTICA","Por que nenhum relatório sinalizou que a usina estava gerando pela metade?","Injeção caiu de 13.600 kWh (set) para 5.801 kWh (out) sem uma linha de comentário.","A gestão da usina é nossa, mas quem vê a curva de geração todo mês é a Bro. Um alerta teria antecipado o reparo."),
   ("ALTA","Houve expiração de créditos durante o período de geração reduzida?","Saldo total caiu de 36.430 para 7.823 kWh; a UC 3014144595 zerou.","Crédito de GD expira em 60 meses. Precisamos saber se perdemos algum."),
   ("CRÍTICA","A UC 3014144595 fechou outubro com saldo ZERO. Qual o plano quando o estoque de créditos acabar?","Saldo caiu de 26.548 kWh (jan) para 0 (out).","Sem estoque, a compensação cai ao nível da injeção e o faturamento cai junto — em nov/dez."),
   ("ALTA",'Por que a observação mudou de "Fatura CEMIG paga pela Bro" para "Fatura CEMIG retida" a partir de junho/2026?',"Campo Observações dos relatórios jan–mai contra jun–out.","Se há fatura CEMIG retida e não paga, existe passivo se acumulando em nome da LF."),
   ("ALTA","Qual é o contrato vigente com a Bro: prazo, rescisão, exclusividade e de quem é a carteira de clientes?","Nenhum contrato foi apresentado junto com os relatórios.","Se a carteira é da Bro, a LF não tem ativo comercial — só um fluxo que pode ser desligado."),
   ("ALTA","Zero clientes novos em 9 relatórios. Qual é o pipeline e quem responde pela captação?","Aba Clientes_Comparativo: nenhuma entrada, duas saídas.","Define se o contrato com a Bro inclui obrigação comercial ou é só cobrança."),
   ("ALTA","Qual o critério de rateio dos créditos entre as UCs e onde está formalizado?","A alocação por UC varia muito mês a mês sem explicação.","É o que determina quem recebe benefício — e hoje ninguém consegue conferir."),
   ("ALTA","A administração de 10% incide sobre o recebido. Que esforço de cobrança a Bro assume em troca?","10,0% do valor pago nos 9 meses, confirmado.","Hoje a LF absorve 100% do risco de inadimplência e paga 10% mesmo assim."),
   ("MÉDIA","Por que o desconto ao cliente varia de ~20% a ~38% sem política aparente?","Tarifa Consórcio contra tarifa CEMIG, por UC, na aba Base.","O maior cliente tem o maior desconto e o pior histórico de pagamento."),
   ("MÉDIA","Out/26, UC 3003617528: tarifa CEMIG registrada em R$ 0,9336 contra R$ 1,1726 das demais. Erro ou mudança de classe?","Linha da UC 3003617528 no relatório de outubro.","Se for erro, o boleto saiu menor do que devia."),
   ("MÉDIA","A UC 3012593143 ficou 5 meses com 0 kWh compensado, saldo parado em 732 kWh, e sumiu. O que houve com esses créditos?","Relatórios jan a jun/26.","732 kWh podem ter sido perdidos por expiração."),
   ("MÉDIA","A UC 3012693035 saiu em agosto. Foi cancelamento, migração ou corte por inadimplência?","Último relatório com a UC: jul/26.","Define se existe problema de retenção a tratar."),
   ("MÉDIA","A dívida de R$ 30,66 da UC 3002347701 está em aberto desde ago/2025. Cobrar ou baixar?","Aparece nos 9 relatórios sem baixa.","Valor irrelevante, mas sinaliza que ninguém encerra pendência."),
   ("MÉDIA","Os juros cobrados nos atrasos ficam com quem?","R$ 3.271,93 de acréscimos no período (aba Indicadores).","Se não entram no repasse, há receita saindo da LF sem contrato."),
   ]
r=r0+1
for i,(pr,q,ev,dec) in enumerate(P,1):
    ws.cell(r,1,i).font=N
    cc=ws.cell(r,2,pr); cc.font=VM if pr=="CRÍTICA" else NB
    cc.fill=ALERT if pr=="CRÍTICA" else (WARN if pr=="ALTA" else PatternFill())
    cc.alignment=Alignment(horizontal="center")
    for ci,t in [(3,q),(4,ev),(5,dec)]:
        c_=ws.cell(r,ci,t); c_.font=N if ci==3 else Font(name=F,size=9,color="404040")
        c_.alignment=Alignment(wrap_text=True,vertical="top")
    ws.row_dimensions[r].height=32
    r+=1

# ===================== PLANO DE AÇÃO =====================
ws=wb.create_sheet("Plano_de_Acao")
r0=head(ws,"Plano de ação — o que fazer com o que esta planilha mostrou",
        "Ordenado por impacto financeiro, não por facilidade.")
hrow(ws,r0,["#","Prazo","Ação","Por quê","Impacto estimado"],[5,14,62,62,30])
A=[("Até 7 dias","Cobrar formalmente a UC 3014144595 (R$ 5.422,69 de out/26).","É 52% do faturamento do mês e repete atraso desde dez/25.","R$ 5.422,69 de caixa imediato"),
   ("Até 7 dias","Confirmar no relatório de novembro que a injeção voltou ao patamar de 11.000 a 13.000 kWh.","O inversor parado já foi reparado; falta comprovar a recuperação no número.","Confirma ~R$ 4.000/mês de receita"),
   ("Até 15 dias","Quantificar a energia não gerada enquanto um inversor esteve parado.","É receita que nunca foi faturada e que ninguém mediu.","Dimensiona a perda real"),
   ("Até 15 dias","Trocar o indicador de inadimplência: passar a medir faturado x recebido do próprio mês.","O indicador do relatório subdeclara a dívida em 19,5x.","Evita decisão com número errado"),
   ("Até 30 dias","Renegociar a UC 3014144595: garantia, débito automático ou redução do desconto de 38%.","Maior cliente, maior desconto e pior pagador ao mesmo tempo.","Reduz risco de 52% da carteira"),
   ("Até 30 dias","Obter e ler o contrato com a Bro; definir de quem é a carteira de clientes.","Sem isso não se sabe se existe ativo comercial ou só um fluxo.","Define o valor do negócio"),
   ("Até 30 dias","Plano comercial para repor as 2 UCs perdidas e ocupar o estoque ocioso.","Zero entradas em 9 meses; a regra de 50% no 1º mês nunca foi usada.","Recompõe ~13% da carteira"),
   ("Até 30 dias","Baixar contabilmente os R$ 30,66 de ago/25 ou cobrar.","Pendência de 15 meses poluindo o relatório.","Higiene de controle"),
   ("Até 60 dias","Decidir o destino da receita: ela entra na LF Agropastoril, mas o ativo é da Fotovolt Curral Novo SPE.","9 meses e R$ 67.638,47 de repasse foram para uma empresa que não é a dona da usina.","Risco societário e fiscal"),
   ("Até 60 dias","Formalizar o contrato entre a SPE (dona do ativo) e quem explora a energia.","Hoje não existe instrumento entre as duas pontas.","Protege os 5 sócios"),
   ("Até 90 dias","Padronizar a política de desconto por faixa de consumo e risco.","Descontos variam de 20% a 38% sem critério visível.","Recupera margem"),
   ("Contínuo","Atualizar esta planilha a cada relatório recebido.","A série mensal é o único histórico estruturado que existe hoje.","Base para valuation da SPE"),
   ]
r=r0+1
for i,(pz,ac,pq,imp) in enumerate(A,1):
    ws.cell(r,1,i).font=N
    cc=ws.cell(r,2,pz); cc.font=NB; cc.alignment=Alignment(horizontal="center")
    if "7 dias" in pz: cc.fill=ALERT
    elif "15 dias" in pz: cc.fill=WARN
    for ci,t in [(3,ac),(4,pq),(5,imp)]:
        c_=ws.cell(r,ci,t); c_.font=N if ci==3 else Font(name=F,size=9,color="404040")
        c_.alignment=Alignment(wrap_text=True,vertical="top")
    ws.row_dimensions[r].height=30
    r+=1
wb.save(OUT); print("ok parte 3")
