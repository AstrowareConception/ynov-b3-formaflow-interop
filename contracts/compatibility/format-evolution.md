# Règles d'évolution par format

| Changement | JSON Schema strict | Protobuf | Avro writer/reader |
|---|---|---|---|
| Ajouter un champ facultatif avec défaut | nouveau lecteur compatible ; ancien schéma strict rejette sans adaptation | ancien lecteur ignore et préserve généralement l'inconnu | compatible si le lecteur fournit un défaut |
| Supprimer un champ requis | rupture | réserver numéro et nom, ne jamais réutiliser | rupture si lecteur l'attend sans défaut |
| Renommer | rupture de propriété | nouveau numéro/champ ; ancien nom réservé | alias possible mais à tester |
| Changer le type | rupture | souvent rupture wire/semantique | dépend de la promotion autorisée, jamais supposée |

La compatibilité est une relation entre writer, reader et usage, pas une qualité absolue d'un fichier de schéma.

