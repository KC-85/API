import subprocess
import time

def start_redis():
    try:
        # Check if Redis is already running
        result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)

        if "PONG" in result.stdout:
            print("✅ Redis is already running.")
            return
        
        # Start Redis in daemon mode
        print("🚀 Starting Redis server...")
        subprocess.run(["redis-server", "--daemonize", "yes"], check=True)
        
        # Wait for Redis to fully start
        time.sleep(2)

        # Test if Redis started successfully
        result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
        if "PONG" in result.stdout:
            print("✅ Redis started successfully!")
        else:
            print("❌ Failed to start Redis.")
    
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    start_redis()
