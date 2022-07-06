#!/bin/sh

npx @apidevtools/swagger-cli bundle ./openapi.yaml --outfile ./build/merged.yaml --type yaml
npx @openapitools/openapi-generator-cli generate -i ./build/merged.yaml -g python-flask --package-name api --additional-properties=featureCORS=true -o ../backend
npx @openapitools/openapi-generator-cli generate -i ./build/merged.yaml -g typescript-redux-query -o ../frontend