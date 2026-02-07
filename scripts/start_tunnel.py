
import paramiko
from sshtunnel import SSHTunnelForwarder
import time
import sys

# Remote config
HOST = "122.51.215.20"
USER = "root"
PASS = "A$#@^&*202601+."

def run_tunnel():
    print(f"Opening SSH Tunnel to {HOST}...")
    print(f"Forwarding localhost:5432 -> remote:5432 (via docker db container)")
    
    # We need to forward to the 'db' container port 5432.
    # From the host's perspective (122.51.215.20), 'localhost:5432' maps to the db container 
    # IF the docker-compose exposes it.
    # debug_server.py logs didn't explicitly show ports, but docker-compose.yml has "5432:5432".
    # So connecting to 127.0.0.1:5432 ON THE REMOTE HOST should work.
    
    try:
        server = SSHTunnelForwarder(
            (HOST, 22),
            ssh_username=USER,
            ssh_password=PASS,
            remote_bind_address=('127.0.0.1', 5432),
            local_bind_address=('127.0.0.1', 5432)
        )
        
        server.start()
        print("✅ Tunnel established!")
        print("Local port 5432 is now forwarding to remote database.")
        print("Press Ctrl+C to stop.")
        
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Tunnel setup failed: {e}")
        print("Make sure no local Postgres is running on port 5432!")
    except KeyboardInterrupt:
        print("\nStopping tunnel...")
        server.stop()

if __name__ == "__main__":
    # Check if sshtunnel is installed
    try:
        import sshtunnel
    except ImportError:
        print("Please run: pip install sshtunnel")
        sys.exit(1)
        
    run_tunnel()
