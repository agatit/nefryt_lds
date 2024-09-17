def pytest_addoption(parser):
    parser.addoption(
        "--db",
        action="store",
        default="temp",
        help="Type of database to use. Options are: 'temp' (temporary), 'tc' (testcontainers). Default is 'temp'."
    )


def pytest_configure(config):
    db_type = config.getoption("db")
    if db_type not in ["temp", "tc"]:
        raise ValueError(f"Unsupported database type: {db_type}")
    config.db_type = db_type
