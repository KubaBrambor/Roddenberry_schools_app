FROM node:20

WORKDIR /app/frontend

# Use corepack instead of npm -g pnpm (more stable and versioned)
RUN corepack enable && corepack prepare pnpm@10.15.0 --activate

# Copy manifests separately (cache layers)
COPY package.json pnpm-lock.yaml* ./

# Copy the rest of the sources
COPY . .

EXPOSE 3000

# If node_modules is missing -> install deps; then start dev on all interfaces
CMD ["/bin/sh","-lc","set -e; if [ ! -x node_modules/.bin/nuxt ]; then echo '→ Installing deps…'; pnpm install --frozen-lockfile; fi; exec pnpm dev"]