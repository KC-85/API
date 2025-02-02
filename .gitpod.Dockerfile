FROM gitpod/workspace-full

# Install Redis
USER root
RUN sudo apt update && sudo apt install redis-server -y

# Expose Redis port
EXPOSE 6379

# Start Redis when the workspace starts
CMD ["redis-server", "--daemonize", "no", "--protected-mode", "no"]
