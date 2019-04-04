
import re
import sys
import subprocess

from packaging.version import Version, InvalidVersion


def _capture_versions(package_name, test_database=False):
    command = [sys.executable, "-m", "pip", "install", "{}==".format(package_name)]
    if test_database:
        command.append("--index-url")
        command.append("https://test.pypi.org/simple/")

    resp = subprocess.run(command, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT).stdout

    captured_versions = []
    for potential_version in resp.split():
        front_stripped_potential_version = re.sub(r"^[\D]*", "", potential_version.decode("utf-8"))
        striped_potential_version = re.sub(r"[\D]*$", "", front_stripped_potential_version)
        try:
            version = Version(striped_potential_version)
            captured_versions.append(version)
        except InvalidVersion:
            continue

    return captured_versions


def _max_version(versions):
    return max(versions)


def get_latest_version(package_name, test_database=False):
    """
    Retrieve the latest version of the given package name from PyPi.  Return a version of 0.0.0
    if no package version information is found.
    :param package_name: A string specifying the package name to interrogate.
    :param test_database: A boolean to signal whether to use the test.pypi.org database, default is False.
    :return: A packaging version Version of the latest version found, version 0.0.0 otherwise.
    """
    latest_version = Version("0.0.0")
    captured_versions = _capture_versions(package_name, test_database)
    if captured_versions:
        latest_version = _max_version(captured_versions)

    return latest_version


def bump_dev_version(version):
    """
    Bump the dev version of the given version.
    :param version: The packaging version Version to bump.
    :return: The bumped packaging version Version.
    """
    if version.dev is None:
        bumped_version = Version(version.public + ".dev0")
    else:
        bumped_version = Version(version.public.replace("dev{}".format(version.dev), "dev{}".format(version.dev + 1)))

    return bumped_version


POSITIVE_VALUES = ['True', 'TRUE', 'true', '1']


def main():
    """
    Print out the next available dev version from PyPi database.  The test database will be
    queried unless a 2nd argument is passed which evaluates to not True.
    :return: 0 on success, -1 otherwise.
    """
    args = sys.argv[:]
    args.pop(0)
    if len(args) > 0:
        package_name = args.pop(0)
        test_database = True
        if len(args) > 0:
            test_database = True if args.pop(0) in POSITIVE_VALUES else False

        latest_version = get_latest_version(package_name, test_database)
        next_dev_version = bump_dev_version(latest_version)
        print("{}".format(next_dev_version))

    else:
        sys.exit(-1)

    sys.exit(0)


if __name__ == "__main__":
    main()
