import subprocess

def run_airflow_task_test(dag_id, task_id, execution_date):
    """Run the Airflow task test command."""
    command = [
        "airflow", "tasks", "test", dag_id, task_id, execution_date
    ]
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Command output:\n{result.stdout}")
        print(f"Command error:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running task test: {e}")
        print(f"Error output: {e.stderr}")