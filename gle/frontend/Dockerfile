# Use an official Node.js runtime as a parent image
FROM node:22-slim

# Set the working directory
WORKDIR /web

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Svelte application and start node server
CMD ["sh", "-c", "npm run build && node build"]
