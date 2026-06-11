{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        py3 = pkgs.python3;
        NetfilterQueue = pkgs.python3Packages.buildPythonPackage rec {
          pname = "NetfilterQueue";
          version = "1.1.0";
          nativeBuildInputs = [
            pkgs.python3Packages.setuptools
            pkgs.python3Packages.cython
          ];
          buildInputs = [
            pkgs.libnfnetlink
            pkgs.libnetfilter_queue
          ];
          pyproject = true;
          src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            hash = "sha256-4w7/mZMlYX9UvZWz2NM1MhTMd7XjGI+Q7DpvYoiIjXI=";
          };
        };
      in
      {
        packages.default = pkgs.python3Packages.buildPythonPackage rec {
          pname = "filter203";
          version = "0.1.0";
          nativeBuildInputs = [
            pkgs.python3Packages.setuptools
          ];
          buildInputs = with pkgs.python3Packages; [
            pkgs.python3
            numpy
            NetfilterQueue
            scapy
            bitarray
          ];
          pyproject = true;
          src = ./.;
        };
        devShells.default = pkgs.mkShell {
          buildInputs = [
            (py3.withPackages (ps: with ps; [
              numpy
              NetfilterQueue
              scapy
              bitarray
            ]))
          ];
        };
      });
}
