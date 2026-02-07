
import paramiko
import os
import sys
import time

# Remote config (hardcoded based on debug_server.py context)
HOST = "122.51.215.20"
USER = "root"
PASS = "A$#@^&*202601+."
CONTAINER_NAME = "yaothink-backend"

def run_remote_setup():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, username=USER, password=PASS)
        print("✅ SSH Connected")
        
        # Read the payload script
        payload_path = os.path.join(os.path.dirname(__file__), "remote_db_setup_payload.py")
        with open(payload_path, "r", encoding="utf-8") as f:
            payload_script = f.read()
            
        print(f"Reading payload from {payload_path} ({len(payload_script)} bytes)")
        
        # Command to run python inside docker getting input from stdin
        # We use 'python -u -' to run from stdin and unbuffered output
        docker_cmd = f"docker exec -i {CONTAINER_NAME} python -u -"
        
        print(f"Executing remote command: {docker_cmd}")
        stdin, stdout, stderr = client.exec_command(docker_cmd)
        
        # Write payload to stdin
        stdin.write(payload_script)
        stdin.channel.shutdown_write() # Signal EOF
        
        # Stream output
        print("\n--- Remote Output ---")
        while True:
            # Read line by line
            line = stdout.readline()
            if not line:
                break
            print(line, end="")
            
        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"\n--- Remote Stderr ---\n{error_output}")
            
        print("\n--- End of Output ---")
        
        # Check exit status
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("✅ Remote setup completed successfully.")
        else:
            print(f"❌ Remote setup failed with exit code {exit_status}.")

    except Exception as e:
        print(f"❌ Execution Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    run_remote_setup()
