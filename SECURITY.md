# Security — EXPANSÃO360

## Política de Secrets
- Nunca versionar arquivos `.env`, chaves, tokens, credenciais, certificados ou dumps de banco.
- Use `.env.example` apenas com placeholders.
- Se um secret vazar no Git, considerar comprometido e rotacionar imediatamente.

## Boas práticas
- Preferir variáveis de ambiente e secret managers quando aplicável.
- Evitar credenciais hardcoded em código e testes.
- Revisar commits antes de push quando houver configuração/infra.
