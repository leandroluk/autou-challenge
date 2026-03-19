FROM node:24-slim AS builder

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm build


FROM node:24-slim

WORKDIR /app

RUN npm install -g pnpm

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

ENV ENVIRONMENT=production \
    NEXT_PUBLIC_API_URL=http://localhost:8000

EXPOSE 3000

CMD ["node", "server.js"]