# Frontières et ownership

Gestion des inscriptions possède `Enrollment`, ses transitions, la décision de remboursement et les domain events locaux. Catalogue et planification est upstream pour session/dates/capacité/état. Commande et facturation est upstream pour confirmation et prix accepté. Notification et Projections sont downstream.

Cette context map n'impose aucun microservice. Les hypothèses de consommateurs devront être confirmées pendant le module Interopérabilité.
