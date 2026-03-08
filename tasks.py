"""Eastleigh FC Academy - Invoke Task Runner"""
from invoke import task, Context
import os
import sys
import subprocess

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

def print_success(text="Success"):
    print(f"\n{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"\n{Colors.FAIL}✗ {text}{Colors.ENDC}")

def get_python_cmd():
    """Find the correct Python command"""
    for cmd in ['python3', 'python', 'py']:
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return 'python3'

def get_pip_cmd():
    """Find the correct pip command"""
    for cmd in ['pip3', 'pip']:
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return 'pip3'

PYTHON = get_python_cmd()
PIP = get_pip_cmd()

# ==================== SETUP & INSTALLATION ====================

@task
def install(c):
    """Install frontend dependencies (npm install)"""
    print_header("Installing Frontend Dependencies")
    with c.cd("frontend"):
        c.run("npm install", pty=True)
    print_success("Frontend dependencies installed")

@task
def install_backend(c):
    """Install backend dependencies (pip install)"""
    print_header("Installing Backend Dependencies")
    with c.cd("backend"):
        c.run(f"{PIP} install -r requirements.txt", pty=True)
    print_success("Backend dependencies installed")

@task
def setup(c):
    """Full setup - install all dependencies"""
    print_header("FULL PROJECT SETUP")
    install_backend(c)
    install(c)
    print_success("Setup complete! Run 'invoke build' next")

# ==================== DOCKER COMMANDS ====================

@task
def build(c):
    """Build all Docker images"""
    print_header("Building Docker Images")
    c.run("docker-compose build --no-cache", pty=True)
    print_success("Docker images built")

@task
def start(c):
    """Start all services (detached mode)"""
    print_header("Starting All Services")
    c.run("docker-compose up -d", pty=True)
    print_success("Services started!")
    print(f"\n{Colors.OKGREEN}Access Points:{Colors.ENDC}")
    print("  🌐 Website:    http://localhost:3000")
    print("  🔧 API:        http://localhost:5000/api")
    print("  🗄️  Database:  http://localhost:8080 (Adminer)")

@task
def stop(c):
    """Stop all services"""
    print_header("Stopping Services")
    c.run("docker-compose stop", pty=True)
    print_success("Services stopped")

@task
def down(c):
    """Stop and remove all containers"""
    print_header("Removing Containers")
    c.run("docker-compose down", pty=True)
    print_success("Containers removed")

@task
def restart(c, service=None):
    """Restart all or specific service"""
    if service:
        print_header(f"Restarting {service}")
        c.run(f"docker-compose restart {service}", pty=True)
        print_success(f"{service} restarted")
    else:
        print_header("Restarting All Services")
        c.run("docker-compose restart", pty=True)
        print_success("All services restarted")

@task
def reset(c):
    """⚠️ Full reset - removes containers, volumes, and rebuilds"""
    print(f"\n{Colors.WARNING}⚠️  WARNING: This will DELETE all database data!{Colors.ENDC}")
    response = input("Type 'yes' to continue: ")
    if response.lower() == 'yes':
        print_header("Full Reset in Progress")
        c.run("docker-compose down -v --remove-orphans", pty=True)
        print("Rebuilding...")
        c.run("docker-compose up -d --build", pty=True)
        print_success("Reset complete! Run 'invoke init' to seed data")
    else:
        print("Cancelled")

@task
def logs(c, service=None, follow=False):
    """View logs (use -f to follow)"""
    cmd = "docker-compose logs"
    if follow:
        cmd += " -f"
    if service:
        cmd += f" {service}"
        print_header(f"Logs for {service} {'(following)' if follow else ''}")
    else:
        print_header(f"All Logs {'(following)' if follow else ''}")
    
    c.run(cmd, pty=True)

@task
def ps(c):
    """List running containers"""
    print_header("Container Status")
    c.run("docker-compose ps", pty=True)

@task
def status(c):
    """Show detailed system status"""
    print_header("SYSTEM STATUS")
    c.run("docker-compose ps", pty=True)
    print(f"\n{Colors.OKCYAN}API Health Check:{Colors.ENDC}")
    c.run("curl -s http://localhost:5000/api/health || echo 'Backend not responding'", pty=True, warn=True)

# ==================== DATABASE COMMANDS ====================

@task
def init(c):
    """Initialize database with sample data"""
    print_header("Initializing Database")
    c.run("curl -X POST http://localhost:5000/api/init", pty=True)
    print_success("Database initialized with sample data")

@task
def db_shell(c):
    """Open PostgreSQL interactive shell"""
    print_header("Opening PostgreSQL Shell")
    c.run("docker-compose exec db psql -U postgres -d eastleigh_academy", pty=True)

@task
def backup(c, filename=None):
    """Backup database (auto-timestamp if no filename)"""
    if not filename:
        import datetime
        filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    print_header(f"Creating Backup: {filename}")
    c.run(f"docker-compose exec -T db pg_dump -U postgres eastleigh_academy > {filename}", pty=True)
    print_success(f"Backup saved to {filename}")

@task
def restore(c, filename):
    """Restore database from backup file"""
    if not os.path.exists(filename):
        print_error(f"File not found: {filename}")
        sys.exit(1)
    
    print_header(f"Restoring from {filename}")
    c.run(f"docker-compose exec -T db psql -U postgres eastleigh_academy < {filename}", pty=True)
    print_success("Database restored")

# ==================== ALEMBIC MIGRATION COMMANDS ====================

@task
def alembic_init(c):
    """Initialize Alembic migrations (run once)"""
    print_header("Initializing Alembic")
    with c.cd("backend"):
        if os.path.exists("migrations"):
            print(f"{Colors.WARNING}Migrations already initialized{Colors.ENDC}")
            return
        c.run(f"{PYTHON} -m alembic init migrations", pty=True)
        print(f"\n{Colors.OKCYAN}Updating configuration...{Colors.ENDC}")
        
        # Update env.py to import models
        env_py = '''import sys
sys.path.append('.')

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import db

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.Model.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
        with open("migrations/env.py", "w") as f:
            f.write(env_py)
        
        # Update alembic.ini with database URL
        c.run("sed -i '' 's|driver://user:pass@localhost/dbname|postgresql://postgres:postgres@localhost:5432/eastleigh_academy|' alembic.ini 2>/dev/null || true", warn=True)
    
    print_success("Alembic initialized!")
    print(f"\n{Colors.OKCYAN}Next steps:{Colors.ENDC}")
    print("1. Run: invoke alembic-revision -m 'initial'")
    print("2. Run: invoke alembic-upgrade")

@task
def alembic_revision(c, m="auto migration"):
    """Create new migration (auto-detects model changes)"""
    print_header(f"Creating Migration: {m}")
    with c.cd("backend"):
        c.run(f'{PYTHON} -m alembic revision --autogenerate -m "{m}"', pty=True)
    print_success("Migration created!")

@task
def alembic_upgrade(c, revision="head"):
    """Upgrade database (default: head = latest)"""
    print_header(f"Upgrading to: {revision}")
    with c.cd("backend"):
        c.run(f"{PYTHON} -m alembic upgrade {revision}", pty=True)
    print_success("Database upgraded!")

@task
def alembic_downgrade(c, revision="-1"):
    """Downgrade database (default: -1 = previous)"""
    print_header(f"Downgrading to: {revision}")
    print(f"{Colors.FAIL}⚠️  This may cause data loss!{Colors.ENDC}")
    if input("Type 'yes' to continue: ").lower() == 'yes':
        with c.cd("backend"):
            c.run(f"{PYTHON} -m alembic downgrade {revision}", pty=True)
        print_success("Database downgraded!")
    else:
        print("Cancelled")

@task
def alembic_history(c):
    """Show migration history"""
    print_header("Migration History")
    with c.cd("backend"):
        c.run(f"{PYTHON} -m alembic history --verbose", pty=True)

@task
def alembic_current(c):
    """Show current database version"""
    print_header("Current Database Version")
    with c.cd("backend"):
        c.run(f"{PYTHON} -m alembic current", pty=True)

@task
def alembic_stamp(c, revision="head"):
    """Stamp database without running migrations"""
    print_header(f"Stamping at: {revision}")
    with c.cd("backend"):
        c.run(f"{PYTHON} -m alembic stamp {revision}", pty=True)
    print_success("Database stamped!")

# ==================== DEVELOPMENT COMMANDS ====================

@task
def dev(c):
    """Start backend + frontend with auto-install check"""
    import time
    
    print_header("Starting Development Environment")
    
    # Check if node_modules exists
    if not os.path.exists("frontend/node_modules"):
        print(f"{Colors.WARNING}⚠️  Frontend dependencies not found{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Running npm install first...{Colors.ENDC}\n")
        with c.cd("frontend"):
            c.run("npm install", pty=True)
        print_success("Dependencies installed")
    
    # Check if backend packages exist
    try:
        result = subprocess.run([PYTHON, "-c", "import flask"], capture_output=True, cwd="backend")
        if result.returncode != 0:
            raise Exception("Flask not found")
    except Exception:
        print(f"{Colors.WARNING}⚠️  Backend dependencies not found{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Running pip install...{Colors.ENDC}\n")
        with c.cd("backend"):
            c.run(f"{PIP} install -r requirements.txt", pty=True)
        print_success("Backend dependencies installed")
    
    print(f"\n{Colors.OKGREEN}Starting servers:{Colors.ENDC}")
    print(f"  Backend:  http://localhost:5000/api")
    print(f"  Frontend: http://localhost:3000")
    print(f"  {Colors.WARNING}Press Ctrl+C to stop both{Colors.ENDC}\n")
    
    # Start backend in background
    c.run(f"cd backend && ({PYTHON} app.py > ../backend.log 2>&1 & echo $! > ../.backend.pid)")
    print(f"{Colors.OKCYAN}✓ Backend starting...{Colors.ENDC}")
    time.sleep(3)
    
    # Start frontend (this blocks)
    print(f"{Colors.OKCYAN}✓ Starting frontend...{Colors.ENDC}\n")
    try:
        with c.cd("frontend"):
            c.run("npm start", pty=True)
    finally:
        # Cleanup when frontend stops
        c.run("kill $(cat .backend.pid) 2>/dev/null; rm -f .backend.pid", warn=True)
        print(f"\n{Colors.WARNING}Servers stopped{Colors.ENDC}")

@task
def stopdev(c):
    """Stop development servers"""
    c.run("kill $(cat .backend.pid) 2>/dev/null; rm -f .backend.pid", warn=True)
    c.run("pkill -f 'npm start' 2>/dev/null", warn=True)
    c.run("pkill -f 'react-scripts' 2>/dev/null", warn=True)
    print_success("Development servers stopped")

@task
def dev_frontend(c):
    """Run frontend locally with npm (hot reload)"""
    print_header("Starting React Dev Server")
    print(f"{Colors.WARNING}Note: Runs on http://localhost:3001 if 3000 is taken{Colors.ENDC}\n")
    with c.cd("frontend"):
        c.run("npm start", pty=True)

@task
def dev_backend(c):
    """Run backend locally with Flask (hot reload)"""
    print_header("Starting Flask Dev Server")
    print(f"{Colors.WARNING}Note: Requires: {PIP} install -r requirements.txt{Colors.ENDC}\n")
    with c.cd("backend"):
        c.run(f"{PYTHON} app.py", pty=True)

# ==================== UTILITY COMMANDS ====================

@task
def shell(c, service="backend"):
    """Open shell in container (default: backend)"""
    print_header(f"Opening shell in {service}")
    c.run(f"docker-compose exec {service} sh", pty=True)

@task
def clean(c):
    """Clean unused Docker resources"""
    print_header("Cleaning Docker System")
    c.run("docker system prune -f", pty=True)
    c.run("docker volume prune -f", pty=True)
    print_success("Docker cleaned")

@task
def test(c):
    """Run tests"""
    print_header("Running Tests")
    with c.cd("backend"):
        c.run(f"{PYTHON} -m pytest", pty=True, warn=True)

@task
def admin(c):
    """Show admin panel access info"""
    print(f"""
{Colors.HEADER}{'='*60}{Colors.ENDC}
{Colors.BOLD}ADMIN PANEL ACCESS{Colors.ENDC}
{Colors.HEADER}{'='*60}{Colors.ENDC}

  1. Open: http://localhost:3000
  2. Click the shield icon (🛡️) in top navigation
  3. Or go directly: http://localhost:3000/#admin

{Colors.OKCYAN}Admin Features:{Colors.ENDC}
  • Manage Squads (create, edit, delete, change formation)
  • Manage Players (add, edit, move between squads, delete)
  • Review Applications (accept/reject)

{Colors.HEADER}{'='*60}{Colors.ENDC}
""")

@task(default=True)
def help(c):
    """Show this help message"""
    print(f"""
{Colors.HEADER}{'='*70}{Colors.ENDC}
{Colors.BOLD}EASTLEIGH FC ACADEMY - INVOKE TASK RUNNER{Colors.ENDC}
{Colors.HEADER}{'='*70}{Colors.ENDC}

{Colors.OKCYAN}SETUP & INSTALLATION:{Colors.ENDC}
  invoke setup              Full setup (install all dependencies)
  invoke install            Install frontend npm packages
  invoke install-backend    Install backend pip packages

{Colors.OKCYAN}DOCKER COMMANDS:{Colors.ENDC}
  invoke build              Build all Docker images
  invoke start              Start all services
  invoke stop               Stop all services
  invoke down               Remove all containers
  invoke restart [service]  Restart service (backend|frontend|db)
  invoke reset              ⚠️ Full reset (DELETES ALL DATA)
  invoke logs [-f] [svc]    View logs (-f to follow, svc=service)
  invoke ps                 List containers
  invoke status             Show system status

{Colors.OKCYAN}DATABASE:{Colors.ENDC}
  invoke init               Initialize with sample data
  invoke db-shell           Open PostgreSQL CLI
  invoke backup [--file]    Backup database
  invoke restore --file X   Restore from backup

{Colors.OKCYAN}ALEMBIC MIGRATIONS:{Colors.ENDC}
  invoke alembic-init       Initialize Alembic (first time only)
  invoke alembic-revision -m "desc"   Create new migration
  invoke alembic-upgrade    Upgrade to latest (head)
  invoke alembic-downgrade  Downgrade one revision (-1)
  invoke alembic-history    Show migration history
  invoke alembic-current    Show current revision
  invoke alembic-stamp      Stamp database without migrating

{Colors.OKCYAN}DEVELOPMENT:{Colors.ENDC}
  invoke dev                Start backend + frontend (one command)
  invoke dev-frontend       Run React dev server only
  invoke dev-backend        Run Flask dev server only
  invoke stopdev            Stop dev servers

{Colors.OKCYAN}UTILITIES:{Colors.ENDC}
  invoke shell [service]    Open shell in container
  invoke clean              Clean Docker system
  invoke test               Run tests
  invoke admin              Show admin access info
  invoke help               Show this help

{Colors.OKCYAN}QUICK START:{Colors.ENDC}
  invoke setup              # First time only
  invoke build              # Build images
  invoke start              # Start services
  invoke init               # Add sample data
  # Open http://localhost:3000

{Colors.HEADER}{'='*70}{Colors.ENDC}
""")

# Aliases for common commands
@task
def up(c):
    """Alias for start"""
    start(c)

@task
def down_volumes(c):
    """Alias for reset"""
    reset(c)