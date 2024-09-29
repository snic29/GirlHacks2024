#!/bin/bash

# 1. Open Az Cloud Shell
# 2. Upload the script and change permissions to 755
# 3. Upload the app updated file (zipped)
# 4. Execute the script passing the new app to be deployed as parameter


echo "Redeploying the application using $1 file ..."
az webapp config appsettings set --resource-group stelni-webapp --name resumeremix --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
az webapp deploy --name resumeremix --resource-group stelni-webapp --src-path $1 

echo " Done !!! \n"