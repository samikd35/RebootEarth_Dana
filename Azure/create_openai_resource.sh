#!/bin/bash

# Variables - modify these as needed
RESOURCE_GROUP="openai-resource-group"
LOCATION="eastus"  # Check available regions for Azure OpenAI
RESOURCE_NAME="my-openai-service"

# Create resource group if it doesn't exist
echo "Creating resource group if it doesn't exist..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure OpenAI resource
echo "Creating Azure OpenAI resource..."
az cognitiveservices account create \
  --name $RESOURCE_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --kind OpenAI \
  --sku S0

# Get the endpoint and keys
echo "Retrieving endpoint and keys..."
ENDPOINT=$(az cognitiveservices account show --name $RESOURCE_NAME --resource-group $RESOURCE_GROUP --query properties.endpoint -o tsv)
KEY=$(az cognitiveservices account keys list --name $RESOURCE_NAME --resource-group $RESOURCE_GROUP --query key1 -o tsv)

echo "Azure OpenAI resource created successfully!"
echo "Endpoint: $ENDPOINT"
echo "Key: $KEY"
echo "Save these values for future use."
