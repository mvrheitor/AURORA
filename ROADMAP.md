# 🚀 ROADMAP – AURORA

Este arquivo descreve ideias e direções futuras para o desenvolvimento da Aurora.
Nem todas estão planejadas para curto prazo, mas representam a visão de longo prazo do projeto.

---

## 🖥️ 1. "Ver o Terminal" (Terminal Persistente)

Objetivo: permitir que Aurora interaja com um terminal real e contínuo.

No momento, Aurora consegue executar comandos diretamente no terminal. No entanto, ela faz isso chamando uma tool e enviando o comando a ser executado como argumento.
A tool executa o comando no terminal, retorna o resultado, sendo erro ou não, e, por fim, o terminal "morre", pois nenhum terminal foi aberto de fato, ela apenas executou um comando. Isso faz com que algumas coisas não sejam possíveis:
- Se Aurora estiver procurando um diretório, ela não consegue primeiro dar um 'cd' em uma pasta, listar o conteúdo, dar 'cd' em outra dentro daquela, e assim por diante. Como o terminal não fica "aberto", é como se ela voltasse ao diretório que estava antes, sempre que executa um comando. Então, ela sempre tem que ficar escrevendo o caminho completo do diretório, além de ter que executar vários comandos em uma linha só, dependendo do que ela for fazer. Exemplo: 'cd /caminho/completo/do/diretório && algum comando específico que deve ser rodado naquele diretório'.
- Outra coisa: vamos supor que há um script python que pergunte meu peso através de um 'input'. Se eu pedir para ela executar o script, ela vai simplesmente travar, pois a tool nunca vai retornar uma saída enquanto o script não terminar, e o script nunca vai terminar enquanto não sair do 'input'. 

Tenho que desenvolver algo que possibilite Aurora "ver" que o terminal está pedindo um input e, se ela souber o que colocar, escrever nele, e se ela não souber, ela ainda poderia deixar o terimnal aberto, me perguntar e depois voltar ao terminal para escrever a resposta, como se a Aurora estivesse vendo duas "telas", uma com o chat entre eu e ela e outra com o terminal que ela abriu.

Problemas atuais:
- Cada comando é executado isoladamente.
- Não há estado de diretório (`cd` não persiste).
- Programas que pedem input travam.
- Aurora não consegue "ver" quando o terminal espera uma resposta.

Ideias:
- Criar uma sessão de terminal persistente.
- Capturar `stdout` e `stderr` em tempo real.
- Detectar quando um programa está esperando input.
- Permitir que Aurora escreva no `stdin`.
- Caso Aurora não saiba responder, perguntar ao usuário e continuar a execução.

---

## 🌐 2. Pesquisa Iterativa na Internet

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

## 🧠 3. Memória de Longo Prazo

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