const rawContent = $input.item.json.data; 
const filename = $input.item.json.filename;
const sha = $input.item.json.sha;

const yaml = require('js-yaml');
let api;

try {
  api = yaml.load(rawContent);
} catch (e) {
  api = typeof rawContent === 'string' ? JSON.parse(rawContent) : rawContent;
}

const schemas = api.components?.schemas || {};
const apiTitle = api.info?.title || "API Sans Titre";
const apiGlobalDesc = api.info?.description || "";

function resolveSchema(schema) {
  if (!schema) return "N/A";
  if (schema.$ref) {
    const schemaName = schema.$ref.split('/').pop();
    return resolveSchema(schemas[schemaName]);
  }
  if (schema.type === 'array' && schema.items) {
    return `Array of ${resolveSchema(schema.items)}`;
  }
  if (schema.type === 'object' && schema.properties) {
    const props = {};
    for (const [key, value] of Object.entries(schema.properties)) {
      props[key] = {
        type: value.type,
        description: value.description || "",
        example: value.example || ""
      };
    }
    return JSON.stringify(props);
  }
  return schema.type || "string";
}

const results = [];

for (const [path, pathMethods] of Object.entries(api.paths || {})) {
  const pathLevelParams = (pathMethods.parameters || []).map(p => 
    `${p.name} (dans ${p.in}): ${p.description || ""}`
  ).join(', ');

  for (const [method, detail] of Object.entries(pathMethods)) {
    if (method === 'parameters') continue;

    const methodParams = (detail.parameters || []).map(p => 
      `${p.name} (dans ${p.in}): ${p.description || ""}`
    ).join(', ');

    const allParams = [pathLevelParams, methodParams].filter(p => p).join(' | ');
    const reqBodySchema = detail.requestBody?.content?.['application/json']?.schema;
    const resolvedReqBody = reqBodySchema ? resolveSchema(reqBodySchema) : "Aucun corps requis";
    const successCode = detail.responses?.['201'] ? '201' : '200';
    const respSchema = detail.responses?.[successCode]?.content?.['application/json']?.schema;
    const resolvedResponse = resolveSchema(respSchema);

    const semanticText = `
API TITLE: ${apiTitle}
SERVICE DESCRIPTION: ${apiGlobalDesc}
---
ENDPOINT: ${method.toUpperCase()} ${path}
SUMMARY: ${detail.summary || "Non défini"}
DESCRIPTION: ${detail.description || "Non définie"}
PARAMÈTRES: ${allParams || "Aucun"}
BODY REQUIS: ${resolvedReqBody}
RÉPONSE SUCCESS (${successCode}): ${resolvedResponse}
    `.trim();

    results.push({
      json: {
        id: `${apiTitle}-${method}-${path}`.toLowerCase().replace(/[^a-z0-9]/gi, '-'),
        text: semanticText,
        metadata: {
          api_name: apiTitle,
          method: method.toUpperCase(),
          path: path,
          filename: filename
        }
      }
    });
  }
}

return results;