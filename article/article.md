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

.

Executadas as etapas supracitadas, prosseguimos com o treinamento do modelo. 

## **ABORDAGEM** <!-- Guilherme -->

Optamos pela utilização do modelo transformer para o treinamento da nossa rede neural. Essa escolha se deu pelo fato da mesma ser o atual estado da arte para modelos de linguagem focados na geração textual, superando até modelos clássicos como os RNNs padrões, GRUs e até as LSTM, que por muito tempo foram os modelos mais utilizados para esse tipo de trabalho, mas que sofriam de problemas ligados à otimização, visto que as células utilizadas não processam simultaneamente uma sequência de palavras, e sim sequencialmente palavra por palavra, o que aumentava consideravelmente o tempo de treinamento. Além disso, os transformers possuem uma maneira mais eficiente de recorrer às informações passadas. Enquanto as LSTMs e as GRUs utilizam das células de mémoria para se basear nas próximas gerações, os transformers têm acesso direto ao contexto, sem utilizar dessas células citadas anteriormente.

![transformers](article\images\transformers.png)

Nossa metodologia consistiu em utilizar o modelo pré-treinado distilgpt2, do huggingface, e então fazer o ajuste fino dos parâmetros utilizando uma grande base de dados contendo mais de 100.000 histórias de terror. O modelo distilgpt2 foi escolhido por ser a menor versão do GPT2, possuindo menos parâmetros e consequentemente sendo mais rápida e menos custosa para treinar, visto que para o treinamento foi utilizada uma única GPU disponibilizada através do Collab.

O nosso modelo foi treinado por cinco épocas, com oito batches, levando aproximadamente 12 horas e 53.705 passos de otimização. A base de dados possuia 107.402 textos onde 85.921 foram usados no treino e 21.481 foram usados na validação.

## **BACKGROUND E TRABALHOS RELACIONADOS** <!-- Douglas -->

## **CONCLUSÃO** <!-- Luiz -->

<!-- NOTES
1. escrever qual foi o tipo de persistencia escolhida - 1
2. escrever sobre o deploy da aplicação (qual ferramenta?) - 2
-->
Após a persistência do modelo para o disco <!--1-->, foi construído toda a interface, incluindo os templates e rotas de consumo. Para isso, foi utilizado o Flask, que é um microframework web escrito em Python, para a construção das rotas e HTML, CSS e Bootstrap -outro framework web de código aberto- para a construção dos templates renderizados pelas rotas do Flask.
<!--2-->
Após o desenvolvimento concluído da aplicação web, foi feito o deploy do mesmo, ou seja, a disponibilização do sistema em um ambiente no qual pode ser acessado e utilizado por qualquer pessoa. <!--Qual ferramenta?-->

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