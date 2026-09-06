# Plan de migration V1 vers V2

1. Cartographier les producteurs, lecteurs et hypothèses par format.
2. Publier contrats V2, défauts et adaptateurs sans retirer V1.
3. Exécuter la matrice automatisée et le scénario d'incident.
4. Activer `/api/v2` pour un client synthétique pilote.
5. Mesurer les appels V1 et erreurs de downcast avec correlation ID.
6. Migrer chaque consommateur, avec retour possible à V1.
7. Appliquer le Sunset annoncé seulement lorsque l'inventaire ne montre plus de client V1.

