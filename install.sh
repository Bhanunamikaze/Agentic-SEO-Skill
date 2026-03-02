#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/Bhanunamikaze/Agentic-SEO-Skill.git}"
SKILL_NAME="seo"
TARGET="antigravity"
PROJECT_DIR="$(pwd)"
FORCE=0
INSTALL_DEPS=0
INSTALL_PLAYWRIGHT=0
SOURCE_MODE="auto"
REPO_PATH=""
TEMP_DIR=""

usage() {
  cat <<'EOF'
SEO Skill Installer (Antigravity / Claude / Codex)

Usage:
  bash install.sh [options]

Options:
  --target <antigravity|claude|codex|global|all> Install target (default: antigravity)
  --project-dir <path>                       Project path for antigravity target (default: current directory)
  --skill-name <name>                        Installed folder name (default: seo)
  --repo-url <url>                           Source Git URL for remote mode
  --source <auto|local|remote>              Source mode (default: auto)
  --repo-path <path>                         Use a specific local repository path as source
  --install-deps                             Install Python deps (requests, beautifulsoup4)
  --install-playwright                       Also install Playwright + Chromium
  --force                                    Overwrite existing target directory
  -h, --help                                 Show help

Examples:
  # Antigravity (project-local)
  bash install.sh --target antigravity --project-dir /path/to/project

  # Claude
  bash install.sh --target claude

  # Codex only
  bash install.sh --target codex

  # Global install (Claude + Codex)
  bash install.sh --target global

  # Install from a local checkout path
  bash install.sh --target antigravity --project-dir /path/to/project --repo-path /path/to/Agentic-SEO-Skill

  # Install from a custom remote repository URL
  bash install.sh --target codex --source remote --repo-url https://github.com/you/Agentic-SEO-Skill.git

  # All targets
  bash install.sh --target all --project-dir /path/to/project

  # Pipe install from GitHub
  curl -fsSL https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh | \
    bash -s -- --target codex
EOF
}

cleanup() {
  if [[ -n "${TEMP_DIR}" && -d "${TEMP_DIR}" ]]; then
    rm -rf "${TEMP_DIR}"
  fi
}
trap cleanup EXIT

require_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: required command not found: ${cmd}" >&2
    exit 1
  fi
}

resolve_dir() {
  local dir="$1"
  if [[ ! -d "${dir}" ]]; then
    echo "Error: directory not found: ${dir}" >&2
    exit 1
  fi
  (
    cd "${dir}"
    pwd
  )
}

copy_skill() {
  local src="$1"
  local dest="$2"
  local label="$3"

  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    echo "Error: ${label} target already exists: ${dest}" >&2
    echo "Use --force to overwrite." >&2
    exit 1
  fi

  mkdir -p "$(dirname "${dest}")"
  if [[ -e "${dest}" ]]; then
    rm -rf "${dest}"
  fi
  mkdir -p "${dest}"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a \
      --exclude ".git/" \
      --exclude ".github/" \
      --exclude "__pycache__/" \
      --exclude "*.pyc" \
      --exclude "smoke-screenshots-hackingdream/" \
      --exclude "seo-report-*.html" \
      "${src}/" "${dest}/"
  else
    (
      cd "${src}"
      tar \
        --exclude=".git" \
        --exclude=".github" \
        --exclude="__pycache__" \
        --exclude="*.pyc" \
        --exclude="smoke-screenshots-hackingdream" \
        --exclude="seo-report-*.html" \
        -cf - .
    ) | (
      cd "${dest}"
      tar -xf -
    )
  fi

  echo "✓ Installed for ${label}: ${dest}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --project-dir)
      PROJECT_DIR="${2:-}"
      shift 2
      ;;
    --skill-name)
      SKILL_NAME="${2:-}"
      shift 2
      ;;
    --repo-url)
      REPO_URL="${2:-}"
      shift 2
      ;;
    --source)
      SOURCE_MODE="${2:-}"
      shift 2
      ;;
    --repo-path)
      REPO_PATH="${2:-}"
      shift 2
      ;;
    --install-deps)
      INSTALL_DEPS=1
      shift
      ;;
    --install-playwright)
      INSTALL_PLAYWRIGHT=1
      INSTALL_DEPS=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ "${TARGET}" != "antigravity" && "${TARGET}" != "claude" && "${TARGET}" != "codex" && "${TARGET}" != "global" && "${TARGET}" != "all" ]]; then
  echo "Error: invalid --target: ${TARGET}" >&2
  exit 1
fi
if [[ "${SOURCE_MODE}" != "auto" && "${SOURCE_MODE}" != "local" && "${SOURCE_MODE}" != "remote" ]]; then
  echo "Error: invalid --source: ${SOURCE_MODE}" >&2
  exit 1
fi

require_cmd bash
require_cmd python3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR=""
SHOULD_CLONE=0

if [[ -n "${REPO_PATH}" ]]; then
  SRC_DIR="$(resolve_dir "${REPO_PATH}")"
  echo "Using repo path source: ${SRC_DIR}"
elif [[ "${SOURCE_MODE}" == "local" ]]; then
  SRC_DIR="${SCRIPT_DIR}"
  echo "Using local source: ${SRC_DIR}"
elif [[ "${SOURCE_MODE}" == "remote" ]]; then
  SHOULD_CLONE=1
elif [[ -f "${SCRIPT_DIR}/SKILL.md" ]]; then
  SRC_DIR="${SCRIPT_DIR}"
  echo "Using local source: ${SRC_DIR}"
else
  SHOULD_CLONE=1
fi

if [[ "${SHOULD_CLONE}" -eq 1 ]]; then
  require_cmd git
  TEMP_DIR="$(mktemp -d)"
  echo "Cloning source repo: ${REPO_URL}"
  if ! git clone --depth 1 "${REPO_URL}" "${TEMP_DIR}/repo" >/dev/null 2>&1; then
    echo "Error: failed to clone source repo: ${REPO_URL}" >&2
    echo "Tip: pass --repo-url <git-url> or set REPO_URL for remote installs." >&2
    exit 1
  fi
  SRC_DIR="${TEMP_DIR}/repo"
  echo "Using remote source: ${SRC_DIR}"
fi

if [[ ! -f "${SRC_DIR}/SKILL.md" ]]; then
  echo "Error: SKILL.md not found in source directory: ${SRC_DIR}" >&2
  exit 1
fi

echo ""
echo "Installing SEO Skill"
echo "Target: ${TARGET}"
echo "Skill name: ${SKILL_NAME}"
echo ""

if [[ "${TARGET}" == "antigravity" || "${TARGET}" == "all" ]]; then
  AG_DIR="${PROJECT_DIR}/.agent/skills/${SKILL_NAME}"
  copy_skill "${SRC_DIR}" "${AG_DIR}" "antigravity"
fi

if [[ "${TARGET}" == "claude" || "${TARGET}" == "global" || "${TARGET}" == "all" ]]; then
  CLAUDE_DIR="${HOME}/.claude/skills/${SKILL_NAME}"
  copy_skill "${SRC_DIR}" "${CLAUDE_DIR}" "claude"
fi

if [[ "${TARGET}" == "codex" || "${TARGET}" == "global" || "${TARGET}" == "all" ]]; then
  CODEX_ROOT="${CODEX_HOME:-${HOME}/.codex}"
  CODEX_DIR="${CODEX_ROOT}/skills/${SKILL_NAME}"
  copy_skill "${SRC_DIR}" "${CODEX_DIR}" "codex"
fi

if [[ "${INSTALL_DEPS}" -eq 1 ]]; then
  echo ""
  echo "Installing Python dependencies..."
  if python3 -m pip install --user requests beautifulsoup4; then
    echo "✓ Installed requests + beautifulsoup4"
  else
    echo "⚠ Could not auto-install Python dependencies. Install manually:"
    echo "  python3 -m pip install --user requests beautifulsoup4"
  fi

  if [[ "${INSTALL_PLAYWRIGHT}" -eq 1 ]]; then
    if python3 -m pip install --user playwright && python3 -m playwright install chromium; then
      echo "✓ Installed Playwright + Chromium"
    else
      echo "⚠ Could not auto-install Playwright. Install manually:"
      echo "  python3 -m pip install --user playwright && python3 -m playwright install chromium"
    fi
  fi
fi

echo ""
echo "Install complete."
echo "Next: restart your tool session to pick up the installed skill."
