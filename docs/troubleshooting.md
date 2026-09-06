# Dépannage

- Vérifier `py -3.12 --version` sous Windows ou `python --version` ailleurs.
- Si le port 8000 est occupé, arrêter uniquement le processus local concerné.
- Pour RabbitMQ, consulter `docker compose -p formaflow-interop ps` et les logs ciblés.
- Nettoyer uniquement ce projet avec `docker compose -p formaflow-interop down --volumes --remove-orphans`.
- Ne jamais employer un nettoyage Docker global pour ce module.

