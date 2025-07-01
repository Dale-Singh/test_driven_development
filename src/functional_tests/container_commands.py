# Standard library
import subprocess

# Username used for SSH connections to remote servers
USER = "dale"

# Public function to create a pre-authenticated session on a given host
def create_session_on_server(host, email):
    return _exec_in_container(
        host, ["/venv/bin/python", "/src/manage.py", "create_session", email]
    )

# Dispatch to the appropriate method depending on whether the host is local or remote
def _exec_in_container(host, commands):
    if "localhost" in host:
        return _exec_in_container_locally(commands)
    else:
        return _exec_in_container_on_server(host, commands)

# Run the given command inside a local Docker container
def _exec_in_container_locally(commands):
    print(f"Running {commands} on inside local docker container")
    return _run_commands(["docker", "exec", _get_container_id()] + commands)

# Run the given command inside a remote Docker container via SSH
def _exec_in_container_on_server(host, commands):
    print(f"Running {commands!r} on {host} inside docker container")
    return _run_commands(
        ["ssh", f"{USER}@{host}", "docker", "exec", "superlists"] + commands
    )

# Get the ID of the running Docker container based on the 'superlists' image
def _get_container_id():
    return subprocess.check_output(
        ["docker", "ps", "-q", "--filter", "ancestor=superlists"]
    ).strip()

# Run the given command and return the output, raise if it fails
def _run_commands(commands):
    process = subprocess.run(
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    result = process.stdout.decode()
    if process.returncode != 0:
        raise Exception(result)
    print(f"Result: {result!r}")
    return result.strip()
