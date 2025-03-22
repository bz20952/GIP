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

# Set environment variables
ENV ENV=${ENV}
ENV PUBLIC_BACKEND_PORT=${PUBLIC_BACKEND_PORT}
ENV FRONTEND_PORT=${FRONTEND_PORT}

# Build the Svelte application
RUN npm run build

# Start Node server
CMD [ "node", "build" ]
