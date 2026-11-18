# -*- coding: utf-8 -*-
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
R=json.load(open("ref.json")); TR=R["tot_rel"]
import json as _j; NM=len(_j.load(open("dados.json"))["meta"])
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=14,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
AZ=Font(name=F,size=10,color="0000FF"); VD=Font(name=F,size=10,color="008000")
VM=Font(name=F,size=10,bold=True,color="C00000")
ALERT=PatternFill("solid",fgColor="FCE4E4"); OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC")
THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; KW='#,##0'; PC='0.00%'; PC1='0.0%'

ws=wb.create_sheet("Contrato_Bro")
for col,w in [("A",50),("B",18),("C",18),("D",18),("E",62)]: ws.column_dimensions[col].width=w
ws["A1"]="Cálculo com a Bro Energy — contrato GD-074-02-24 contra o que foi praticado"
ws["A1"].font=TIT
ws["A2"]="Contratante no papel: AGRO PASTORIL DOS POCOES LTDA (19.605.278/0001-10). Contratada: BRO ENERGY GESTÃO DE ENERGIA LTDA (29.118.895/0001-45). Assinado 07/03/2024, vigência 5 anos."
ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
ws["A3"]="ATENÇÃO — ESTA ABA ESTÁ SUSPENSA. O sócio confirmou em 18/11/2026 que o GD-074-02-24 é de OUTRA empresa e NÃO rege esta usina. O contrato correto com a Bro Energy será providenciado. Até lá, NÃO use nenhum número desta aba e NÃO cite estas cláusulas com a Bro."
ws["A3"].font=Font(name=F,size=11,bold=True,color="C00000")
ws["A3"].fill=PatternFill("solid",fgColor="FCE4E4")
ws.row_dimensions[3].height=30
r=5

def bloco(t):
    global r
    c=ws.cell(r,1,t); c.font=SUB; r+=1
def head5(cols):
    global r
    for i,c in enumerate(cols,1):
        x=ws.cell(r,i,c); x.font=H; x.fill=HF; x.border=THIN
        x.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    r+=1
def linha(a,b=None,c=None,d=None,e=None,fmt=R2,fonte=None,fill=None):
    global r
    ws.cell(r,1,a).font=fonte or N
    for ci,v in [(2,b),(3,c),(4,d)]:
        if v is not None:
            x=ws.cell(r,ci,v); x.font=fonte or N; x.number_format=fmt
            if fill: x.fill=fill
    if e is not None: ws.cell(r,5,e).font=SM
    r+=1

# ---- BLOCO 1
bloco("1. Quem assina, quem recebe e quem é dono — três empresas diferentes")
head5(["Papel no negócio","CNPJ","","","Empresa / prova documental"])
for papel,cnpj,emp in [
 ("Dona dos equipamentos (UFV)","51.245.620/0001-21",'FOTOVOLT CURRAL NOVO SPE LTDA — informação do sócio'),
 ("Assina o contrato com a Bro","19.605.278/0001-10",'AGRO PASTORIL DOS POCOES LTDA — preâmbulo do GD-074'),
 ("Recebe relatório e repasse","—",'LF AGROPASTORIL LTDA — 9 relatórios mensais de 2026')]:
    ws.cell(r,1,papel).font=N; ws.cell(r,2,cnpj).font=N; ws.cell(r,5,emp).font=SM
    ws.cell(r,1).fill=ALERT; r+=1
linha('O contrato declara que a CONTRATANTE "é detentora do imóvel rural e suas respectivas instalações de SGE".',
      e='Se a usina é da SPE, essa declaração (cl. 10.1) está incorreta.',fonte=VM)
r+=1

# ---- BLOCO 2
bloco("2. Remuneração da Bro — contrato contra praticado")
head5(["Item","Base do contrato","Valor praticado","Diferença","Cláusula e leitura"])
linha("Faturamento bruto RECEBIDO dos consumidores (9 meses)",f"=Indicadores!$B$9",None,None,
      e="Soma de tudo que os consumidores pagaram no período.")
linha("Taxa de Administração — 10% do recebido (cl. 2.1 B)","=B7*0.10",f"=Relatorios!$J${TR}","=C8-B8",
      e="A Bro aplica esta leitura. Confere com os 9 relatórios.")
ws.cell(r-1,4).fill=OKF
linha("Taxa Inicial — 50% do 1º faturamento de cada novo consumidor (cl. 2.1 A)",0,0,0,
      e="Zero clientes novos no período, logo nada cobrado — e nenhuma captação entregue.")
linha("Total retido pela Bro no período",f"=C8+C9",None,None,e="Custo da gestão comercial.")
r+=1
linha("LEITURA ALTERNATIVA DA CLÁUSULA 2.2 — risco em aberto",fonte=VM)
linha("Faturamento total EMITIDO (inclui recobranças)",f"=SUM(Base_Lancamentos!$K$5:$K${R['base_last']})",None,None,
      e="A cl. 2.2 define a taxa sobre energia compensada, independentemente do pagamento.")
linha("10% sobre o emitido","=B13*0.10",None,None,e="Quanto a Bro poderia cobrar com a outra leitura.")
linha("EXPOSIÇÃO se a Bro passar a aplicar a cl. 2.2","=B14-C8",None,None,
      e="O contrato se contradiz: cl. 2.1(B) diz 'recebido', cl. 2.2 diz 'independentemente do pagamento'.",
      fonte=VM,fill=ALERT)
r+=1

# ---- BLOCO 3
bloco("3. Parcela Fixa de Locação de R$ 1.000,00/mês — prevista no contrato, ausente dos relatórios")
head5(["Item","Valor","","","Observação"])
linha("Parcela Fixa mensal prevista (cl. 2.2)",1000.00,None,None,
      e="\"Valor fixo mensal de R$1.000,00 conforme definido no contrato de locação firmado pela CONTRATANTE e o consórcio de energia\".",fonte=AZ)
linha("Meses analisados",NM,None,None,fmt='0',e="jan a out/2026, série completa.",fonte=AZ)
linha("Valor que deveria ter sido faturado como LOCAÇÃO","=B18*B19",None,None,
      e="Nenhum relatório mensal traz esta linha.",fill=WARN,fonte=NB)
linha("Na fórmula do contrato a Parcela Fixa é subtraída e somada de volta.",None,None,None,
      e="Portanto NÃO É DINHEIRO FALTANDO: é documento faltando. O total recebido é o mesmo.")
linha("O que falta de fato: o contrato de locação da usina com o consórcio.",None,None,None,
      e="É esse contrato que dá base legal ao rótulo \"aluguel de equipamento\". Ele nunca foi apresentado.",fonte=VM)
r+=1

# ---- BLOCO 4
bloco("4. Base tributável da locação — o contrato define base maior que o dinheiro que entra")
head5(["Item","Valor","","","Fundamento"])
linha("Contribuições pagas pelos consumidores","=Indicadores!$B$9",None,None,e="Entrada bruta do ciclo.")
linha("(−) Custos da Distribuidora",f"=-Relatorios!$K${TR}",None,None,e="Único item que o contrato manda deduzir da base.")
linha("= REMUNERAÇÃO TOTAL DA LOCAÇÃO (base de cálculo dos tributos)","=B25+B26",None,None,
      e="Cláusula 2.2: \"base de cálculo para apuração dos tributos sobre a locação\".",fonte=NB,fill=WARN)
linha("Valor que efetivamente entrou na conta (repasse)",f"=Relatorios!$L${TR}",None,None,e="Aba Relatorios.")
linha("Diferença entre a base tributável e o que entrou","=B27-B28",None,None,
      e="É a taxa de administração. Ela é DESPESA, não redução de receita.",fonte=VM)
r+=1
linha("Estimativa de tributos — Lucro Presumido, locação de bens móveis. CONFIRMAR COM O CONTADOR.",fonte=VM)
head5(["Tributo","Alíquota efetiva","Sobre a base correta","Sobre o repasse","Observação"])
aliq=[("PIS (cumulativo)",0.0065,"Regime cumulativo do Lucro Presumido."),
      ("COFINS (cumulativo)",0.0300,"Regime cumulativo do Lucro Presumido."),
      ("IRPJ (15% sobre presunção de 32%)",0.0480,"Presunção de 32% aplicável a locação de bens móveis."),
      ("CSLL (9% sobre presunção de 32%)",0.0288,"Presunção de 32% aplicável a locação de bens móveis."),
      ("ISS",0.0000,"Locação de bem móvel não sofre ISS — Súmula Vinculante 31 do STF.")]
first_t=r
for nome,a,obs in aliq:
    ws.cell(r,1,nome).font=N
    x=ws.cell(r,2,a); x.font=AZ; x.number_format=PC
    x=ws.cell(r,3,f"=$B${27}*B{r}"); x.font=N; x.number_format=R2
    x=ws.cell(r,4,f"=$B${28}*B{r}"); x.font=N; x.number_format=R2
    ws.cell(r,5,obs).font=SM
    r+=1
last_t=r-1
ws.cell(r,1,"TOTAL ESTIMADO").font=NB
for ci,L in [(2,"B"),(3,"C"),(4,"D")]:
    x=ws.cell(r,ci,f"=SUM({L}{first_t}:{L}{last_t})"); x.font=NB
    x.number_format=PC if ci==2 else R2
    x.fill=OKF
TOT_T=r; r+=1
linha("Tributo a mais se a base correta for usada",f"=C{TOT_T}-D{TOT_T}",None,None,
      e="Se a apuração vinha sendo feita sobre o valor que entrou na conta, faltou recolher isto em 9 meses.",
      fonte=VM,fill=ALERT)
r+=1

# ---- BLOCO 5
bloco("5. Garantia de geração — cláusula 6.1.7 exige no mínimo 80% da média esperada")
head5(["Competência","Injeção kWh","Piso de 80% kWh","% da média","Situação"])
first_g=r
for i in range(NM):
    er=5+i
    ws.cell(r,1,f"=Energia!$A${er}").font=N
    x=ws.cell(r,2,f"=Energia!$C${er}"); x.font=N; x.number_format=KW
    x=ws.cell(r,3,f"=$B${first_g+NM}*0.8"); x.font=N; x.number_format=KW
    x=ws.cell(r,4,f"=IFERROR(B{r}/$B${first_g+NM},0)"); x.font=N; x.number_format=PC1
    x=ws.cell(r,5,f'=IF(B{r}<C{r},"ABAIXO DO PISO CONTRATUAL","ok")'); x.font=N
    r+=1
ws.cell(r,1,"Média do período").font=NB
x=ws.cell(r,2,f"=AVERAGE(B{first_g}:B{r-1})"); x.font=NB; x.number_format=KW; x.fill=OKF
r+=1
linha("Três meses abaixo do piso: março, agosto e outubro/2026. Outubro ficou em 56% da média.",
      e="Causa conhecida: um dos dois inversores estava parado. O O&M é integralmente nosso (cl. 2.4 e 6.1.6), então o descumprimento é nosso.",fonte=VM)
r+=1

# ---- BLOCO 6
bloco("6. Potência declarada contra geração observada")
head5(["Item","Valor","","","Observação"])
linha("Potência declarada no contrato (cl. 2.1)",37,None,None,fmt=KW,fonte=AZ,e="\"por uma usina de 37K de potência instalada\".")
linha("Geração média mensal observada (kWh)",f"=B{first_g+NM}",None,None,fmt=KW,e="Média dos 10 relatórios, já contaminada pelos meses com um inversor parado.")
linha("Produtividade típica assumida para MG (kWh/kWp/dia)",4.7,None,None,fmt='0.0',fonte=AZ,e="Premissa editável. Ajuste se tiver o dado real da usina.")
linha("Dias por mês",30.4,None,None,fmt='0.0',fonte=AZ)
linha("Potência implícita na geração observada (kWp)",f"=IFERROR(B{r-3}/(B{r-2}*B{r-1}),0)",None,None,fmt=KW,
      e="Muito acima dos 37 kWp do contrato.",fonte=VM,fill=ALERT)
linha("A usina tem DOIS inversores (informação do sócio). Isso reforça que a potência real é muito maior que os 37 kWp do contrato.",fonte=VM)
linha("Pergunta para a Bro: qual a potência registrada na CEMIG para esta UC geradora?",fonte=VM)
r+=1

# ---- BLOCO 7
bloco("7. Janela e custo de saída do contrato")
head5(["Item","Valor","","","Cláusula"])
linha("Assinatura",None,None,None,e="07/03/2024 — cláusula final")
linha("Término da vigência (5 anos)",None,None,None,e="07/03/2029 — cláusula 9.1")
linha("Aviso prévio obrigatório para rescindir",90,None,None,fmt='0" dias"',fonte=AZ,e="Cláusula 8.1")
linha("Faixa de multa em que estamos hoje (mês 32)",None,None,None,
      e="2x a Taxa Inicial paga — faixa do 25º ao 48º mês (cl. 8.1 ii)",fonte=VM)
linha("Sem o aviso de 90 dias",None,None,None,e="3x a Taxa Inicial, independentemente do período (cl. 8.2)",fonte=VM)
linha("Valor da Taxa Inicial efetivamente paga",None,None,None,
      e="PRECISA SER LEVANTADO no histórico 2024-2025. É ele que define se sair é caro ou barato.",fonte=VM,fill=WARN)
linha("Atraso da Bro no repasse",None,None,None,e="2% de multa + 1% ao mês + IPCA (cl. 7.1)")
linha("Descumprimento de cláusula por mais de 20 dias",None,None,None,e="1x a Taxa Inicial (cl. 7.3) — o relatório de fev/26 não entregue se enquadra aqui")
ws.sheet_view.showGridLines=False
ordem=["Leia-me","Relatorios","Clientes_Comparativo","Inadimplencia","Contas_a_Receber",
       "Energia","Indicadores","Contrato_Bro","Perguntas_Bro","Plano_de_Acao","Base_Lancamentos"]
wb._sheets=[wb[s] for s in ordem]
wb.save(OUT); print("Contrato_Bro criada")
