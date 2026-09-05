# Objectifs et périmètre

## Couverture obligatoire

Le repository couvre intégralement les quatre axes du syllabus :

1. échanger en JSON, Protocol Buffers et Avro et comparer leurs performances ;
2. définir et gouverner un JSON Schema comme data contract ;
3. implémenter un pattern asynchrone avec un broker ;
4. versionner une API par URL ou en-tête en maintenant la rétrocompatibilité.

Il mobilise également REST, JSON/CSV, Python, Git, tests automatisés et documentation technique.

## Ce que le module ne cherche pas à faire

- concevoir de nouveaux bounded contexts ; ceux-ci sont fournis en entrée ;
- enseigner NestJS ou une architecture microservices complète ;
- construire une plateforme de streaming de production ;
- démontrer un « exactly once » de bout en bout ;
- installer Redis en plus de RabbitMQ ;
- choisir un format universellement supérieur ;
- transformer les productions formatives en évaluation cachée.

## Principes de réussite

- le sens métier reconstruit est identique dans les trois formats ;
- chaque contrat possède identité, version, propriétaire, exemples et tests ;
- les mesures sont reproductibles et leurs limites sont écrites ;
- un doublon ou un message invalide produit un comportement déterministe ;
- une évolution compatible est prouvée par un ancien client et une matrice ;
- les décisions séparent faits observés, hypothèses et préférences.
