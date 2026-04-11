# Mot Mystère

## Algorithmes et Fonctionnalités Clés
1. **Le Système de Rating (Difficulté) :**
   * Le score d'un mot n'est pas aléatoire. Il est calculé selon la fréquence d'apparition des lettres en français (Wikipedia). Plus un mot contient de lettres rares (X, Z, W, K), plus sa note est élevée.
   * La formule prend aussi en compte le ratio lettres uniques / longueur totale pour éviter les mots trop simples.

3. **Mode Mort Subite :**
   * Une mécanique de jeu où le joueur enchaîne les mots.
   * À chaque victoire, le système filtre la liste de 22 000 mots pour proposer un mot plus difficile que le précédent.
   * Le score final est la somme cumulée des difficultés des mots trouvés.

4. **Interface Graphique :**
   * Utilisation de la bibliothèque `CustomTkinter` pour un rendu moderne.
   * Gestion dynamique de l'affichage : masquage des lettres absentes, mise à jour du classement en temps réel via un fichier CSV.


