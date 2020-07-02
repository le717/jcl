from datetime import datetime
from os import environ

from core.arguments import Arguments
from juniper.flash import flash_juniper

__all__ = ["main"]


def main():
    # Get the command-line arguments
    args = Arguments()

    # Get the current time, for metric purposes
    start_time = datetime.now()

    # Start the flashing process
    flash_juniper(args)

    # Calculate how long it took to load the config
    end_time = datetime.now()
    print(f"Config loaded in {end_time - start_time}")

    # Only make the script require a closing prompt when we're not in dev
    if "IS_DEV_RUN" not in environ:
        input("Press enter to close.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
