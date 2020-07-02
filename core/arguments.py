from sys import argv


class Arguments:
    """Command-line arguments."""

    def __init__(self):
        self.com_port: str = None
        self.config_path: str = None

        # No args were given
        if len(argv) == 1:
            print(
                "usage: jcl.exe com_port config_path\n",
                "jcl.exe: error: the following arguments are required: com_port, config_path",  # noqa
            )
            raise SystemExit(1)

        # Only one arg was given and it's not a COM port
        # Ask for the COM port while we don't have one
        if len(argv) == 2 and argv[1][:3].strip().upper() != "COM":
            while True:
                com_port = input(
                    "Please enter the COM port for the connection: "
                ).strip()

                # We got one! Record it and the file path
                if com_port and com_port.isnumeric():
                    self.com_port = com_port
                    self.config_path = argv[1]
                    break

        # All args were given
        else:
            self.com_port = argv[1]
            self.config_path = argv[2]
