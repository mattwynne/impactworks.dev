{ pkgs, ... }:

{
  packages = with pkgs; [
    hugo
    nodejs_22
  ];

  languages.javascript = {
    enable = true;
    package = pkgs.nodejs_22;
  };

  scripts.dev.exec = ''
    hugo server --bind 127.0.0.1
  '';

  scripts.build.exec = ''
    hugo --minify
  '';

  scripts.check.exec = ''
    hugo --minify
    python3 scripts/check_site.py
  '';

  enterShell = ''
    echo "Impact Works website"
    echo "Commands: dev, build, check"
    hugo version
  '';
}
