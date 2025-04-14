-- Criação do banco de dados Data Lake
CREATE DATABASE raw
	WITH OWNER = airflow
	ENCODING = 'UTF8'
	LOCALE_PROVIDER = 'icu'
	ICU_LOCALE = 'pt'
	TEMPLATE = template0;

-- Criando tabelas
-- tabela transacoes 
CREATE TABLE IF NOT EXISTS public."TorreTransacoes" (
    "CNPJIntegradora" TEXT,
    "NomeIntegradora" TEXT,
    "Transacao" TEXT NOT NULL,
    "DataTransacao" TEXT,
    "CartaoMascarado" TEXT,
    "Placa" TEXT,
    "MarcaVeiculo" TEXT,
    "ModeloVeiculo" TEXT,
    "CorVeiculo" TEXT,
    "AnoVeiculo" TEXT,
    "MatriculaVeiculo" TEXT,
    "MatriculaMotorista" TEXT,
    "Motorista" TEXT,
    "IDPosto" TEXT,
    "RazaoSocialPosto" TEXT,
    "CNPJPosto" TEXT,
    "NomeFantasiaPosto" TEXT,
    "EnderecoPosto" TEXT,
    "NumeroEnderecoPosto" TEXT,
    "ComplementoEnderecoPosto" TEXT,
    "BairroPosto" TEXT,
    "CEPPost" TEXT,
    "CidadePosto" TEXT,
    "UFPosto" TEXT,
    "Hodometro" TEXT,
    "CodCombustivel" TEXT,
    "NomeCombustivel" TEXT,
    "Litragem" TEXT,
    "Valor" TEXT,
    "CPFMotorista" TEXT,
    "IDServico" TEXT,
    "Servico" TEXT,
    "TipoAbastecimento" TEXT,
    "TransacaoEstornada" TEXT,
    "CNPJCliente" TEXT,
    "CodigoTanque" TEXT,
    "NomeTanque" TEXT,
    "CodigoBomba" TEXT,
    "NomeBomba" TEXT,
    "MediaFabrica" TEXT,
    "TanqueCheio" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT torre_transacoes_unique UNIQUE ("Transacao")
);

-- Tabela de fretes
CREATE TABLE IF NOT EXISTS public."Fretes" (
    "ID" TEXT NOT NULL,
    "FreteData" TEXT,
    "FreteColeta" TEXT,
    "FreteTotal" TEXT,
    "TrechoOrigemCidade" TEXT,
    "TrechoOrigemEstado" TEXT,
    "TrechoOrigemRegiao" TEXT,
    "TrechoDestinoCidade" TEXT,
    "TrechoDestinoEstado" TEXT,
    "TrechoDestinoRegiao" TEXT,
    "MercadoriaNota" TEXT,
    "MercadoriaPedido" TEXT,
    "MercadoriaDescricao" TEXT,
    "MercadoriaValor" TEXT,
    "MercadoriaVolumes" TEXT,
    "MercadoriaPesoRealNota" TEXT,
    "MercadoriaPesoReal" TEXT,
    "MercadoriaPesoCubado" TEXT,
    "MercadoriaPesoM3" TEXT,
    "MercadoriaPesoTaxado" TEXT,
    "FiscalBaseIcms" TEXT,
    "FiscalAliquotaIcms" TEXT,
    "FiscalValorIcms" TEXT,
    "FiscalBasePisCofins" TEXT,
    "FiscalAliquotaPis" TEXT,
    "FiscalValorPis" TEXT,
    "FiscalAliquotaCofins" TEXT,
    "FiscalValorCofins" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_unique UNIQUE ("ID")
);

-- Tabela de atores envolvidos nos fretes
CREATE TABLE IF NOT EXISTS public."FretesAtores" (
    "ID" TEXT NOT NULL,
    "EmissorRazao" TEXT,
    "EmissorFantasia" TEXT,
    "EmissorUsuario" TEXT,
    "PagadorDocumento" TEXT,
    "PagadorRazao" TEXT,
    "PagadorFantasia" TEXT,
    "PagadorVendedor" TEXT,
    "RemetenteDocumento" TEXT,
    "RemetenteRazao" TEXT,
    "RemetenteFantasia" TEXT,
    "RemetenteCidade" TEXT,
    "RemetenteEstado" TEXT,
    "ExpedidorDocumento" TEXT,
    "ExpedidorRazao" TEXT,
    "ExpedidorFantasia" TEXT,
    "ExpedidorCidade" TEXT,
    "ExpedidorEstado" TEXT,
    "DestinatarioDocumento" TEXT,
    "DestinatarioRazao" TEXT,
    "DestinatarioFantasia" TEXT,
    "DestinatarioCidade" TEXT,
    "DestinatarioEstado" TEXT,
    "RecebedorDocumento" TEXT,
    "RecebedorRazao" TEXT,
    "RecebedorFantasia" TEXT,
    "RecebedorCidade" TEXT,
    "RecebedorEstado" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_atores_unique UNIQUE ("ID")
);

-- Tabela de conferências de fretes
CREATE TABLE IF NOT EXISTS public."FretesConferencias" (
    "ID" TEXT NOT NULL,
    "ConferenciaOrdem" TEXT,
    "ConferenciaData" TEXT,
    "ConferenciaInicio" TEXT,
    "ConferenciaFim" TEXT,
    "ConferenciaTipo" TEXT,
    "ConferenciaVolumes" TEXT,
    "ConferenciaVolumesLidos" TEXT,
    "ConferenciaVolumesPendentes" TEXT,
    "ConferenciaStatus" TEXT,
    "ConferenciaDoca" TEXT,
    "ConferenciaGerarManifesto" TEXT,
    "ConferenciaManifesto" TEXT,
    "ConferenciaTipoManifesto" TEXT,
    "ConferenciaFilial" TEXT,
    "ConferenciaAgente" TEXT,
    "ConferenciaUsuario" TEXT,
    "ManifestoID" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_conferencias_unique UNIQUE ("ID")
);

-- Tabela de informações dinâmicas de fretes
CREATE TABLE IF NOT EXISTS public."FretesDinamico" (
    "ID" TEXT NOT NULL,
    "FreteMinuta" TEXT,
    "FreteMinutaData" TEXT,
    "FreteConhecimento" TEXT,
    "FreteConhecimentoSerie" TEXT,
    "FreteConhecimentoChave" TEXT,
    "FreteConhecimentoData" TEXT,
    "OcorrenciaPrevisaoEntrega" TEXT,
    "AgenteEntregaRazao" TEXT,
    "AgenteEntregaFantasia" TEXT,
    "AgenteEntregaValor" TEXT,
    "AgenteEntregaAdicional" TEXT,
    "AgenteEntregaTotal" TEXT,
    "AgenteColetaRazao" TEXT,
    "AgenteColetaFantasia" TEXT,
    "AgenteColetaValor" TEXT,
    "AgenteColetaAdicional" TEXT,
    "AgenteColetaTotal" TEXT,
    "SeguroAverbacao" TEXT,
    "FaturaID" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_dinamico_unique UNIQUE ("ID")
);

-- Tabela de fretes excluídos
CREATE TABLE IF NOT EXISTS public."FretesExcluidos" (
    "ID" TEXT NOT NULL,
    "ExclusaoData" TEXT,
    "ExclusaoMotivo" TEXT,
    "ExclusaoUsuarioExclusao" TEXT,
    "ExclusaoUsuarioCriacao" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_excluidos_unique UNIQUE ("ID")
);

-- Tabela de faturas de fretes
CREATE TABLE IF NOT EXISTS public."FretesFaturas" (
    "ID" TEXT NOT NULL,
    "FaturaNumero" TEXT,
    "FaturaDocumento" TEXT,
    "FaturaData" TEXT,
    "FaturaMesCompetencia" TEXT,
    "FaturaAnoCompetencia" TEXT,
    "FaturaValor" TEXT,
    "FaturaAcrescimo" TEXT,
    "FaturaDesconto" TEXT,
    "FaturaValorReceber" TEXT,
    "FaturaObservacoes" TEXT,
    "FaturaBoleto" TEXT,
    "FaturaVencimento" TEXT,
    "FaturaAgencia" TEXT,
    "FaturaConta" TEXT,
    "FaturaStatus" TEXT,
    "FaturaValorPago" TEXT,
    "FaturaEnviarEmail" TEXT,
    "FaturaEmailCliente" TEXT,
    "FaturaCopiaEmailCliente" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_faturas_unique UNIQUE ("ID")
);

-- Tabela de manifestos de fretes
CREATE TABLE IF NOT EXISTS public."FretesManifestos" (
    "ID" TEXT NOT NULL,
    "ManifestoDocumento" TEXT,
    "ManifestoSaida" TEXT,
    "ManifestoChegada" TEXT,
    "ManifestoStatus" TEXT,
    "ManifestoEletronico" TEXT,
    "ManifestoEletronicoStatus" TEXT,
    "ManifestoMonitoramento" TEXT,
    "ManifestoVeiculoModelo" TEXT,
    "ManifestoPlaca" TEXT,
    "ManifestoFretesEntregas" TEXT,
    "ManifestoFretesTransferencias" TEXT,
    "ManifestoColetas" TEXT,
    "ManifestoTotalFretes" TEXT,
    "ManifestosNotas" TEXT,
    "ManifestoNotasValor" TEXT,
    "ManifestoVolumes" TEXT,
    "ManifestoNotasPeso" TEXT,
    "ManifestoPesoM3" TEXT,
    "ManifestoPesoTaxado" TEXT,
    "ManifestoUsuario" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_manifestos_unique UNIQUE ("ID")
);

-- Tabela de ocorrências de fretes
CREATE TABLE IF NOT EXISTS public."FretesOcorrencias" (
    "ID" TEXT NOT NULL,
    "OcorrenciaStatus" TEXT,
    "OcorrenciaData" TEXT,
    "OcorrenciaCodigo" TEXT,
    "OcorrenciaNome" TEXT,
    "OcorrenciaObservacao" TEXT,
    "OcorrenciaRecebedor" TEXT,
    "OcorrenciaDocumento" TEXT,
    "OcorrenciaBaixaMobile" TEXT,
    "OcorrenciaComprovanteFrete" TEXT,
    "OcorrenciaComprovanteNota" TEXT,
    "OcorrenciaUsuario" TEXT,
    "OcorrenciaUsuarioFilial" TEXT,
    "FreteID" TEXT,
    "ManifestoID" TEXT,
    "Atualizacao" TEXT,
    CONSTRAINT fretes_ocorrencias_unique UNIQUE ("ID")
);