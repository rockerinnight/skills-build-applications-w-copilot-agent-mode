const codespaceName = process.env.REACT_APP_CODESPACE_NAME;

const apiBase = codespaceName
  ? `https://${codespaceName}-8000.app.github.dev/api`
  : '/api';

export const buildApiUrl = (resource) => `${apiBase}/${resource}/`;

export const fetchAllPages = async (resource) => {
  let url = buildApiUrl(resource);
  const allResults = [];

  while (url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`${resource} request failed with status ${response.status}`);
    }

    const data = await response.json();
    if (Array.isArray(data)) {
      return data;
    }

    const pageResults = Array.isArray(data.results) ? data.results : [];
    allResults.push(...pageResults);
    url = data.next || null;
  }

  return allResults;
};
