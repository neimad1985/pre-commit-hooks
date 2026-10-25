# pre-commit-hooks

Hooks pre-commit partagés : ils alignent chaque projet sur la même configuration.

## Ajouter les hooks à un projet

```bash
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/neimad1985/pre-commit-hooks
    rev: 0.6.0
    hooks:
      - id: sync-pre-commit-config
EOF
prek install
prek run --all-files
```
## Hooks

| Hook | Effet |
| --- | --- |
| `sync-pre-commit-config` | Réécrit `.pre-commit-config.yaml` d'après [la référence](reference/pre-commit-config.yaml) du dernier tag. |
| `check-gitignore` | Vérifie le contenu de `.gitignore`. |
| `check-transcrypt` | Ajoute la ligne `secrets.*` à `.gitattributes` et initialise transcrypt au besoin. |
| `sync-ruff-config` | Réécrit `ruff.toml` d'après [la référence](src/pre_commit_hooks/sync_ruff_config/ruff.toml), si le projet a un `pyproject.toml`. |

## Publier une version

Pousser un tag semver sans `v`, par exemple `0.7.0`. Chaque projet passe sur ce tag à son commit suivant.

## Développement

```bash
uv sync
uv run pytest
```

Ce dépôt applique ses propres hooks, avec une différence. Dans un projet, la config pointe vers ce dépôt sur GitHub, à un
tag : pre-commit lance la dernière version publiée. Ici, ce serait l'ancienne version des hooks, pas le code en cours
de modification.

`sync-pre-commit-config` reconnaît donc ce dépôt grâce à [.pre-commit-hooks.yaml](.pre-commit-hooks.yaml). Il lit la
référence dans le répertoire de travail, et non au dernier tag. Il remplace le bloc GitHub par un bloc `repo: local`,
qui lance chaque hook par `uv run`. Les autres blocs, comme ruff, restent tels quels.
