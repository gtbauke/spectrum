# ===========================
# 1. BUILD STAGE
# ===========================
FROM node:20 AS builder

WORKDIR /app

# Copy root workspace manifests
COPY package.json package-lock.json ./
COPY .env /app/.env

# Copy full monorepo (required for workspace resolution)
COPY . .

# Install ALL dependencies for ALL workspaces
RUN npm ci

# Generate Prisma client (shared, at root)
RUN npx prisma generate

# Build the API workspace
WORKDIR /app/packages/backend
RUN npm run build


# ===========================
# 2. PRODUCTION STAGE
# ===========================
FROM node:20-slim AS production

WORKDIR /app

# Copy root workspace manifests again (needed for npm ci)
COPY package.json package-lock.json ./

# Install ONLY production deps for ALL workspaces
RUN npm ci --omit=dev

# Copy built API workspace output
COPY --from=builder /app/packages/backend/dist ./dist

# Copy Prisma client (stored in root-level node_modules)
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder /app/node_modules/@prisma ./node_modules/@prisma

# (Optional) copy root-level prisma folder if running migrations inside container
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000
CMD ["node", "dist/index.js"]
