-- Criação do banco de dados Data Lake
CREATE DATABASE bronze
	WITH OWNER = postgres
	ENCODING = 'UTF8'
	LOCALE_PROVIDER = 'icu'
	ICU_LOCALE = 'pt'
	TEMPLATE = template0;

-- Criando tabelas
-- tabela transacoes 
CREATE TABLE IF NOT EXISTS public.torre_transacoes (

);

-- Tabela de fretes
CREATE TABLE IF NOT EXISTS public.fretes (
    id TEXT NOT NULL,
    frete_data TIMESTAMP NOT NULL,
    frete_coleta NUMERIC(8,2) ,
    frete_total NUMERIC(8,2) ,
    trecho_origem_cidade TEXT ,
    trecho_origem_estado CHAR(2) ,
    trecho_origem_regiao TEXT ,
    trecho_destino_cidade TEXT ,
    trecho_destino_estado CHAR(2) ,
    trecho_destino_regiao TEXT ,
    mercadoria_nota TEXT ,
    mercadoria_pedido TEXT ,
    mercadoria_descricao TEXT ,
    mercadoria_valor NUMERIC(8,2) ,
    mercadoria_volumes INTEGER ,
    mercadoria_peso_real_nota NUMERIC(8,2) ,
    mercadoria_peso_real NUMERIC(8,2) ,
    mercadoria_peso_cubado NUMERIC(9,3) ,
    mercadoria_peso_m3 NUMERIC(8,2) ,
    mercadoria_peso_taxado NUMERIC(9,3) ,
    fiscal_base_icms NUMERIC(8,2) ,
    fiscal_aliquota_icms NUMERIC(5,2) ,
    fiscal_valor_icms NUMERIC(8,2) ,
    fiscal_base_pis_cofins NUMERIC(8,2) ,
    fiscal_aliquota_pis NUMERIC(5,2) ,
    fiscal_valor_pis NUMERIC(8,2) ,
    fiscal_aliquota_cofins NUMERIC(5,2) ,
    fiscal_valor_cofins NUMERIC(8,2) ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_pkey PRIMARY KEY (id)
);

-- Tabela de atores envolvidos nos fretes
CREATE TABLE IF NOT EXISTS public.fretes_atores (
    id TEXT NOT NULL,
    emissor_razao TEXT ,
    emissor_fantasia TEXT ,
    emissor_usuario TEXT ,
    pagador_documento TEXT ,
    pagador_razao TEXT ,
    pagador_fantasia TEXT ,
    pagador_vendedor TEXT ,
    remetente_documento TEXT ,
    remetente_razao TEXT ,
    remetente_fantasia TEXT ,
    remetente_cidade TEXT ,
    remetente_estado CHAR(2) ,
    expedidor_documento TEXT ,
    expedidor_razao TEXT ,
    expedidor_fantasia TEXT ,
    expedidor_cidade TEXT ,
    expedidor_estado CHAR(2) ,
    destinatario_documento TEXT ,
    destinatario_razao TEXT ,
    destinatario_fantasia TEXT ,
    destinatario_cidade TEXT ,
    destinatario_estado CHAR(2) ,
    recebedor_documento TEXT ,
    recebedor_razao TEXT ,
    recebedor_fantasia TEXT ,
    recebedor_cidade TEXT ,
    recebedor_estado CHAR(2) ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_atores_pkey PRIMARY KEY (id)
);

-- Tabela de conferências de fretes
CREATE TABLE IF NOT EXISTS public.fretes_conferencias (
    id TEXT NOT NULL,
    conferencia_ordem TEXT ,
    conferencia_data TIMESTAMP ,
    conferencia_inicio TIMESTAMP ,
    conferencia_fim TIMESTAMP ,
    conferencia_tipo TEXT ,
    conferencia_volumes INTEGER ,
    conferencia_volumes_lidos INTEGER ,
    conferencia_volumes_pendentes INTEGER ,
    conferencia_status TEXT ,
    conferencia_doca TEXT ,
    conferencia_gerar_manifesto CHAR(3) ,
    conferencia_manifesto TEXT ,
    conferencia_tipo_manifesto TEXT ,
    conferencia_filial TEXT ,
    conferencia_agente TEXT ,
    conferencia_usuario TEXT ,
    manifesto_id TEXT ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_conferencias_pkey PRIMARY KEY (id)
);

-- Tabela de informações dinâmicas de fretes
CREATE TABLE IF NOT EXISTS public.fretes_dinamico (
    id TEXT NOT NULL,
    frete_minuta TEXT ,
    frete_minuta_data TIMESTAMP ,
    frete_conhecimento TEXT ,
    frete_conhecimento_serie TEXT ,
    frete_conhecimento_chave TEXT ,
    frete_conhecimento_data TIMESTAMP ,
    ocorrencia_previsao_entrega TIMESTAMP ,
    agente_entrega_razao TEXT ,
    agente_entrega_fantasia TEXT ,
    agente_entrega_valor NUMERIC(8,2) ,
    agente_entrega_adicional NUMERIC(8,2) ,
    agente_entrega_total NUMERIC(8,2) ,
    agente_coleta_razao TEXT ,
    agente_coleta_fantasia TEXT ,
    agente_coleta_valor NUMERIC(8,2) ,
    agente_coleta_adicional NUMERIC(8,2) ,
    agente_coleta_total NUMERIC(8,2) ,
    seguro_averbacao TEXT ,
    fatura_id TEXT ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_dinamico_pkey PRIMARY KEY (id)
);

-- Tabela de fretes excluídos
CREATE TABLE IF NOT EXISTS public.fretes_excluidos (

CONSTRAINT fretes_excluidos_pkey PRIMARY KEY (id)
);

-- Tabela de faturas de fretes
CREATE TABLE IF NOT EXISTS public.fretes_faturas (
    id TEXT NOT NULL,
    fatura_numero TEXT NOT NULL,
    fatura_documento TEXT NOT NULL,
    fatura_data TIMESTAMP NOT NULL,
    fatura_mes_competencia CHAR(2) ,
    fatura_ano_competencia CHAR(4) ,
    fatura_valor NUMERIC(8,2) ,
    fatura_acrescimo NUMERIC(8,2) ,
    fatura_desconto NUMERIC(8,2) ,
    fatura_valor_receber NUMERIC(8,2) ,
    fatura_observacoes TEXT ,
    fatura_boleto CHAR(3) ,
    fatura_vencimento TIMESTAMP ,
    fatura_agencia TEXT ,
    fatura_conta TEXT ,
    fatura_status CHAR(3) ,
    fatura_valor_pago NUMERIC(8,2) ,
    fatura_enviar_email CHAR(3) ,
    fatura_email_cliente TEXT ,
    fatura_copia_email_cliente TEXT ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_faturas_pkey PRIMARY KEY (id)
);

-- Tabela de manifestos de fretes
CREATE TABLE IF NOT EXISTS public.fretes_manifestos (
    id TEXT NOT NULL,
    manifesto_documento TEXT ,
    manifesto_saida TIMESTAMP ,
    manifesto_chegada TIMESTAMP ,
    manifesto_status TEXT ,
    manifesto_eletronico CHAR(3) ,
    manifesto_eletronico_status TEXT ,
    manifesto_monitoramento CHAR(3) ,
    manifesto_veiculo_modelo TEXT ,
    manifesto_placa CHAR(7) ,
    manifesto_fretes_entregas INTEGER ,
    manifesto_fretes_transferencias INTEGER ,
    manifesto_coletas INTEGER ,
    manifesto_total_fretes NUMERIC(8,2) ,
    manifestos_notas INTEGER ,
    manifesto_notas_valor NUMERIC(9,2) ,
    manifesto_volumes INTEGER ,
    manifesto_notas_peso NUMERIC(8,2) ,
    manifesto_peso_m3 NUMERIC(8,2) ,
    manifesto_peso_taxado NUMERIC(8,2) ,
    manifesto_usuario TEXT ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_manifestos_pkey PRIMARY KEY (id)
);

-- Tabela de ocorrências de fretes
CREATE TABLE IF NOT EXISTS public.fretes_ocorrencias (
    id TEXT NOT NULL,
    ocorrencia_status TEXT ,
    ocorrencia_data TIMESTAMP ,
    ocorrencia_codigo TEXT ,
    ocorrencia_nome TEXT ,
    ocorrencia_observacao TEXT ,
    ocorrencia_recebedor TEXT ,
    ocorrencia_documento TEXT ,
    ocorrencia_baixa_mobile CHAR(3) ,
    ocorrencia_comprovante_frete CHAR(3) ,
    ocorrencia_comprovante_nota CHAR(3) ,
    ocorrencia_usuario TEXT ,
    ocorrencia_usuario_filial TEXT ,
    frete_id TEXT ,
    manifesto_id TEXT ,
    atualizacao TIMESTAMP NOT NULL,
    CONSTRAINT fretes_ocorrencias_pkey PRIMARY KEY (id)
);