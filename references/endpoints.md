eleicoes2018
==============================


Endpoints de API do TSE 2018
------------

* `getResourceCandidato`: 

`/rest/v1/candidatura/buscar/:ano/:sgUe/:eleicao/candidato/:idCandidato`

* `getResourceCandidatos`: 

`/rest/v1/candidatura/listar/:ano/:sgUe/:eleicao/:cargo/candidatos`

* `getResourceCandidatosCSV`: 

`/rest/v1/candidatura/listar/:ano/:sgUe/:eleicao/:cargo/candidatos/csv`

* `getServerStatus`: 

`/rest/v1/eleicao/database/monitor`

* `getEleicaoAtual`: 

`/rest/v1/eleicao/eleicao-atual`

* `getResourceAnosEleitorais`: 

`/rest/v1/eleicao/anos-eleitorais`

* `getResourceEstadosPorAnoReferencia`: 

`/rest/v1/eleicao/estados/:ano/ano`

* `getResourceEleicaoPorAno`: 

`/rest/v1/eleicao/ordinaria/:ano`

* `getResourceEleicoesOrdinarias`: 

`/rest/v1/eleicao/ordinarias`

* `getResourceEleicoesSuplementares`: 

`/rest/v1/eleicao/suplementares/:ano/:sgUe`

* `getResourceMunicipios`: 

`/rest/v1/eleicao/buscar/:uf/:sqEleicao/municipios`

* `getResourceCargos`: 

`/rest/v1/eleicao/listar/municipios/:eleicao/:sgUe/cargos`

* `getResourceCargosPorEleicao`: 

`/rest/v1/eleicao/:eleicao/cargos`

* `getResourceUfs`: 

`/rest/v1/eleicao/ufs`

* `getResourceMunicipiosPorUf`: 

`/rest/v1/eleicao/ufs/:uf/municipios`

* `getResourceMunicipiosPorUfPrestacaoContas`: 

`/rest/v1/eleicao/uf/:sqEleicao/:uf/municipios`

* `getResourceConsultaPrestadores`: 

`/rest/v1/prestador/consulta/nome/:sqEleicao/:tipoPrestador?nome=:nome`

* `getResourceConsultaPrestadorCNPJ`: 

`/rest/v1/prestador/consulta/cnpj/:sqEleicao/:cnpj`

* `getResourcePrestador`: 

`/rest/v1/prestador/consulta/:sqEleicao/:ano/:sgUe/:idCargo/:nrPartido/:nrCandidato/:sqCandidato`

* `getResourcePartido`: 

`/rest/v1/prestador/consulta/partido/:sqEleicao/:ano/:sgUe/:cdOrgao/:nrPartido`

* `getResourceExtratoPrestador`: 

`/rest/v1/prestador/consulta/extrato/:sqEleicao/:anoReferencia/:sqPrestadorConta/:nrBanco/:agencia/:conta`

* `getResourcePartidos`: 

`/rest/v1/eleicao/:sqEleicao/:sgUe/:cdOrgao/partidos`

* `getResourceCompararEntregas`: 

`/rest/v1/prestador/consulta/:sqEleicao/:ano/:sgUe/:cdCargo/:nrPartido/:nrCandidato/:sqCandidato/:sqPrestador/:sqEntrega1/:sqEntrega2`

* `getResourceConsultaConciliacao`: 

`/rest/v1/prestador/consulta/conciliacao/:sqEleicao/:ano/:sqPrestador/:sqEntregaPrestacao`

* `getResourceConsultaComercializacao`: 

`/rest/v1/prestador/consulta/comercializacao/:sqEleicao/:ano/:sqPrestador/:sqEntregaPrestacao`

* `getResourceListaPartidos`: 

`/rest/v1/prestador/campanha/partidos/:idEleicao`

* `getResourceDividasIndividual`: 

`/rest/v1/prestador/campanha/divida/:idEleicao/individual/:idPrestador`

* `getResourceDividasIndividual`: 

`/rest/v1/prestador/financiamento/consulta/empresa`

* `getResourceFinanciamentoColetivo`: 

`/rest/v1/prestador/financiamento/consulta/:codEleicao/empresa`

* `getResourceDividasCandidatos`: 

`/rest/v1/prestador/campanha/divida/:idEleicao/candidatos/:nrPartido`

* `getResourceDividasPartidos`: 

`/rest/v1/prestador/campanha/divida/:idEleicao/partidos/:nrPartido`

* `getResourceSobrasIndividual`: 

`/rest/v1/prestador/campanha/sobra/:idEleicao/individual/:idPrestador`

* `getResourceSobrasCandidatos`: 

`/rest/v1/prestador/campanha/sobra/:idEleicao/candidatos/:nrPartido`

* `getResourceSobrasPartidos`: 

`/rest/v1/prestador/campanha/sobra/:idEleicao/partidos/:nrPartido`

* `getResourceDoadoresFornecedores`: 

`/rest/v1/doador-fornecedor/consulta/:idEleicao`

* `getResourceTotalizador`: 

`/rest/v1/doador-fornecedor/consulta/totalizador/:idEleicao/:cpfCnpj`

* `getResourceDetalhamentoReceita`: 

`/rest/v1/doador-fornecedor/receita/detalhe/:idEleicao/:cpfCnpjDoador`

* `getResourceDetalhamentoDespesa`: 

`/rest/v1/doador-fornecedor/despesa/detalhe/:idEleicao/:cpfCnpjFornecedor`

* `getResourceRankConcentracao`: 

`/rest/v1/prestador/ranks/concentracao/:eleicao/:ano`

* `getResourceRankDoadores`: 

`/rest/v1/prestador/ranks/doadores/:eleicao/:ano`

* `getResourceRankFornecedores`: 

`/rest/v1/prestador/ranks/fornecedores/:eleicao/:ano`

* `getResourceRankTotalizado`: 

`/rest/v1/prestador/ranks/total/:eleicao`

* `getResourceComparativoCandidatos`: 

`/rest/v1/prestador/comparativo/candidatos/:eleicao/:ano/uf/:uf/cargo/:cargo`






