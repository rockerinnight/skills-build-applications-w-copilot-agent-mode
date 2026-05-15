const codespaceName = process.env.REACT_APP_CODESPACE_NAME;

const apiBase = codespaceName
  ? `https://${codespaceName}-8000.app.github.dev/api`
  : '/api';

export const buildApiUrl = (resource) => `${apiBase}/${resource}/`;
