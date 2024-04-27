#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m'

# Check if mkcert is installed

if ! command -v mkcert &> /dev/null
then
	echo -e "${RED} mkcert is not installed. Please install mkcert and run this script again. ${RESET}"
	exit 1
fi

# Prompt user to generate certificates
read -p "Do you want to generate SSL certificates? [yes/no]: " response

if [[ $response != "yes" ]]; then
	echo -e "${RED}Skipping certificate generation.${RESET}"
	exit 0
fi

# Generate certificates
echo "${GREEN}Generating SSL certificates...${RESET}"
mkcert pong.xyz localhost 127.0.0.1 ::1

# Move certificates to the correct location
echo "${GREEN}Moving certificates to the correct location...${RESET}"
mv *.pem ./nginx/certs/

echo "${GREEN}Certificates generated successfully.${RESET}"
