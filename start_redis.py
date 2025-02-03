import docker
import time

def start_redis():
    client = docker.from_env()

    # Check if Redis container exists
    try:
        redis_container = client.containers.get("redis")
        if redis_container.status != "running":
            print("🔄 Starting Redis container...")
            redis_container.start()
            time.sleep(2)  # Wait for Redis to fully start
            print("✅ Redis started successfully!")
        else:
            print("🚀 Redis is already running.")
    except docker.errors.NotFound:
        print("⚠️ Redis container not found. Creating a new one...")
        client.containers.run("redis", name="redis", detach=True, ports={"6379/tcp": 6379})
        time.sleep(2)
        print("✅ New Redis container created and started!")

    # Check Redis connection
    exec_result = redis_container.exec_run("redis-cli ping")
    if b"PONG" in exec_result.output:
        print("✅ Redis is working!")
    else:
        print("❌ Redis failed to start!")

if __name__ == "__main__":
    start_redis()
