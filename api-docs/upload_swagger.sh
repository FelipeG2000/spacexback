#!/bin/bash

set -e

TEMPLATE="api-docs/swagger_template.yaml"
OUTPUT="api-docs/swagger_ui/swagger.yaml"
BUCKET_NAME="spacex-swagger-ui-$(aws sts get-caller-identity --query Account --output text)"

export API_URL=$(aws cloudformation describe-stacks \
  --stack-name spacex-backend \
  --query "Stacks[0].Outputs[?OutputKey=='SpaceXLaunchesApiEndpoint'].OutputValue" \
  --output text)

if [ -z "$API_URL" ]; then
  echo "❌ API_URL is empty. Make sure your stack is deployed and has the correct output."
  exit 1
fi

# 🛡️ Proteger los $ref reemplazándolos temporalmente
cp "$TEMPLATE" "${TEMPLATE}.tmp"
sed -i 's/\$ref/__REF__/g' "${TEMPLATE}.tmp"

# 💾 Interpolar solo variables reales
echo "🔧 Generating swagger.yaml using API_URL=${API_URL}..."
envsubst < "${TEMPLATE}.tmp" > "$OUTPUT"

# ♻️ Restaurar los $ref
sed -i 's/__REF__/\$ref/g' "$OUTPUT"

# 🚀 Subir a S3
echo "📤 Uploading Swagger UI to S3..."
aws s3 sync api-docs/swagger_ui/ "s3://${BUCKET_NAME}/" --delete

# 🧹 Limpiar
rm "${TEMPLATE}.tmp"

echo "✅ Swagger UI available at:"
echo "https://${BUCKET_NAME}.s3.amazonaws.com/index.html"
