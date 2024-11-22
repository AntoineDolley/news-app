# frontend/Dockerfile

# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React application
RUN npm run build

# Install serve to serve the build files
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the application
CMD ["serve", "-s", "build"]