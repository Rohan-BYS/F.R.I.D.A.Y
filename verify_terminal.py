from friday_engine.aci.terminal import VerifiedTerminal

print("Testing VerifiedTerminal WITHOUT Docker (host execution)...")
term_host = VerifiedTerminal(use_docker=False)
obs = term_host.execute("echo 'host_execution'")
if obs.is_success and "host_execution" in obs.stdout:
    print("[PASSED] Host execution successful.")
else:
    print(f"[FAILED] Host execution failed. {obs.stderr}")

print("\nTesting VerifiedTerminal WITH Docker...")
term_docker = VerifiedTerminal(use_docker=True, container_name="friday_sandbox")
obs_docker = term_docker.execute("echo 'docker_execution'")
if obs_docker.is_success and "docker_execution" in obs_docker.stdout:
    print("[PASSED] Docker execution successful.")
else:
    print(f"[FAILED] Docker execution failed. (Is the container running?)")
    print(f"stderr: {obs_docker.stderr}")
    
