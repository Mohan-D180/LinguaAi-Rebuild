# syntax=docker/dockerfile:1.7
FROM node:22-alpine

WORKDIR /app

COPY --chown=node:node package.json package-lock.json ./
RUN chown node:node /app \
    && mkdir -p /home/node/.npm \
    && chown node:node /home/node/.npm
USER node

RUN --mount=type=cache,id=linguaai-frontend-npm,target=/home/node/.npm,uid=1000,gid=1000 npm ci

COPY --chown=node:node . .

EXPOSE 5173

HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=5 \
  CMD node -e "fetch('http://127.0.0.1:5173/').then((response) => process.exit(response.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["sh", "-c", "npm ci --prefer-offline --no-audit --no-fund && npm run dev -- --host 0.0.0.0"]
