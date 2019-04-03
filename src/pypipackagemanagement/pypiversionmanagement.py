
import re
import sys
import subprocess

from packaging.version import Version, InvalidVersion


def _capture_versions(package_name):
    resp = subprocess.run([sys.executable, "-m", "pip", "install", "{}==".format(package_name)], stdout=subprocess.PIPE,
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


def get_latest_version(package_name):
    """
    Retrieve the latest version of the given package name from PyPi.  Return a version of 0.0.0
    if no package version information is found.
    :param package_name: A string specifying the package name to interrogate.
    :return: A packaging version Version of the latest version found, version 0.0.0 otherwise.
    """
    latest_version = Version("0.0.0")
    captured_versions = _capture_versions(package_name)
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
