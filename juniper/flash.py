from serial import SerialException
from tqdm import tqdm

from core.arguments import Arguments
from core.connect import Connection
from juniper.config import Config

__all__ = ["flash_juniper"]


def flash_juniper(args: Arguments):
    # Attempt to load the specified config
    try:
        config = Config(args.config_path)
        load_result = config.load()

    # Well, unless one wasn't specified
    except IndexError:
        print("A Juniper config file was not specified.")
        input("Press the enter key to close")
        raise SystemExit(1)

    # ...Or if the file probably couldn't be loaded
    print(load_result.msg)
    if not load_result.status:
        input("Press the enter key to close")
        raise SystemExit(1)

    # We successfully loaded the config, now parse it out
    # This assumes we have a well-formed config with no errors
    parse_result = config.parse()

    # The parsing failed
    print(parse_result.msg)
    if not parse_result.status:
        input("Press the enter key to close")
        raise SystemExit(1)

    # Attempt to connect to the Juniper
    try:
        juniper = Connection(args.com_port)

    # The connection could not be established
    except SerialException:
        print(
            f"There was an issue connecting to the Juniper on COM port {args.com_port}"  # noqa
        )
        input("Press the enter key to close")
        raise SystemExit(1)

    # Log into the Juniper and go into the configuration mode
    print(f"Connected to Juniper on port {juniper.com_port}")
    juniper.send("root", 3).enter_key()
    juniper.send("cli", 1).enter_key()
    juniper.send("configure", 2).enter_key()

    # Delete the popup message that wrecks configs
    print("Removing auto-image-upgrade message")
    juniper.send("delete chassis auto-image-upgrade").enter_key()

    # Set the root password to a temporary value in order to remove the popup
    print('Setting temporary root password to "Password"')
    juniper.send("set system root-authentication plain-text-password").enter_key(wait=1)
    juniper.send("Password").enter_key(wait=1)
    juniper.send("Password").enter_key(wait=1)
    juniper.send("commit").enter_key(wait=22)

    # Now delete the existing config
    print("Deleting existing config")
    juniper.send("delete", 1).enter_key()
    juniper.send("yes", 2).enter_key()

    # Run the loaded config
    # Display a progress bar to help determine if everything is working
    print("Loading new config")
    config.config_data.append("set chassis alarm management-ethernet link-down ignore")
    for command in tqdm(config.config_data, ascii=True, leave=False):
        juniper.send(command, 0.6).enter_key()

    # Save the loaded config
    print("Saving new config")
    juniper.send("commit", 4).enter_key()

    # Reset the amber alarm once the config is loaded
    print("Reseting amber alarm light")
    juniper.exit()
    juniper.send("request system configuration rescue save").enter_key(wait=3)

    # Restart the device
    print("Restarting Juniper")
    juniper.send("request system reboot at now").enter_key(wait=1)
    juniper.send("yes").enter_key()

    # Disconnect from the device
    juniper.disconnect()
    print("Disconnected from Juniper")
