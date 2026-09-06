# Mise à jour des images Docker

Les références canoniques sont dans `image-lock.yml`, `Dockerfile` et `compose.yml`. Pour mettre à jour : choisir un tag précis, résoudre le digest de manifeste avec `docker buildx imagetools inspect <tag>`, reporter le même couple tag/digest dans les trois fichiers concernés, puis exécuter `docker compose -p formaflow-interop config`, `python scripts/tasks.py smoke` et l'audit d'image disponible localement. Un digest n'est jamais remplacé silencieusement par `latest`.

