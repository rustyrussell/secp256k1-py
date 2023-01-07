import glob
import os
import shutil
import subprocess
from contextlib import contextmanager
from tempfile import mkdtemp


@contextmanager
def workdir():
    cwd = os.getcwd()
    tmpdir = mkdtemp()
    os.chdir(tmpdir)
    try:
        yield
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmpdir)


@contextmanager
def redirect(stdchannel, dest_filename):
    oldstdchannel = os.dup(stdchannel.fileno())
    dest_file = open(dest_filename, "w")
    os.dup2(dest_file.fileno(), stdchannel.fileno())
    try:
        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()


def absolute(*paths):
    op = os.path
    return op.realpath(op.abspath(op.join(op.dirname(__file__), *paths)))


def build_flags(library, type_, path):
    """Return separated build flags from pkg-config output"""

    pkg_config_path = [os.path.join(path, "lib", "pkgconfig")]
    if "PKG_CONFIG_PATH" in os.environ:
        pkg_config_path.append(os.environ["PKG_CONFIG_PATH"])
    if "LIB_DIR" in os.environ:
        pkg_config_path.append(os.environ["LIB_DIR"])
        pkg_config_path.append(os.path.join(os.environ["LIB_DIR"], "pkgconfig"))

    options = [
        "--static",
        {"I": "--cflags-only-I", "L": "--libs-only-L", "l": "--libs-only-l"}[type_],
    ]

    return [
        flag.strip(f"-{type_}")
        for flag in subprocess.check_output(
            ["pkg-config"] + options + [library],
            env=dict(os.environ, PKG_CONFIG_PATH=":".join(pkg_config_path)),
        )
        .decode("UTF-8")
        .split()
    ]


def _find_lib():
    from cffi import FFI

    ffi = FFI()
    try:
        ffi.dlopen("secp256k1")
    except OSError:
        if "LIB_DIR" in os.environ:
            for path in glob.glob(os.path.join(os.environ["LIB_DIR"], "*secp256k1*")):
                try:
                    FFI().dlopen(path)
                    return True
                except OSError:
                    pass
        # We couldn't locate libsecp256k1 so we'll use the bundled one
        return False
    else:
        # If we got this far then the system library should be good enough
        return True


_has_system_lib = None


# This is currently disabled, for two reasons.
# 1. It's a bad idea to have a library which sometimes has functionality
#    and sometimes doesn't.  e.g. if you rely on Schnorr, what are you
#    supposed to do if the local Python of secp256k1 doesn't support it?
#    Complain to the user?  What are *they* supposed to do?  What's the
#    point of a package installable by pip in that case?
# 2. Until v1.0 of libsecp256k1 is released, there is no version information.
#    Since the API can change for experimental features in arbitrary ways,
#    this makes it really difficult to know that it's compatible.
def has_system_lib():
    global _has_system_lib
    if _has_system_lib is None:
        _has_system_lib = _find_lib()
    return False
