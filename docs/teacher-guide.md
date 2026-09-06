# Guide formateur

## Préparation

Vérifier Python 3.12, Docker/Compose, digests de `image-lock.yml`, `python scripts/tasks.py quality`, puis `smoke`. Tester chaque tag avec la commande indiquée dans son annotation. Précharger les images si le réseau de salle est limité ; conserver le parcours natif pour contrats et le parcours Docker pour RabbitMQ.

## Déroulé conseillé

Séance 1 : faire comparer les messages ambigus avant de montrer le mapping ; débriefer propriété, unités et erreurs. Séance 2 : faire prédire tailles/temps, puis confronter aux mesures sans classement universel. Séance 3 : injecter doublon, fermeture avant ack, `x-fail-until` et poison ; observer files et correlation ID. Séance 4 : faire jouer ancien client et writer/reader, puis construire migration et incident avant le temps individuel formatif de 30 minutes.

## Replis

Sans Docker, exécuter tests unitaires/contrats/compatibilité et utiliser les diagrammes/résultats bruts fournis. Sans Node, les SVG sont déjà versionnés et leur empreinte reste vérifiable. Sans GNU Make, utiliser les scripts Python ou PowerShell. Aucun service cloud n'est un repli autorisé ou nécessaire.

## Débrief et correction collective

Demander à chaque groupe de distinguer fait, hypothèse, décision et preuve. Comparer chemins d'erreur, relations writer/reader, position de l'ack, borne de retry et stratégie de rollback. Les checkpoints servent de référence collective progressive ; ils ne constituent pas un corrigé d'évaluation.

## Réinitialisation

Entre groupes, exécuter `python scripts/tasks.py reset-data`, puis vérifier les ressources portant le label Compose `formaflow-interop`. Ne jamais utiliser de prune global. Les fixtures versionnées ne sont pas modifiées par la réinitialisation.

## Statut pédagogique

Toutes les productions et preuves sont formatives, sans note. Le dépôt ne contient aucun contenu de questionnaire, résultat individuel ou mécanisme de notation. Le handoff Agilité transmet un problème exploitable, pas un backlog déjà résolu.

