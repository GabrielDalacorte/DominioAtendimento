consult_empregados = """
SELECT 
	e.codi_emp,e.i_empregados as codigo,e.nome,e.cpf,e.cart_prof,e.admissao, e.serie_cart_prof,e.i_cargos,e.i_depto, d.nome as departamento, e.i_filiais, 
	c.nome as cargo, c.CBO_2002 as CBO,
	f.cgc, f.razao_social as nome_filial, f.TIPO_INSC,
	foccusto.nome as centro_custo,
	CASE e.categoria
		WHEN 1  THEN 'Mensalista' 
		WHEN 2  THEN 'Quinzenalista'
		WHEN 3  THEN 'Semanalista'
		WHEN 4  THEN 'Diarista'
		WHEN 5  THEN 'Horista'
		WHEN 6  THEN 'Tarefeiro'
		WHEN 7  THEN 'Comissionado'
		WHEN 8  THEN 'Diretor'
	ELSE ''
	END AS categoria,
/* Considera a situacao do empregado na data informada logo abaixo no codigo */
	 datasituacao = ( SELECT MAX( bethadba.fosituacoes.data_real ) 
					   FROM bethadba.fosituacoes   
					  WHERE ( bethadba.fosituacoes.codi_emp     = e.codi_emp     )
						AND ( bethadba.fosituacoes.i_empregados = e.i_empregados )
						AND ( bethadba.fosituacoes.data_real    = ( SELECT MAX( sit.data_real ) 
																	  FROM bethadba.fosituacoes sit 
																   WHERE ( sit.codi_emp     = e.codi_emp     ) 
																	 AND ( sit.i_empregados = e.i_empregados )
																	 AND ( sit.data_real < months(DATE('2023-01-01'),1) ) 
					))),

	situacao = isNull( ( SELECT MAX( bethadba.fosituacoes.nova_situacao ) 
						   FROM bethadba.fosituacoes   
						  WHERE ( bethadba.fosituacoes.codi_emp     = e.codi_emp ) 
							AND ( bethadba.fosituacoes.i_empregados = e.i_empregados )
							AND ( bethadba.fosituacoes.data_real    = datasituacao )
						),1 ),
	CASE situacao 
		WHEN 1 THEN 'TRABALHANDO'
		WHEN 8 THEN 'DEMITIDO'
	END AS nome_situcao,
	e.forma_pagto,
	CASE e.forma_pagto 
		WHEN 'C' THEN 'CONTA'
		WHEN 'D' THEN 'DINHEIRO'
	END AS nome_forma_pagto,
	b.numero,b.nome as banco, b.agencia, e.conta_corr,e.DIGITO_CONTA_PAGAMENTO as dig_conta_corr

FROM bethadba.foempregados e 
INNER JOIN bethadba.focargos c on c.codi_emp = e.codi_emp and c.i_cargos = e.i_cargos 
INNER JOIN bethadba.fodepto d on d.codi_emp = e.codi_emp and d.i_depto = e.i_depto 
INNER JOIN bethadba.fofiliais f on f.i_filiais = e.i_filiais and f.codi_emp = e.codi_emp
INNER JOIN bethadba.foccustos foccusto on foccusto.codi_emp = e.codi_emp and foccusto.i_ccustos = e.i_ccustos 
LEFT JOIN bethadba.fobancos b on b.i_bancos = e.i_bancos 


/* Se quisermos um empresa em específico */
WHERE e.codi_emp IN (1716)
/* Se quisermos empregados de uma competencia específica */
AND EXISTS (SELECT * FROM bethadba.FOMOVTO mov WHERE mov.CODI_EMP = e.codi_emp AND mov.TIPO_PROCES = 41 and mov."DATA" = '2023-01-01' AND mov.I_EMPREGADOS = e.i_empregados)
"""

consult_rubrics = """
SELECT 
	mov.codi_emp,mov.i_empregados,mov.DATA,mov.TIPO_PROCES,mov.I_EVENTOS,mov.VALOR_INF,mov.VALOR_INF_COMPL,mov.VALOR_CAL,
	mov.ORIGEM,ev.nome as evento, ev.classificacao  
FROM bethadba.FOMOVTO mov 
INNER JOIN bethadba.foeventos ev on ev.codi_emp = mov.CODI_EMP and ev.i_eventos = mov.I_EVENTOS AND ev.aparece_recibo = 'S'
WHERE mov.data BETWEEN '2023-01-01' AND '2023-01-31'
/* Caso queira selecionar apenas uma empresa */
AND mov.CODI_EMP = 1716
"""

consult_recibo_calculo_base = """
SELECT 
	bs.CODI_EMP,
	bs.I_EMPREGADOS,
	bs.COMPETENCIA,
	bs.SALARIO_MES,
	(SELECT SUM( bases.BASE - bases.ABATIMENTOS - bases.DEPEND_DESCONTO - bases.BASE_DESC_LEI )
		FROM bethadba.FOVBASESSERVIRRF bases 
		WHERE bases.CODI_EMP = bs.codi_emp
		AND bases.I_EMPREGADOS = bs.i_empregados
		AND bases.COMPETENCIA = bs.competencia
		AND bases.RATEIO = 0) as base_irrf,
	bs.TAXA_IRRF,
	(bs.proventos - bs.DESCONTOS) as LIQUIDO,
	bs.PROVENTOS,
	bs.DESCONTOS,
	bs.TIPO_PROCESS,
	bs.I_CALCULOS,
    empregado.SALARIO,
	(SELECT SUM(fbases.base)
		FROM bethadba.FOVCALCULOSBASES fbases
		WHERE fbases.i_calculos = bs.i_calculos
		AND fbases.I_CADBASES IN (9, 10, 11, - 1, - 2, 29, 30, 47, 48, 49)) as BASE_INSS,
	(SELECT SUM(fbases.base)
		FROM bethadba.FOVCALCULOSBASES fbases
		WHERE fbases.i_calculos = bs.i_calculos
		AND fbases.I_CADBASES IN ( 15, 16, 17, 31, 32 )) as BASE_FGTS,
	(SELECT SUM(fbases.valor)
		FROM bethadba.FOVCALCULOSBASES fbases
		WHERE fbases.i_calculos = bs.i_calculos
		AND fbases.I_CADBASES IN ( 15, 16, 17, 31, 32 )) as FGTS_MES
	FROM bethadba.FOVBASES bs
    INNER JOIN bethadba.foempregados empregado ON (empregado.codi_emp = bs.codi_emp AND empregado.i_empregados = bs.i_empregados)
WHERE bs.COMPETENCIA = '2023-01-01' /* se for necessário competencia deve ser selecionado ou deve ser igualada a 1 para que venham todos os registros */
/* Caso queira selecionar alguma empresa */
AND bs.codi_emp = 1716
AND bs.TIPO_PROCESS = 41
"""


MAP_YEARS = {
    '01': 'JAN',
    '02': 'FEV',
    '03': 'MAR',
    '04': 'ABR',
    '05': 'MAI',
    '06': 'JUN',
    '07': 'JUL',
    '08': 'AGO',
    '09': 'SET',
    '10': 'OUT',
    '11': 'NOV',
    '12': 'DEZ',
}

