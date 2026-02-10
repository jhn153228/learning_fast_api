"""Create initial migration manually"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from alembic import command
from alembic.config import Config

# Create Alembic config
alembic_cfg = Config("alembic.ini")

# Run autogenerate
command.revision(alembic_cfg, "Initial migration", autogenerate=True)

print("Migration created successfully!")

