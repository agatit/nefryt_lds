call npx @apidevtools/swagger-cli bundle ./openapi.yaml --outfile ./build/merged.yaml --type yaml
call npx @openapitools/openapi-generator-cli generate -i ./build/merged.yaml -g python-flask --package-name api --additional-properties=featureCORS=true -o ../backend
call npx @openapitools/openapi-generator-cli generate -i ./build/merged.yaml -g typescript-redux-query -o ../frontend

@echo done