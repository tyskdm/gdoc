import logging


def add_arguments(parser):
    """
    Setup logging arguments
    """
    for key, value in {
        "filename": {
            "help": "Specifies that a FileHandler be created, using "
            + "the specified filename.",
        },
        "filemode": {
            "help": "If filename is specified, open the file in this mode. "
            + "Defaults to 'a'.",
            "choices": ["a", "w"],
        },
        "level": {
            "help": "Set the root logger level to the specified level.",
            "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        },
        "scope": {
            "help": "Module paths for logger output.",
            "nargs": "*",
        },
        "timestamp": {
            "help": "Add a time stamp to each record.",
            "action": "store_true",
        },
    }.items():
        parser.add_argument("--logging-" + key, **value)


def basic_config(args, stream=None):
    """
    Setup logging
    """
    logging_level: int | None = None
    if hasattr(args, "logging_level"):
        logging_level = getattr(args, "logging_level")

    if hasattr(args, "logging_scope") and (
        (val := getattr(args, "logging_scope")) is not None
    ):
        #
        # scope is specified
        #
        logging.basicConfig(handlers=[logging.NullHandler()])

        kwargs: dict | None = None
        if hasattr(args, "logging_filename") and (
            (filename := getattr(args, "logging_filename")) is not None
        ):
            kwargs = {"filename": filename}
            if hasattr(args, "logging_filemode") and (
                (mode := getattr(args, "logging_filemode")) is not None
            ):
                kwargs["mode"] = mode

        scope: list[str] = val
        for module in scope:
            if "/" in module:
                module = module.removesuffix(".py")
                module = ".".join(module.split("/"))

            if logging_level is not None:
                logging.getLogger(module).setLevel(level=logging_level)

            if kwargs is not None:
                handler = logging.FileHandler(**kwargs)
            else:
                handler = logging.StreamHandler(stream)

            if getattr(args, "logging_timestamp"):
                handler.setFormatter(
                    logging.Formatter(
                        fmt="%(asctime)s %(levelname)s:%(name)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                    )
                )
            else:
                handler.setFormatter(
                    logging.Formatter(
                        fmt="%(levelname)s:%(name)s:%(message)s",
                    )
                )
            logging.getLogger(module).addHandler(handler)

    else:
        #
        # scope is not specified
        #
        kwargs = {}

        if logging_level is not None:
            kwargs["level"] = logging_level

        if hasattr(args, "logging_filename") and (
            (filename := getattr(args, "logging_filename")) is not None
        ):
            kwargs["filename"] = filename
            if hasattr(args, "logging_filemode") and (
                (mode := getattr(args, "logging_filemode")) is not None
            ):
                kwargs["filemode"] = mode
        elif stream is not None:
            kwargs["stream"] = stream

        if getattr(args, "logging_timestamp"):
            kwargs["format"] = "%(asctime)s %(levelname)s:%(name)s:%(message)s"
            kwargs["datefmt"] = "%Y-%m-%d %H:%M:%S"

        logging.basicConfig(**kwargs)
