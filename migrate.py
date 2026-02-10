"""Database migration helper script"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from alembic import command
from alembic.config import Config


def main():
    """Run database migrations."""
    alembic_cfg = Config("alembic.ini")

    print("=" * 60)
    print("Database Migration Tool")
    print("=" * 60)
    print()

    # Show current version
    print("Current migration status:")
    try:
        command.current(alembic_cfg, verbose=True)
    except Exception as e:
        print(f"  No migrations applied yet or database not initialized")
    print()

    # Show available migrations
    print("Available migrations:")
    command.history(alembic_cfg, verbose=False)
    print()

    # Prompt user
    print("What would you like to do?")
    print("1. Upgrade to latest (alembic upgrade head)")
    print("2. Downgrade one version (alembic downgrade -1)")
    print("3. Show SQL only (alembic upgrade head --sql)")
    print("4. Reset to base (alembic downgrade base)")
    print("5. Exit")
    print()

    choice = input("Enter your choice (1-5): ").strip()
    print()

    try:
        if choice == "1":
            print("Upgrading to latest version...")
            command.upgrade(alembic_cfg, "head")
            print("✅ Migration completed successfully!")

        elif choice == "2":
            print("Downgrading one version...")
            command.downgrade(alembic_cfg, "-1")
            print("✅ Downgrade completed successfully!")

        elif choice == "3":
            print("Showing SQL for upgrade to head:")
            print("-" * 60)
            command.upgrade(alembic_cfg, "head", sql=True)
            print("-" * 60)

        elif choice == "4":
            confirm = input("⚠️  This will reset all migrations. Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                print("Resetting to base...")
                command.downgrade(alembic_cfg, "base")
                print("✅ Reset completed successfully!")
            else:
                print("❌ Operation cancelled")

        elif choice == "5":
            print("Exiting...")
            return

        else:
            print("❌ Invalid choice")
            return

        # Show current version after operation
        print()
        print("Current migration status:")
        command.current(alembic_cfg, verbose=True)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

