"""
Remote Server Debug Script
uses paramiko to inspect docker containers and logs
"""
import paramiko
import sys
import io

# Set encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HOST = "122.51.215.20"
USER = "root"
PASS = "A$#@^&*202601+."

def run_cmd(ssh, cmd):
    print(f"\n[EXEC] {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    
    if out:
        print(f"[STDOUT]\n{out.strip()}")
    if err:
        print(f"[STDERR]\n{err.strip()}")
    
    return out, err

def debug_server():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, username=USER, password=PASS)
        print("✅ SSH Connected")
        
        # 1. Check Containers
        run_cmd(client, "docker ps")
        
        # 2. Check Nginx Logs (Frontend)
        # Assuming container name is yaothink-frontend
        print("\n=== Nginx Logs (Last 50) ===")
        run_cmd(client, "docker logs --tail 50 yaothink-frontend")
        
        # 3. Check Backend Logs
        print("\n=== Backend Logs (Last 50) ===")
        run_cmd(client, "docker logs --tail 50 yaothink-backend")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    debug_server()
