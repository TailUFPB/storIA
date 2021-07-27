# StorIA
**Processamento de Linguagem Natural**

Participantes: *Douglas Antonio Monteiro, Felipe Honorato, Guilherme Jácome, Luiz Felipe Soares, Maria Victória Grisi, Rômulo Kunrath.*


Orientador: *Yuri Malheiros.*

*Realizado durante a rotação 2021.1*
*** 
## **INTRODUÇÃO** <!-- Felipe -->

Na última decada, com o acelerado avanço das tecnologias e dos algoritmos computacionais, diversas tarefas têm tido um salto de performace. Dentre elas, a área de Processamento de Linguagem Natural. Esse campo de pesquisa é responsável por toda a compreensão e reprodução da língua humana utilizando-se das mais diversas técnicas de deep learning. Visando explorar mais essa área e os modelos estado da arte, procuramos testar possibilidades na geração autoregressiva de textos. 

![Chatbot](article\images\chatbot.png)

Uma cena muito comum nos filmes de terror são as histórias contadas em volta de uma fogueira. Nesses ambientes, ocorrem diversas vezes trocas entre os narradores, que improvisam de acordo com sua criatividade continuações, o que confere à história diversidade e imprevisibilidade.

![fogueira](article\images\fogueira.jpg)

Pensando nisso, o projeto utiliza de modelos de inteligência artificial que permitem que um usuário escreva em parceria com uma máquina, que, utilizando de um conhecimento linguístico, simula a participação de outros narradores na escritava colaborativa.


## **CONSTRUÇÃO DO DATASET** <!-- Rômulo -->

## **PRÉ-PROCESSAMENTO** <!-- Victória -->

O pré-processamento feito consiste em buscar remover imperfeições dos textos do nosso dataset, algo que é bastante comum em dados que não são totalmente controlados como os obtidos em fóruns e redes sociais. Essa etapa é de fundamental importância pois o texto visto servirá de "molde" para os textos que serão gerados pela máquina.

### **1. Remover linhas que estivessem com o corpo do texto deletado ou duplicado.**
Dentro do dataset foi possível encontrar uma boa quantidade de linhas duplicadas ou com o atributo do corpo de texto descritos como "deleted" ou "removed". Optamos por deletar a linha inteira caso detectássemos algum destes casos.
### **2. Substituir, através de expressões regulares, pedaços de texto que atrapalhariam no treinamento.**
Muitos dos textos possuíam links, que retiramos, e cadeias de caracteres que fazem parte da sintaxe do Markdown. Como a intenção é que o modelo gerasse textos para serem lidos em HTML, foi necessário substituir as partes em Markdown, principalmente as quebras de linha.
### **3. Adicionar tokens de marcação.**
Inserimos dentro dos textos os tokens de início de texto ```<|startoftext|>``` e de fim de texto ```<|endoftext|>```. Além disso, adicionamos a marcação de quebra de linha em HTML, o ```<br>```, como token para o nosso modelo.
### **4. Dividir o dataset em dois.**
Separamos nossos dados tratados em duas váriaveis, o dataset de treinamento, que fica com 80% dos textos, e o dataset de teste, que fica com os outros 20%.
### **5. Criar o tokenizer e o dividí-lo em batches.**

Executadas as etapas supracitadas, prosseguimos com o treinamento do modelo. 

## **ABORDAGEM** <!-- Guilherme -->

Optamos pela utilização do modelo transformer para o treinamento da nossa rede neural. Essa escolha se deu pelo fato da mesma ser o atual estado da arte para modelos de linguagem focados na geração textual, superando até modelos clássicos como os RNNs padrões, GRUs e até as LSTM, que por muito tempo foram os modelos mais utilizados para esse tipo de trabalho, mas que sofriam de problemas ligados à otimização, visto que as células utilizadas não processam simultaneamente uma sequência de palavras, e sim sequencialmente palavra por palavra, o que aumentava consideravelmente o tempo de treinamento. Além disso, os transformers possuem uma maneira mais eficiente de recorrer às informações passadas. Enquanto as LSTMs e as GRUs utilizam das células de mémoria para se basear nas próximas gerações, os transformers têm acesso direto ao contexto, sem utilizar dessas células citadas anteriormente.

![transformers](article\images\transformers.png)

Nossa metodologia consistiu em utilizar o modelo pré-treinado distilgpt2, do huggingface, e então fazer o ajuste fino dos parâmetros utilizando uma grande base de dados contendo mais de 100.000 histórias de terror. O modelo distilgpt2 foi escolhido por ser a menor versão do GPT2, possuindo menos parâmetros e consequentemente sendo mais rápida e menos custosa para treinar, visto que para o treinamento foi utilizada uma única GPU disponibilizada através do Collab.

O nosso modelo foi treinado por cinco épocas, com oito batches, levando aproximadamente 12 horas e 53.705 passos de otimização. A base de dados possuia 107.402 textos onde 85.921 foram usados no treino e 21.481 foram usados na validação.

## **BACKGROUND E TRABALHOS RELACIONADOS** <!-- Douglas -->

Com a ascensão e popularização de cada vez mais tecnologias voltadas para a criação de modelos de NLP, é notório observar que muitas abordagens vêm surgindo e inspirando cada vez mais pessoas a trabalhar embasados em determinadas soluções. De tal modo, é necessário destacar alguns projetos que se assimilam ao StorIA e que aumentam a gama de programas com solução de processamento de linguagem natural para melhor compreensão e estudo. 

**1. Write with transformer**

[Transformer](https://transformer.huggingface.co/) -
Construído e idealizado pela comunidade de inteligência artificial, Hugging Face, o Write with Transformer, é a web app de demonstração oficial do transformers. Nela a NLP da ferramenta é utilizada para completar inputs que o usuário à medida que ele vai escrevendo em um ambiente de escrita similar ao Microsoft Word. O usuário pode optar por iniciar um texto do zero, gerar um texto inicial aleatório e ir recebendo sugestões do modelo conforme vai escrevendo.

**2. AI Dungeon**

[AI Dungeon](https://play.aidungeon.io/main/home) -
O AI Dungeon é um jogo online gratuito baseado em uma aventura de textos, simulando uma mesa de RPG. Nela o programa é utilizado para gerar a história enquanto o jogador é responsável por agir, falar ou complementar a história dizendo o que aconteceria em seguida. A ideia desse jogo foi concebida por um estudante chamado Nick Walton durante uma hackathon, e foi inicialmente desenvolvida utilizando uma versão inicial da rede neural GPT-2.


## **CONCLUSÃO** <!-- Luiz -->

Após o treinamento do modelo, foi gerado todos os checkpoints para recriá-lo e construído toda a interface, incluindo os templates e rotas de consumo. Para isso, foi utilizado o Flask, que é um microframework web escrito em Python, para a construção das rotas e HTML, CSS e Bootstrap -outro framework web de código aberto- para a construção dos templates renderizados pelas rotas do Flask. Algo importante a se comentar é que, como os checkpoints do modelo são bem pesados, ou seja, ultrapassam os limites de tamanho de arquivo do git (100mb). Dessa forma, o consumo do modelo foi realizado via API de compartilhamento do Hugging Face e não precisou fazer a persistência do modelo para o disco. Assim, os dados (texto, temperatura e tamanho) são enviados pelo formulário e recebidos pelo Flask, onde ocorre um pequeno pré-processamento, apenas para adequar o formato de entrada. Após isso, os dados de entrada são enviados na requisição para o modelo como parâmetros e o texto gerado é retornado.

Após ter a interface finalizada e funcional localmente, foi realizado o deploy da aplicação via [Heroku](https://www.heroku.com/home). Os passos são bem simples, sendo necessário apenas criar uma conta, conectar com a do Github e escolher um repositório com o formato adequado, ou seja, com o arquivo requirements.txt com as bibliotecas que devem ser instaladas e o arquivo Procfile que tem o comando de inicialização da aplicação, que nesse caso foi ```web: gunicorn app:app```. Lembrando que o código e toda essa estrutura pode ser visualizado em nosso [repositório](https://github.com/TailUFPB/storIA) no Github.

Para avaliação do modelo, utilizamos a perplexidade, que é uma métrica que avalia, de acordo com nossa fatia de dados separadas para validação, quão bem o modelo consegue predizer a próxima palavra de uma história. Ou seja, compara o texto gerado palavra a palavra pelo modelo com uma parte dos textos do dataset. A perplexidade atingiu o valor de  22.194 na etapa final do treinamento.

#### **Alguns exemplos de geração colaborativa utilizando nosso modelo**: 

_História 1:_    
```input: me and alicia were investigating a murder in los angeles```
 

``` output: we were looking for clues as to who was responsible, but we couldn't find anything. we had to go back to the house to find whoever was responsible. we didn't know who it was until we got to the basement.```  

_História 2:_  
```input:  when i was a child, i used to hear voices in my head, they were always telling```

```output: me that i was being watched, and that i needed to be quiet. i wasn’t allowed to do that, so i was forced to listen to the voices. they told me “i’m going to die soon```  

## **TRABALHOS FUTUROS E MELHORIAS**
Para obtermos gerações ainda melhores, testaremos modelos maiores da GPT2, bem como os novos modelos GPT-Neo. Além disso, buscaremos acrescentar mais dados à nossa base para que o modelo possua uma maior diversidade de histórias e adquira melhor conhecimento linguístico nesse campo específico de histórias de terror.

Outra possibilidade já mapeada é acrescentar um narrador para as histórias, para que a experiência fique ainda mais imersiva e adicionar ao modelo a geração de uma imagem com base no local onde se passa a história gerada.

Pretendemos também fazer uma segunda versão da interface para melhorar a experiência da geração do texto para o usuário, deixar mais chamativa e acrescentar elementos visuais para uma maior interação. E por fim, a criação de algum tipo de template para que o usuário, ao terminar o texto, possa fazer o download ou compartilhar em redes sociais.
