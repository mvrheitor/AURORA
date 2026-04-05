# 🚀 ROADMAP – AURORA

Este arquivo descreve ideias e direções futuras para o desenvolvimento da Aurora.
Nem todas estão planejadas para curto prazo, mas representam a visão de longo prazo do projeto.

---

## 🌐 1. Pesquisa Iterativa na Internet

Objetivo: permitir que Aurora pesquise como um agente real, não como uma única query.

Inventar alguma tool e um jeito inteligente de fazer a Aurora poder pesquisar diversas coisas na internet, como o Perplexity AI faz.
Apenas uma tool que pede umas 3 queries e retorna o conteúdo dos principais resultados encontrados na internet é uma droga.
Tenho que invenjar um jeito de fazer Aurora poder continuar pesquisando até que ela encontre e/ou esteja satisfeita com o que encontrou na internet, assim como ela faz com a tool de executar comandos, e assim como o Perplexity AI faz. Seria um loop de pesquisa autônomo: buscar → analisar → refinar → buscar novamente.

Problemas atuais:
- Uma tool simples de busca é limitada.
- Não há refinamento automático.
- Não há avaliação de qualidade dos resultados.

Ideias:
- Criar um loop de pesquisa:
  - buscar → analisar → refinar → buscar novamente.
- Permitir múltiplas chamadas automáticas.
- Tornar a pesquisa autônoma, como no Perplexity AI.

---

## 🧠 2. Memória de Longo Prazo

Objetivo: dar à Aurora uma memória de verdade.

Usar embeddings/vetores para guardar memórias com base em similaridade e inventar algum jeito da Aurora poder consultar as memórias.
Apenas uma tool para procurar memórias seria bem eficiente, mas Aurora nunca saberia quando usar, a não ser que eu dissesse para ela usar em todas as interações, mas isso deixaria as interações lentas. Além disso, tenho que inventar um jeito eficiente de guardar memórias úteis, pois simplesmente guardar todas as interações é meio inútil.

Desafios:
- Não salvar tudo.
- Não deixar lento.
- Saber quando buscar memórias.
- Saber quando criar novas.

Ideias:
- Usar embeddings/vetores.
- Criar critérios para salvar memórias úteis.
- Criar heurísticas para consulta automática.
- Separar memória curta e memória longa.
