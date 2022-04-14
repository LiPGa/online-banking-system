### Aplicação tipo To Do com Python Flask e CosmosDB usando API MongoDB para deploy em Azure WebApp

Baseado no tutorial de SARATH LAL https://codewithsarath.com/a-simple-to-do-python-flask-application-with-mongodb/
E da Azure https://docs.microsoft.com/pt-br/azure/cosmos-db/create-mongodb-flask

##### Requisitos

Conta grátis na Azure
https://azure.microsoft.com/pt-br/free/

Conta grátis do CosmosDB com API para MongoDB da Azure

Azure Cloud Shell


##### Instruções
Crie uma conta grátis na Azure seguindo as instruções
https://azure.microsoft.com/pt-br/free/

Crie uma conta CosmosDB com API para MongoDB da Azure

1. Na busca do portal.azure.com digite "cosmos" e clique em "Azure Cosmos DB"

2. Clique em +Adicionar

3. Selecione e complete dos dados

    Assinatura: Selecione "Avaliação Gratuita"
    
    Grupo de Recursos: Crie um novo Grupo de Recursos, lembre do nome pois usara depois

    Nome da Conta: Escolha um nome para a sua conta Cosmos DB

    API: Selecione API do Azure Cosmos DB para MongoDB

    Notebooks: Selecione Off

    Apply Free Tier Discount: Selecione Apply, isso lhe permitira usufruir o CosmosDB grátis.

    Localização: Selecione a localizacao geografica mais proxima de seus usuarios - (South America) Sul do Brasil

    Version: Selecione 3.6

    Redundancia Geografica: Selecione Disable

    Gravações de Várias Regiões: Selecione Disable

4. Clique em Revisar e Criar, aguarde a validação então clique em Create e aguarde a criação da conta.

5. Apos a conta ser criada, acesse ela, clique em Cadeia de Conexão (Connection String) copie a Cadeia de Conexão Primária (PRIMARY CONNECTION STRING)

6. Entre na Cloud Shell

7. Clone o codigo do github com o comando

    git clone https://github.com/azuretar/python-cosmosdb-azure-webapp-tutorial.git

8. Acesse a pasta e instale os pacotes necessarios com comando

    cd CosmosDBnoAzureWebApp
    pip install -r requirements.txt

9. Acesse a pasta e abra o editor online

    code .

10. Abra o arquivo app.py e cole a PRIMARY CONNECTION STRING no local indicado e pressione CTRL+S para salvar

11. Teste o codigo

    Na cloud shell digite

    python app.py
    e aperte enter

    Feche o editor online, clique no botao WebPreview, clique em Configure
    Escreva: 5000

    Clique em Open and Browse

    Veja se a pagina abre, volte a cloud shell aperte CTRL+C para parar e  vamos fazer o Deploy em um Azure Web App usando a AZ Cli

 12. Na Cloud Shell use comando

    az webapp up --sku F1 --name <Nome do seu Serviço de Aplicativos(WebApp)> --resource-group <Nome do grupo de recursos em que criou a sua conta CosmosDB>

    Aguarde a implantação

13. Na busca do Portal Azure digite Serviços de Aplicativo, clique em Serviçõs de Aplicativos

14. Voce vera seu WebApp listado, clique nele

15. Clique na URL para ver o seu WebApp funcionando!

16. Para apagar digite grupo de recursos na busca do Portal Azure, e clique em Grupo de Recursos, clique no Grupo de Recursos onde esta a conta do CosmosDB e o WebApp, clique em Excluir, escreva o nome do Grupo de Recursos e clique em Excluir.

