{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.setuptools
    pkgs.python39Packages.wheel
    pkgs.python39Packages.requests
    pkgs.python39Packages.pandas
    pkgs.python39Packages.numpy
    pkgs.python39Packages.pytz
    pkgs.python39Packages.python-dateutil
    pkgs.python39Packages.solana
    pkgs.python39Packages.base58
    pkgs.git
    pkgs.wget
    pkgs.curl
  ];
}