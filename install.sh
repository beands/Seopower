#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-all}"
SRC="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
NAME="ru-seo-agent"
[ -f "$SRC/SKILL.md" ] || { echo "Source directory must contain SKILL.md: $SRC" >&2; exit 2; }
install_to(){
  base="$1"
  mkdir -p "$base"
  dest="$base/$NAME"
  [ "$dest" = "$base/$NAME" ] || { echo "Unsafe destination" >&2; exit 1; }
  rm -rf -- "$dest"
  cp -R "$SRC" "$dest"
  echo "Installed: $dest"
}
case "$TARGET" in
  hermes) install_to "$HOME/.hermes/skills";;
  openclaw) install_to "$HOME/.openclaw/skills";;
  codex) install_to "$HOME/.codex/skills";;
  claude) install_to "$HOME/.claude/skills";;
  agents) install_to "$HOME/.agents/skills";;
  all)
    install_to "$HOME/.hermes/skills"
    install_to "$HOME/.openclaw/skills"
    install_to "$HOME/.agents/skills"
    install_to "$HOME/.codex/skills"
    install_to "$HOME/.claude/skills"
    ;;
  *) echo "Usage: ./install.sh [hermes|openclaw|codex|claude|agents|all]"; exit 2;;
esac
