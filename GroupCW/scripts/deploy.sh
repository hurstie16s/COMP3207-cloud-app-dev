#!/bin/bash
set -e
GRAY="\e[90m"
RED="\e[91m"
GREEN="\e[92m"
YELLOW="\e[93m"
BLUE="\e[94m"
MAGENTA="\e[95m"
CYAN="\e[96m"
RESET="\e[0m"

scriptPath=$(readlink -f $0)
root=$(dirname $(dirname $scriptPath))

echo -n -e "${YELLOW}Deploy backend? [Y/n]${RESET} "
read -r shouldDeployBackend
shouldDeployBackend=${shouldDeployBackend,,} # Lowercase
if [[ $shouldDeployBackend =~ ^(y| ) ]] || [[ -z $shouldDeployBackend ]]; then
  echo -e "\n${GREEN}Deploying backend...${RESET}"
  cd $root/AzureFunctions

  echo -n -e "${YELLOW}Enter the Azure function app ID (the function app *must* already exist): ${RESET}"
  read funcappid

  echo -e $GRAY
  set -x
  func azure functionapp publish $funcappid
  set +x
  $backendUrl="https://${funcappid}.azurewebsites.net"

  echo -e "${GREEN}Deployed backend to ${CYAN}${backendUrl}${RESET}"
fi

frontendZip="$root/src.zip"
function deleteOnExit {
  if [ -f "$frontendZip" ] ; then
    rm "$frontendZip"
  fi
}

echo -n -e "${YELLOW}Deploy frontend? [Y/n]${RESET} "
read -r shouldDeployFrontend
shouldDeployFrontend=${shouldDeployFrontend,,} # Lowercase
if [[ $shouldDeployFrontend =~ ^(y| ) ]] || [[ -z $shouldDeployFrontend ]]; then
  echo -e "\n${GREEN}Deploying frontend...${RESET}"
  cd $root

  echo -n -e "${YELLOW}Enter the Azure resource group name (this *must* already exist): ${RESET}"
  read resourceGroup

  echo -n -e "${YELLOW}Enter the Azure frontend webapp ID (this *must* already exist): ${RESET}"
  read webAppId

  echo -n -e "${YELLOW}Override Azure subscription ID? [y/N]${RESET} "
  read -r overrideSubscription
  overrideSubscription=${overrideSubscription,,} # Lowercase
  if [[ $overrideSubscription =~ ^(y) ]]; then
    echo -n -e "${YELLOW}Enter the Azure subscription ID: ${RESET}"
    read subscriptionId

    echo -e $GRAY
    set -x
    az account set --subscription $subscriptionId
    set +x
  fi

  if [ -z "$backendUrl" ]; then
    echo -n -e "${YELLOW}Enter the backend URL (no trailing slash): ${RESET}"
    read backendUrl
  fi

  trap deleteOnExit EXIT

  echo -e $GRAY
  set -x
  zip -r $frontendZip node_modules public/ views/ package.json package-lock.json app.js > /dev/null
  az webapp config appsettings set --resource-group $resourceGroup --name $webAppId --settings BACKEND=$backendUrl > /dev/null
  az webapp deploy --resource-group $resourceGroup --name $webAppId --src-path $frontendZip --type zip > /dev/null
  set +x

  frontendUrl="https://${webAppId}.azurewebsites.net"
  managementUrl="https://${webAppId}.scm.azurewebsites.net"
  echo -e "\n${GREEN}Deployed frontend to ${CYAN}${frontendUrl}${RESET}"
  echo -e "${GREEN}Management URL: ${CYAN}${managementUrl}${RESET}"
fi