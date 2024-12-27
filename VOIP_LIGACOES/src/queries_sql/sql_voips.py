# Delete all data from VOIP
SQL_DELETE_VOIP = """DELETE FROM CAMPANHAS_VOIP_BASE"""

# get data of the best oerformance from VOIPS
SQL_VOIP_RANKING = """
    SELECT l4.NOME_CAMP_AJUSTADO,
    (SUM(l4.QTD_UNI_TAB_PAC_GUIA) / SUM(l4.QTD_DISCADO_COMPLETOU))*100 AS RESULTADO
    FROM
    (SELECT l3.data_discagem,
        --l3.nome_campanha,
        l3.nome_camp_ajustado,
        l3.sexo,
        l3.grupo_idade,
        --count(distinct ID_CONVERSA) as qtd_uni_cod_whats,
        COUNT(DISTINCT l3.cod_paciente)        AS qtd_discado_geral,
        COUNT(DISTINCT l3.cod_pac_n_completou) AS qtd_discado_n_completou,
        COUNT(DISTINCT l3.cod_pac_completou)   AS qtd_discado_completou,
        COUNT(DISTINCT l3.cod_pac_sistema)     AS qtd_uni_tab_pac_guia,
        COUNT(DISTINCT l3.guia_ajustada)       AS qtd_uni_guias,
        COUNT(DISTINCT l3.qtd_pg_cons)         AS qtd_pg_cons,
        COUNT(DISTINCT l3.qtd_pg_exame)        AS qtd_pg_exame,
        COUNT(DISTINCT l3.qtd_pg_odonto)       AS qtd_pg_odonto,
        COUNT(DISTINCT l3.qtd_pg_lab)          AS qtd_pg_lab,
        SUM(l3.valor_tt_pago)                  AS valor_pago_tt,
        SUM(l3.v_pg_cons_tt)                   AS v_pg_cons_tt,
        SUM(l3.v_pg_exame_tt)                  AS v_pg_exame_tt,
        SUM(l3.v_pg_odonto_tt)                 AS v_pg_odonto_tt,
        SUM(l3.v_pg_lab_tt)                    AS v_pg_lab_tt
    FROM
        (SELECT l2.data_discagem,
        l2.data_janela,
        l2.cpf,
        l2.nome_campanha,
        l2.nome_camp_ajustado,
        l2.fone,
        l2.status,
        CASE
            WHEN l2.status = 'Completou'
            THEN l2.cod_paciente
            ELSE NULL
        END AS cod_pac_completou,
        CASE
            WHEN l2.status <> 'Completou'
            THEN l2.cod_paciente
            ELSE NULL
        END AS cod_pac_n_completou,
        l2.cod_paciente,
        l2.sexo,
        l2.DATA_NASCIMENTO,
        TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) AS Idade,
        CASE
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 0 AND 18
            THEN '01 - 00 A 18 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 19 AND 25
            THEN '02 - 19 A 25 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 26 AND 35
            THEN '03 - 26 A 35 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 36 AND 45
            THEN '04 - 36 A 45 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 46 AND 55
            THEN '05 - 46 A 55 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 56 AND 65
            THEN '06 - 56 A 65 ANOS'
            ELSE '07 - MAIOR QUE 65 ANOS'
        END AS grupo_idade,
        bp.cod_pac_sistema,
        bp.dt_pg,
        bp.v_central,
        bp.v_custo,
        bp.v_total,
        bp.valor_tt_pago,
        bp.grupo,
        bp.especialidade,
        bp.grupo_ajustado,
        bp.procedimento,
        bp.medico,
        bp.guia,
        bp.guia_ajustada,
        CASE
            WHEN bp.grupo_ajustado = 'CONSULTAS'
            THEN bp.guia_ajustada
            ELSE NULL
        END AS qtd_pg_cons,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES'
            THEN bp.guia_ajustada
            ELSE NULL
        END AS qtd_pg_exame,
        CASE
            WHEN bp.grupo_ajustado = 'ODONTOLOGIA'
            THEN bp.guia_ajustada
            ELSE NULL
        END AS qtd_pg_odonto,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES DE LABORATORIO'
            THEN bp.guia_ajustada
            ELSE NULL
        END AS qtd_pg_lab,
        CASE
            WHEN bp.grupo_ajustado = 'CONSULTAS'
            THEN bp.v_custo
            ELSE 0
        END AS v_pg_cons_custo,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES'
            THEN bp.v_custo
            ELSE 0
        END AS v_pg_exame_custo,
        CASE
            WHEN bp.grupo_ajustado = 'ODONTOLOGIA'
            THEN bp.v_custo
            ELSE 0
        END AS v_pg_odonto_custo,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES DE LABORATORIO'
            THEN bp.v_custo
            ELSE 0
        END AS v_pg_lab_custo,
        CASE
            WHEN bp.grupo_ajustado = 'CONSULTAS'
            THEN bp.v_central
            ELSE 0
        END AS v_pg_cons_central,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES'
            THEN bp.v_central
            ELSE 0
        END AS v_pg_exame_central,
        CASE
            WHEN bp.grupo_ajustado = 'ODONTOLOGIA'
            THEN bp.v_central
            ELSE 0
        END AS v_pg_odonto_central,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES DE LABORATORIO'
            THEN bp.v_central
            ELSE 0
        END AS v_pg_lab_central,
        CASE
            WHEN bp.grupo_ajustado = 'CONSULTAS'
            THEN bp.valor_tt_pago
            ELSE 0
        END AS v_pg_cons_tt,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES'
            THEN bp.valor_tt_pago
            ELSE 0
        END AS v_pg_exame_tt,
        CASE
            WHEN bp.grupo_ajustado = 'ODONTOLOGIA'
            THEN bp.valor_tt_pago
            ELSE 0
        END AS v_pg_odonto_tt,
        CASE
            WHEN bp.grupo_ajustado = 'EXAMES DE LABORATORIO'
            THEN bp.valor_tt_pago
            ELSE 0
        END AS v_pg_lab_tt
        FROM
        (SELECT l1.mes_ligacao,
            l1.data_ajustada             AS data_discagem,
            TRUNC(l1.data_ajustada) + 30 AS data_janela,
            l1.cod_paciente              AS CPF,
            l1.nome_campanha,
            l1.NUMERO AS fone,
            l1.status,
            CASE
            WHEN l1.nome_campanha = 'CAMPANHA_INICIO_DE_ANO'
            THEN 'INSTITUCIONAL'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_01_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_01_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_02_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_02_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_03_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_03_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_04_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_04_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_05_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_05_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_06_PRINCIPAL | Voip Psico'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_08_PRINCIPAL | Voip Homem'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_01_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_06_PRINCIPAL | Voip Psico'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'Voip_Campanha_Azenha'
            THEN 'OUTRAS'
            WHEN l1.nome_campanha = 'Voip_Campanha_Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Campanha_Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_CARDIO_NOV_22'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Cardio_Geral'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Homem_Geral'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'Voip_Checkup_Mulher_Geral'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'Voip_Checkup_Mulher_Outubro'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Saude_dez2021'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_HOMEM_NOV_22'
            THEN 'NOVEMBRO AZUL'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO_A'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO_B'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM_A'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM_B'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO_A'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO_B'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_INSTITUCIONAL'
            THEN 'INSTITUCIONAL'
            WHEN l1.nome_campanha = 'VOIP_MULHER_NOV_22'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'Voip_Novembro_azul'
            THEN 'NOVEMBRO AZUL'
            WHEN l1.nome_campanha = 'Voip_Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Odonto_A'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Odonto_B'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_odonto_namorados'
            THEN 'NAMORADOS'
            WHEN l1.nome_campanha = 'VOIP_OFTALMO_NOV_22'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022_A'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022_B'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'Voip_odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_01_PRINCIPAL'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_06_PRINCIPAL'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_07_PRINCIPAL'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_PSICOLOGIA_PSIQUIATRIA'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_ODONTO'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_ODONTO_GERAL'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_PSICOLOGIA_PSIQUIATRIA'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_ODONTO'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_ODONTO_GERAL'
            THEN 'ODONTO'
            ELSE 'VER'
            END                                       AS nome_camp_ajustado,
            NVL(p.cod_paciente,p2.cod_paciente)       AS cod_paciente,
            NVL(p.sexo,p2.sexo)                       AS sexo,
            NVL(p.DATA_NASCIMENTO,p2.DATA_NASCIMENTO) AS DATA_NASCIMENTO
        FROM
            (SELECT to_date('01/'
            || SUBSTR(dxc.data,4,7),'DD/MM/YYYY')            AS mes_ligacao,
            TRUNC(to_Date(dxc.data,'DD/MM/YYYY HH24:MI:SS')) AS data_ajustada,
            to_number(NVL(
            CASE
                WHEN INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') > 0
                THEN SUBSTR( SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') + LENGTH('"cod_paciente":"')),1, INSTR(SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') + LENGTH('"cod_paciente":"')), '"') - 1)
                ELSE NULL
            END,
            CASE
                WHEN INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') > 0
                THEN SUBSTR( SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') + LENGTH('"CPF":"')),1, INSTR(SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') + LENGTH('"CPF":"')), '"') - 1)
                ELSE NULL
            END))        AS cod_paciente,
            dxc.campanha AS nome_campanha,
            dxc.NUMERO,
            dxc.status
            FROM dados_x5_campanhas dxc
            WHERE dxc.campanha LIKE '%VOIP%'
            AND dxc.status                                   = 'Completou'
            AND to_date(SUBSTR(dxc.data,1,10),'DD/MM/YYYY') >= '04/12/2023'
            UNION ALL
            SELECT to_date('01/'
            || TO_CHAR(l.data_discagem,'MM/YYYY'),'DD/MM/YYYY') AS mes_ligacao,
            TRUNC(l.data_discagem)                              AS data_ajustada,
            to_number(l.cpf)                                    AS cod_paciente,
            l.nome_campanha,
            l.fone,
            l.status
            FROM lig_camp_ativas l
            WHERE TRUNC(l.data_discagem) >= '01/01/2023'
            ) l1,
            paciente p,
            paciente p2
        WHERE REPLACE(TO_CHAR(l1.cod_paciente,'00000000000'),' ','') = p.cpf (+)
        AND l1.cod_paciente                                          = p2.cod_paciente (+)
        AND l1.cod_paciente                                         <> 0
        AND NVL(p.cod_paciente,p2.cod_paciente)                     IS NOT NULL
        ) l2,
        ( SELECT DISTINCT bp.cod_paciente AS cod_pac_sistema,
            bp.dt_pg,
            bp.v_central,
            bp.v_custo,
            bp.v_total,
            bp.valor_tt_pago,
            bp.grupo,
            bp.especialidade,
            CASE
            WHEN bp.grupo = 'EXAMES DE LABORATORIO'
            THEN bp.grupo
            WHEN bp.especialidade IN ('EXAMES','ECOGRAFIA','GRAVACAO ECO','COMPLEMENTO','PROCEDIMENTO MÉDICOS','PROCEDIMENTOS','NAO REALIZAMOS','AJUDA - EXAMES')
            THEN 'EXAMES'
                --when bp.especialidade in ('EXAMES','ECOGRAFIA','GRAVACAO ECO','COMPLEMENTO') then bp.especialidade
            ELSE bp.grupo
            END AS grupo_ajustado,
            bp.procedimento,
            bp.medico,
            bp.guia,
            CASE
            WHEN bp.medico = 'LAPROJAL'
            THEN NULL
            ELSE bp.guia
            END AS guia_ajustada
        FROM bi_pagamentos bp
        WHERE bp.status_guia  = 'A'
        AND bp.valor_tt_pago IS NOT NULL
        ) bp
        WHERE l2.cod_paciente = bp.cod_pac_sistema (+)
        AND bp.dt_pg (+) BETWEEN l2.data_discagem AND l2.data_janela
        ) l3
        --where l3.nome_camp_ajustado = 'VER'
    GROUP BY l3.data_discagem,
        --l3.nome_campanha,
        l3.nome_camp_ajustado,
        l3.sexo,
        l3.grupo_idade
    UNION ALL
    SELECT l3.data_discagem,
        --l3.nome_campanha,
        l3.nome_camp_ajustado,
        l3.sexo,
        l3.grupo_idade,
        --count(distinct ID_CONVERSA) as qtd_uni_cod_whats,
        COUNT(DISTINCT l3.cod_paciente)        AS qtd_discado_geral,
        COUNT(DISTINCT l3.cod_pac_n_completou) AS qtd_discado_n_completou,
        COUNT(DISTINCT l3.cod_pac_completou)   AS qtd_discado_completou,
        0                                      AS qtd_uni_tab_pac_guia,
        0                                      AS qtd_uni_guias,
        0                                      AS qtd_pg_cons,
        0                                      AS qtd_pg_exame,
        0                                      AS qtd_pg_odonto,
        0                                      AS qtd_pg_lab,
        SUM(l3.valor_tt_pago)                  AS valor_pago_tt,
        SUM(l3.v_pg_cons_tt)                   AS v_pg_cons_tt,
        SUM(l3.v_pg_exame_tt)                  AS v_pg_exame_tt,
        SUM(l3.v_pg_odonto_tt)                 AS v_pg_odonto_tt,
        SUM(l3.v_pg_lab_tt)                    AS v_pg_lab_tt
    FROM
        (SELECT l2.data_discagem,
        l2.data_janela,
        l2.cpf,
        l2.nome_campanha,
        l2.nome_camp_ajustado,
        l2.fone,
        l2.status,
        CASE
            WHEN l2.status = 'Completou'
            THEN l2.cod_paciente
            ELSE NULL
        END AS cod_pac_completou,
        CASE
            WHEN l2.status <> 'Completou'
            THEN l2.cod_paciente
            ELSE NULL
        END AS cod_pac_n_completou,
        l2.cod_paciente,
        l2.sexo,
        l2.DATA_NASCIMENTO,
        TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) AS Idade,
        CASE
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 0 AND 18
            THEN '01 - 00 A 18 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 19 AND 25
            THEN '02 - 19 A 25 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 26 AND 35
            THEN '03 - 26 A 35 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 36 AND 45
            THEN '04 - 36 A 45 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 46 AND 55
            THEN '05 - 46 A 55 ANOS'
            WHEN TRUNC(Months_between(TRUNC(DATA_DISCAGEM),l2.DATA_NASCIMENTO)/12) BETWEEN 56 AND 65
            THEN '06 - 56 A 65 ANOS'
            ELSE '07 - MAIOR QUE 65 ANOS'
        END AS grupo_idade,
        0   AS cod_pac_sistema,
        0   AS dt_pg,
        0   AS v_central,
        0   AS v_custo,
        0   AS v_total,
        0   AS valor_tt_pago,
        0   AS grupo,
        0   AS especialidade,
        0   AS grupo_ajustado,
        0   AS procedimento,
        0   AS medico,
        0   AS guia,
        0   AS guia_ajustada,
        0   AS qtd_pg_cons,
        0   AS qtd_pg_exame,
        0   AS qtd_pg_odonto,
        0   AS qtd_pg_lab,
        0   AS v_pg_cons_custo,
        0   AS v_pg_exame_custo,
        0   AS v_pg_odonto_custo,
        0   AS v_pg_lab_custo,
        0   AS v_pg_cons_central,
        0   AS v_pg_exame_central,
        0   AS v_pg_odonto_central,
        0   AS v_pg_lab_central,
        0   AS v_pg_cons_tt,
        0   AS v_pg_exame_tt,
        0   AS v_pg_odonto_tt,
        0   AS v_pg_lab_tt
        FROM
        (SELECT l1.mes_ligacao,
            l1.data_ajustada             AS data_discagem,
            TRUNC(l1.data_ajustada) + 30 AS data_janela,
            l1.cod_paciente              AS CPF,
            l1.nome_campanha,
            l1.NUMERO AS fone,
            l1.status,
            CASE
            WHEN l1.nome_campanha = 'CAMPANHA_INICIO_DE_ANO'
            THEN 'INSTITUCIONAL'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_01_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_01_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_02_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_02_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_03_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_03_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_04_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_04_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_05_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_05_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_06_PRINCIPAL | Voip Psico'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_A_Campanha_08_PRINCIPAL | Voip Homem'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_01_PRINCIPAL | CHECKUP SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL | Voip Mulher'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL | Voip Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL | Voip Cardio'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL | Voip Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_06_PRINCIPAL | Voip Psico'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'Voip_Campanha_Azenha'
            THEN 'OUTRAS'
            WHEN l1.nome_campanha = 'Voip_Campanha_Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Campanha_Oftalmo'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_CARDIO_NOV_22'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Cardio_Geral'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Homem_Geral'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'Voip_Checkup_Mulher_Geral'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'Voip_Checkup_Mulher_Outubro'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'Voip_Checkup_Saude_dez2021'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_HOMEM_NOV_22'
            THEN 'NOVEMBRO AZUL'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO_A'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_CARDIO_B'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM_A'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_HOMEM_B'
            THEN 'CHECKUP_HOMEM'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO_A'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_CHECKUP_OFTALMO_B'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_MKT_INSTITUCIONAL'
            THEN 'INSTITUCIONAL'
            WHEN l1.nome_campanha = 'VOIP_MULHER_NOV_22'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'Voip_Novembro_azul'
            THEN 'NOVEMBRO AZUL'
            WHEN l1.nome_campanha = 'Voip_Odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Odonto_A'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_Odonto_B'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'Voip_odonto_namorados'
            THEN 'NAMORADOS'
            WHEN l1.nome_campanha = 'VOIP_OFTALMO_NOV_22'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022_A'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'VOIP_Outubro_Rosa_2022_B'
            THEN 'OUTUBRO ROSA'
            WHEN l1.nome_campanha = 'Voip_odonto'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_01_PRINCIPAL'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_02_PRINCIPAL'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_03_PRINCIPAL'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_04_PRINCIPAL'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_05_PRINCIPAL'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_06_PRINCIPAL'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_Campanha_07_PRINCIPAL'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_PSICOLOGIA_PSIQUIATRIA'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_A_CHECKUP_SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_A_ODONTO'
            THEN 'ODONTO'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_CARDIO'
            THEN 'CARDIOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_MULHER'
            THEN 'CHECKUP_MULHER'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_OFTALMO'
            THEN 'OFTALMOLOGIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_PSICOLOGIA_PSIQUIATRIA'
            THEN 'PSICOLOGO E PSIQUIATRIA'
            WHEN l1.nome_campanha = 'VOIP_B_CHECKUP_SAUDE'
            THEN 'CHECK UP SAUDE'
            WHEN l1.nome_campanha = 'VOIP_B_ODONTO'
            THEN 'ODONTO'
            ELSE 'VER'
            END                                       AS nome_camp_ajustado,
            NVL(p.cod_paciente,p2.cod_paciente)       AS cod_paciente,
            NVL(p.sexo,p2.sexo)                       AS sexo,
            NVL(p.DATA_NASCIMENTO,p2.DATA_NASCIMENTO) AS DATA_NASCIMENTO
        FROM
            (SELECT to_date('01/'
            || SUBSTR(dxc.data,4,7),'DD/MM/YYYY')            AS mes_ligacao,
            TRUNC(to_Date(dxc.data,'DD/MM/YYYY HH24:MI:SS')) AS data_ajustada,
            to_number(NVL(
            CASE
                WHEN INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') > 0
                THEN SUBSTR( SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') + LENGTH('"cod_paciente":"')),1, INSTR(SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"cod_paciente":"') + LENGTH('"cod_paciente":"')), '"') - 1)
                ELSE NULL
            END,
            CASE
                WHEN INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') > 0
                THEN SUBSTR( SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') + LENGTH('"CPF":"')),1, INSTR(SUBSTR(dxc.CAMPO_AGRUPADO, INSTR(dxc.CAMPO_AGRUPADO, '"CPF":"') + LENGTH('"CPF":"')), '"') - 1)
                ELSE NULL
            END))        AS cod_paciente,
            dxc.campanha AS nome_campanha,
            dxc.NUMERO,
            dxc.status
            FROM dados_x5_campanhas dxc
            WHERE dxc.campanha LIKE '%VOIP%'
            AND dxc.status                                  <> 'Completou'
            AND to_date(SUBSTR(dxc.data,1,10),'DD/MM/YYYY') >= '01/12/2023'
            ) l1,
            paciente p,
            paciente p2
        WHERE REPLACE(TO_CHAR(l1.cod_paciente,'00000000000'),' ','') = p.cpf (+)
        AND l1.cod_paciente                                          = p2.cod_paciente (+)
        AND l1.cod_paciente                                         <> 0
        AND NVL(p.cod_paciente,p2.cod_paciente)                     IS NOT NULL
        ) l2
        ) l3
        --where l3.nome_camp_ajustado = 'VER'
    GROUP BY l3.data_discagem,
        l3.nome_camp_ajustado,
        l3.sexo,
        l3.grupo_idade
    ) l4
    GROUP BY l4.NOME_CAMP_AJUSTADO
    ORDER BY 2 DESC
    """

# 
SQL_MAILING = """
    -- SELECT PARA CRIAR O MAILING CONFORME REGRA DESCRITA ABAIXO
        SELECT
        /*ESSE CAMPO É SÓ PARA CONSULTAR APÓS EFETUAR A CONSULTA, DEVE COMENTAR O CAMPO */
        --ttt.nome_camp, count(ttt.cod_paciente) as qtd
        /*APÓS EFETUAR A CONSULTA ACIMA, DEVE DESCOMENTAR ESSES CAMPOS */
        /*ttt.cod_paciente,
        ttt.nome,
        ttt.sexo,
        ttt.idade,
        ttt.fone_primario,
        ttt.fone_primario_ajust,
        */
        ttt.nome_camp,
        ttt.nome
        || ';;;'
        || ttt.fone_primario
        || ';'
        || ttt.cod_paciente AS coluna_concatenada,
        ttt.prioridade_camp
        --ttt.ordem_prioridade
        FROM
        (SELECT tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp,
            tt.prioridade_camp,
            RANK() OVER (PARTITION BY tt.cod_paciente ORDER BY tt.cod_paciente, tt.prioridade_camp, tt.nome_camp) AS ordem_prioridade
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.idade,
            t.fone_primario,
            t.fone_primario_ajust,
            t.nome_camp,
            /* ****************************************** REGRA ********************************************************************
            CONSULTAR O BI DENTRO DE INDICADORES DA GERENCIA . BI AGENDAMENTOS GERAL, NA ABA GUIAS PAGAS VOIP
            % SAUCESSO VOIP POR CAMPANHA, E AJUSTAR O CASE WHEN ABAIXO CONFORME A ORDEM DO BI.
            EXEMPLO.: SE O ODONTO É O PRIMEIRO,
            *********************************************************************************************************************** */
            CASE
                WHEN t.nome_camp = :num0
                THEN 1
                WHEN t.nome_camp = :num1
                THEN 2
                WHEN t.nome_camp = :num2
                THEN 3
                WHEN t.nome_camp = :num3
                THEN 4
                WHEN t.nome_camp = :num4
                THEN 5
                WHEN t.nome_camp = :num5
                THEN 6
                WHEN t.nome_camp = :num6
                THEN 7
                WHEN t.nome_camp = 'ODONTO GERAL'
                THEN 8
            END                                                                                 AS prioridade_camp,
            RANK() OVER (PARTITION BY t.fone_primario ORDER BY t.cod_paciente, t.fone_primario) AS ordem_telefone
            FROM campanhas_voip_base t
            ) tt
        WHERE tt.ordem_telefone = 1
        ) ttt
        WHERE ttt.ordem_prioridade           = 1
        AND SUBSTR(ttt.fone_primario, 2, 2) IN ('51', '53', '54', '55')
        ORDER BY 3
        --and ttt.cod_paciente in (98,170)
        -- APÓS A CONSULTA DE CIMA, COMENTAR ESSA LINHA POIS NÃO VAMOS ESTAR FAZENDO MAIS AGRUPAMENTO PARA CONTAR.
        --group by ttt.nome_camp
    """

# Insert data into VOIP
SQL_INSERT_VOIP= f"""
    INSERT
        INTO CAMPANHAS_VOIP_BASE
        (
            cod_paciente,
            nome,
            sexo,
            Idade,
            fone_primario,
            fone_primario_ajust,
            nome_camp
        )
        SELECT ttt.cod_paciente,
        ttt.nome,
        ttt.sexo,
        ttt.Idade,
        ttt.fone_primario,
        ttt.fone_primario_ajust,
        ttt.nome_camp
        FROM
        (
        -----------------------------------------------------------CAMPANHA CARDIOLOGICOS------------------------------------------------------
        SELECT tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'CARDIOLOGIA' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                -- MUDAR A DATA CONFORME A REGRA
                -- ultimo 1 ano sem vir |UM ANO ATRAS REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> '31/10/2023'
                -- and trunc(ah.data_agenda) between '01/01/2018' and '31/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND LAST_DAY(ADD_MONTHS(SYSDATE, -12))
                --AND trunc(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F','M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (9,16,7606512,7606588,7606600)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --   – *******  MUDAR A DATA CONFORME A REGRA  ******
                --  – *** ESSA DATA e TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATRAS?S ==> UM ANO ATRAS?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                -- and trunc(ah.data_agenda) >= '01/01/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (9,16,7606512,7606588,7606600)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA CHECKUP SAUDE------------------------------------------------------
        SELECT tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'CHECK UP SAUDE' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --– *******  MUDAR A DATA CONFORME A REGRA  ******
                --– *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F','M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (14,3358004,11294058,11294061,11294063,12730246,12981094,13760880,13686714,14240665,12821272)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --  – *******  MUDAR A DATA CONFORME A REGRA   ******
                --   – *** ESSA DATA É TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATR�?S ==> UM ANO ATR�?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                --and trunc(ah.data_agenda) >= '24/12/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (14,3358004,11294058,11294061,11294063,12730246,12981094,13760880,13686714,14240665,12821272)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA GINECOLOGICOS------------------------------------------------------
        SELECT
            --count(tt.cod_paciente),
            tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'CHECKUP_MULHER' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                -- *******  MUDAR A DATA CONFORME A REGRA     ******
                -- *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (513482,11623226,11515091,18)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --  – *******  MUDAR A DATA CONFORME A REGRA   ******
                -- – *** ESSA DATA É TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATR�?S ==> UM ANO ATR�?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                --and trunc(ah.data_agenda) >= '24/12/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (513482,11623226,11515091,18)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA ODONTO GERAL------------------------------------------------------
        SELECT DISTINCT t.cod_paciente,
            t.nome,
            t.sexo,
            TRUNC(Months_between(TRUNC(sysdate),t.data_nascimento)/12) Idade,
            NVL(NVL(
            CASE
            WHEN SUBSTR(t.fone1,5,1) IN ('9','8','7','6')
            THEN t.fone1
            ELSE NULL
            END,
            CASE
            WHEN SUBSTR(t.fone2,5,1) IN ('9','8','7','6')
            THEN t.fone2
            ELSE NULL
            END),NVL(
            CASE
            WHEN SUBSTR(t.fone1,5,1) IN ('1','2','3','4','5')
            THEN t.fone1
            ELSE NULL
            END,
            CASE
            WHEN SUBSTR(t.fone2,5,1) IN ('1','2','3','4','5')
            THEN t.fone2
            ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
            WHEN SUBSTR(t.fone1,5,1) IN ('9','8','7','6')
            THEN t.fone1
            ELSE NULL
            END,
            CASE
            WHEN SUBSTR(t.fone2,5,1) IN ('9','8','7','6')
            THEN t.fone2
            ELSE NULL
            END),NVL(
            CASE
            WHEN SUBSTR(t.fone1,5,1) IN ('1','2','3','4','5')
            THEN t.fone1
            ELSE NULL
            END,
            CASE
            WHEN SUBSTR(t.fone2,5,1) IN ('1','2','3','4','5')
            THEN t.fone2
            ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
        FROM
            ( SELECT DISTINCT p.cod_paciente,
            p.nome,
            p.sexo,
            p.data_nascimento,
            p.fone1,
            p.fone2,
            --trunc(Months_between(trunc(sysdate),p.data_nascimento)/12) Idade,
            'ODONTO GERAL' AS nome_camp
            FROM agenda_horario ah,
            agenda a,
            exame e,
            filial f,
            paciente p,
            medico m,
            especialidade_medica em,
            exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
            -- *******  MUDAR A DATA CONFORME A REGRA     ******
            --– *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
            --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo IN ('F','M')
            --and trunc(Months_between(trunc(sysdate),p.data_nascimento)/12) between 16 and 60
            --and e.cod_exame in (27,28)
            AND p.cod_paciente NOT IN
            (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
            )
            AND p.fone1 NOT IN
            (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
            )
            AND p.fone2 NOT IN
            (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
            )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
            (SELECT DISTINCT t.tel_procon FROM tel_procon t
            )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
            (SELECT DISTINCT t.tel_procon FROM tel_procon t
            )
            -- Nesta parte eu faço um not in somente na parte do cod paciente que nunca teve um conf S em odonto no periodo selecionado.
            AND p.cod_paciente NOT IN
            ( SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --  – *******  MUDAR A DATA CONFORME A REGRA     ******
                -- – *** AQUI PEGAMOS ATE O DIA DE HOJE OU SEJA TODOS QUE NAO VIERAM ATE A DATA DE HOJE.
                --  and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2024'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND TRUNC(SYSDATE)
            AND m.nome     <> 'LAPROJAL'
            AND p.sexo     IN ('F','M')
            AND e.cod_grupo = 347
            )
            ) t
        UNION ALL
        -----------------------------------------------------------CAMPANHA ODONTO------------------------------------------------------
        SELECT
            --count(tt.cod_paciente)
            tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'ODONTO' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --– *******  MUDAR A DATA CONFORME A REGRA   ******
                --– *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F','M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 16 AND 60
            AND e.cod_grupo         = 347
            AND p.cod_paciente NOT IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --   – *******  MUDAR A DATA CONFORME A REGRA   ******
                --  – *** ESSA DATA É TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATR�?S ==> UM ANO ATR�?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                -- and trunc(ah.data_agenda) >= '24/12/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_grupo            = 347
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA OFTALMO------------------------------------------------------
        SELECT
            --–count(tt.cod_paciente)
            tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'OFTALMOLOGIA' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --– *******  MUDAR A DATA CONFORME A REGRA     ******
                -- – *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F','M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (23,12463092,12463096,12463098,12463105)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --   – *******  MUDAR A DATA CONFORME A REGRA     ******
                --   – *** ESSA DATA É TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATR�?S ==> UM ANO ATR�?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                --and trunc(ah.data_agenda) >= '24/12/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (23,12463092,12463096,12463098,12463105)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA CHECKUP HOMEM------------------------------------------------------
        SELECT
            --–count(tt.cod_paciente)
            tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'CHECKUP_HOMEM' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --– *******  MUDAR A DATA CONFORME A REGRA   ******
                --– *** ultimo 1 ano sem vir |UM ANO ATR�?S REFERENTE A ESSE MES QUE ESTAMOS FAZENDO O VOIP -> (31/10/2023)
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/12/2023'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -12)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (30)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --   – *******  MUDAR A DATA CONFORME A REGRA   ******
                --   – *** ESSA DATA É TODOS QUE VIERAM UM DIA DEPOIS DE UM ANO ATR�?S ==> UM ANO ATR�?S =-=> 31/10/2023 UM DIA DEPOIS==>  SEJA 01/11/2023
                --and trunc(ah.data_agenda) >= '24/12/2023'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -12) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (30)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        UNION ALL
        -----------------------------------------------------------CAMPANHA PSICOLOGIA PSQUIATRIA------------------------------------------------------
        SELECT
            --–count(tt.cod_paciente)
            tt.cod_paciente,
            tt.nome,
            tt.sexo,
            tt.Idade,
            tt.fone_primario,
            tt.fone_primario_ajust,
            tt.nome_camp
        FROM
            (SELECT t.cod_paciente,
            t.nome,
            t.sexo,
            t.Idade,
            NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)) AS fone_primario,
            REPLACE(REPLACE(NVL(NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('9','8','7','6')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('9','8','7','6')
                THEN p.fone2
                ELSE NULL
            END),NVL(
            CASE
                WHEN SUBSTR(p.fone1,5,1) IN ('1','2','3','4','5')
                THEN p.fone1
                ELSE NULL
            END,
            CASE
                WHEN SUBSTR(p.fone2,5,1) IN ('1','2','3','4','5')
                THEN p.fone2
                ELSE NULL
            END)),'(',''),')','') AS fone_primario_ajust,
            t.nome_camp
            FROM
            ( SELECT DISTINCT p.cod_paciente,
                p.nome,
                p.sexo,
                TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) Idade,
                'PSICOLOGO E PSIQUIATRIA' AS nome_camp
            FROM agenda_horario ah,
                agenda a,
                exame e,
                filial f,
                paciente p,
                medico m,
                especialidade_medica em,
                exame_grupo eg
            WHERE ah.cod_agenda     = a.cod_agenda
            AND ah.cod_exame        = e.cod_exame
            AND ah.cod_filial       = f.cod_filial
            AND a.cod_paciente      = p.cod_paciente
            AND ah.cod_executor     = m.cod_medico
            AND ah.cod_agenda      IS NOT NULL
            AND e.cod_especialidade = em.cod_especialidade
            AND e.cod_grupo         = eg.cod_grupo
            AND ah.confirmado       = 'S'
                --– *******  MUDAR A DATA CONFORME A REGRA  ******
                -- – *** ultimos 6 meses sem vir  ***
                --and trunc(ah.data_agenda) between '01/01/2018' and '23/06/2024'
            AND TRUNC(ah.data_agenda) BETWEEN '01/01/2018' AND ADD_MONTHS(SYSDATE, -6)
            AND m.nome <> 'LAPROJAL'
            AND p.sexo                                               IN ('F','M')
            AND TRUNC(Months_between(TRUNC(sysdate),p.data_nascimento)/12) BETWEEN 18 AND 70
            AND e.cod_exame                                                 IN (27,28)
            AND p.cod_paciente NOT                                          IN
                (SELECT DISTINCT tq.cod_paciente FROM tel_cod_pac_quarentena tq
                )
            AND p.fone1 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND p.fone2 NOT IN
                (SELECT DISTINCT tq.telefone FROM tel_cod_pac_quarentena tq
                )
            AND REPLACE(REPLACE(p.fone1,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            AND REPLACE(REPLACE(p.fone2,'(',''),')','') NOT IN
                (SELECT DISTINCT t.tel_procon FROM tel_procon t
                )
            ) t,
            paciente p
            WHERE t.cod_paciente NOT IN
            (SELECT DISTINCT p.cod_paciente
            FROM agenda_horario ah,
                agenda a,
                paciente p,
                exame e,
                exame_grupo eg
            WHERE ah.cod_agenda = a.cod_agenda
            AND a.cod_paciente  = p.cod_paciente
            AND ah.cod_agenda  IS NOT NULL
            AND ah.confirmado   = 'S'
                --    – *******  MUDAR A DATA CONFORME A REGRA   ******
                --    – *** ESSA DATA E TODOS QUE VIERAM UM DIA DEPOIS DOS ULTIMOS SEIS MESES ==> 6 MESES ATRAS =-=> 30/04/2023 UM DIA DEPOIS==>  SEJA 01/05/2023
                --and trunc(ah.data_agenda) >= '24/06/2024'
            AND TRUNC(ah.data_agenda) >= ADD_MONTHS(TRUNC(SYSDATE), -6) + 1
            AND e.cod_grupo            = eg.cod_grupo
            AND e.cod_exame           IN (27,28)
            )
            AND t.cod_paciente = p.cod_paciente
            ) tt
        ) ttt
    """
