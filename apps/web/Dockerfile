FROM node:24-slim AS builder

ARG ENVIRONMENT=production
ARG NEXT_PUBLIC_API_URL=http://localhost:8000

WORKDIR /app

RUN npm install -g pnpm rimraf

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --no-frozen-lockfile

ENV ENVIRONMENT=$ENVIRONMENT
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY . .
RUN pnpm build


FROM node:24-slim AS runner

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --no-frozen-lockfile --prod

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

EXPOSE 3000

CMD ["pnpm", "start"]