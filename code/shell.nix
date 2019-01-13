# to activate run
# nix-shell
with import <nixpkgs> {};

# (python36.withPackages (ps: with ps; [ jupyter numpy nltk pandas ])).env
(python36.withPackages (ps: [ps.pip ps.virtualenv ps.jupyter ps.pandas])).env
