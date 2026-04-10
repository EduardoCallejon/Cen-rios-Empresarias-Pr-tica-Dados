# Simulação arquitetura de dados Cenários de Empresas

Para esse projeto desmembrei em 3 cenários {Pequena, Média, Grande empresa}

## Pequena empresa
Para esse projeto fui utilizado as seguintes ferramentas:
- Vscode
- Bibliotecas estão no requeriments
- Orquestrador Dagster
- Docker

Para iniciar o projeto é necessário entender em que nível se encontra, se já existe uma stack, se ainda não existe, nesse cenário estamos simulando como se a empresa não tivesse projeto montando, então será necessário monta-lo. 

Montei um banco de dados simualção simulando os dados transacionais da empresa utilizando o site "SUPABASE"

<div align= "center">
<img width="500px" height="600" alt="Image" src="https://github.com/user-attachments/assets/f885c3a5-9c3b-4e42-b6e0-54d765297677" />
</div>


Análise de dados da empresa 📊

- A empresa é do ramo de varejo e trabalha com equipamentos eletrônicos
- Simples nacional
- Somente uma pessoa irá acessar o dashboard(Gerente)
- O objetivo do dono é entender melhor os dados comerciais para a tomada de decisão


Escolha da arquitetura 🧠

A estack utilizada será local como o cliente tem uma máquina que suporta essa arquitetura.

<div align= "center">
<img width="500px" height="600" alt="Image" src="https://github.com/user-attachments/assets/68193a25-5125-4dec-815a-64f01606b51a" />
</div>

Desenvolvimento 💻

Iniciamos, estabelecendo uma cadeia de conexão para podermos conversar com o banco de dados através do nosso VSCODE, ajustamos algumas medidas e transformações e já podemos iniciar a primeira carga para o nosso banco a "Carga inicial" que fica em "Pequena_empresa\Docker\Carga_inicial.py".

Para fins de conferência efetuamos uma consulta SQL, e vamos direto ao banco verfiicar se os dados chegaram corretamente ao seu destino, com esse processo feito, precisamos pensar em uma outra questão, se utilizarmos este código  toda  vez,  o mesmo irá limpar as tabelas e os dados serão inputados novamente, se estivermos tratando de um banco pequeno que é o caso ok, porém quando se trata de escalar isso se torna um problema, pois irá consumir tempo, memória, disco sem necessidade. Então optamos pela grande  *** Carga incremental ***, onde iremos utilizar uma coluna de referência e a partir da mesma iremos mandar para o nosso DW somente oque for *** Novo ***.

Criei o código incremental_carga, que vai fazer umva varredura na coluna data_venda dentro do dw, obter o último valor, ir ao banco transacional, pegar os dados somente que forem maior que este valor. Isso estamos tratando em um cenário onde os dados anteriores nao são alterados.

Com tudo isso concluído, chegou a hora de orquestrar isso tudo, que nada mais é de que ordenar para uma ferramente com qual frequência que esse código ira rodar, e também junto a isso ela vai nos oferecer dados muito importantes, como logs, e também irá nos fornecer um diagnóstico muito preciso de como a operação está se saindo, e apontar onde e como caso algum erro ocorrer, e para isso iremos utilizar o *** Dagster ***. 

Conclusão 🚩

Após todo esses processos, podemos assegurar que os dados chegarão de forma correta ao seu destino, e só assim iremos para a criação do dashboard que dará insights valiosos para para está analisando. 

<div align="Center">
<img width="600px" height="600px" alt="Image" src="https://github.com/user-attachments/assets/0c27c26a-0905-4cfd-8c8d-05b40c0741ce" />
<img width="500px" height="500px" alt="Image" src="https://github.com/user-attachments/assets/f765ef4f-2c42-41db-8e70-5cc2a11cffd1" />
<img width="500px" height="500px" alt="Image" src="https://github.com/user-attachments/assets/858582e5-26e1-4d79-8a4a-3110a0cc5cac" />
</div>