// On récupère les données du nœud précédent (GitHub Get File)
const rawContent = $input.item.json.data; 
const filename = $input.item.json.filename;
const sha = $input.item.json.sha;

const yaml = require('js-yaml');
let api;

try {
  api = yaml.load(rawContent);
} catch (e) {
  // Fallback au cas où le contenu arrive déjà en JSON
  api = typeof rawContent === 'string' ? JSON.parse(rawContent) : rawContent;
}

const schemas = api.components?.schemas || {};
const apiTitle = api.info?.title || "API Sans Titre";
const apiGlobalDesc = api.info?.description || "";

/**
 * Fonction de déréférencement récursive
 * Elle explore les objets, les tableaux et les liens $ref
 */
function resolveSchema(schema) {
  if (!schema) return "N/A";

  // Si c'est une référence, on va chercher l'objet cible
  if (schema.$ref) {
    const schemaName = schema.$ref.split('/').pop();
    return resolveSchema(schemas[schemaName]);
  }

  // Cas d'un tableau (ex: la liste des clients dans ton GET /customers)
  if (schema.type === 'array' && schema.items) {
    return `Array of ${resolveSchema(schema.items)}`;
  }

  // Cas d'un objet (ex: le schéma Customer)
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

// Parcours des chemins (ex: /customers, /customers/{id})
for (const [path, pathMethods] of Object.entries(api.paths || {})) {
  
  // Certains paramètres peuvent être au niveau du PATH (comme le ID)
  const pathLevelParams = (pathMethods.parameters || []).map(p => 
    `${p.name} (dans ${p.in}): ${p.description || ""}`
  ).join(', ');

  for (const [method, detail] of Object.entries(pathMethods)) {
    // On ignore le champ 'parameters' s'il est au niveau du path
    if (method === 'parameters') continue;

    // 1. Gestion des paramètres spécifiques à la méthode (Query, Header)
    const methodParams = (detail.parameters || []).map(p => 
      `${p.name} (dans ${p.in}): ${p.description || ""}`
    ).join(', ');

    const allParams = [pathLevelParams, methodParams].filter(p => p).join(' | ');

    // 2. Déréférencement du Request Body (pour les POST/PUT)
    const reqBodySchema = detail.requestBody?.content?.['application/json']?.schema;
    const resolvedReqBody = reqBodySchema ? resolveSchema(reqBodySchema) : "Aucun corps requis";

    // 3. Déréférencement de la réponse principale (200 ou 201)
    const successCode = detail.responses?.['201'] ? '201' : '200';
    const respSchema = detail.responses?.[successCode]?.content?.['application/json']?.schema;
    const resolvedResponse = resolveSchema(respSchema);

    // 4. Construction du texte sémantique enrichi
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

    // 5. Envoi vers l'item n8n
    results.push({
      json: {
        id: `${apiTitle}-${method}-${path}`.toLowerCase().replace(/[^a-z0-9]/gi, '-'),
        text: semanticText,
        metadata: {
          api_name: apiTitle,
          method: method.toUpperCase(),
          path: path,
          tags: (detail.tags || []).join(','),
          filename: filename
        }
      }
    });
  }
}

return results;