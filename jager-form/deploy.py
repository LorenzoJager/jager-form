import subprocess, sys, os

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERRORE: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def deploy(message=None):
    if not message:
        message = "Aggiornamento form"
    print("Deploying...")
    run('git add -A')
    status = subprocess.run('git diff --cached --quiet', shell=True)
    if status.returncode == 0:
        print("Nessuna modifica da deployare.")
        return
    run(f'git commit -m "{message}"')
    run('git push origin main')
    print("Deploy avviato! Render si aggiorna in 1-2 minuti.")
    print("https://jager-form.onrender.com")

if __name__ == '__main__':
    msg = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else None
    deploy(msg)
