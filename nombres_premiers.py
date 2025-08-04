# -*- coding: utf-8 -*-

"""
Ce script trouve et affiche un nombre `t` de nombres premiers à partir d'un nombre de départ `start`.
Il utilise un algorithme de crible d'Ératosthène segmenté pour une recherche efficace sur de grands intervalles.
"""

from rich import print
import math

def petits_nombres_premiers(n):
    """
    Génère une liste de nombres premiers jusqu'à la racine carrée de `n` en utilisant un crible d'Ératosthène classique.

    Ces "petits" nombres premiers sont ensuite utilisés pour cribler les segments plus grands.

    Args:
        n (int): La limite supérieure pour la recherche initiale des nombres premiers.

    Returns:
        list[int]: Une liste des nombres premiers jusqu'à √n.
    """
    limite = int(math.isqrt(n)) + 1
    crible = [True] * (limite + 1)

    # 0 et 1 ne sont pas des nombres premiers
    if limite > 0: crible[0] = False
    if limite > 1: crible[1] = False

    for i in range(2, int(limite ** 0.5) + 1):
        if crible[i]:
            # Marquer tous les multiples de i comme non premiers
            for j in range(i * i, limite + 1, i):
                crible[j] = False

    return [i for i, est_premier in enumerate(crible) if est_premier]

def crible_segmenté(start, end, petits_premiers):
    """
    Applique le crible d'Ératosthène sur un segment (ou "fenêtre") de nombres de `start` à `end`.

    Args:
        start (int): Le début de l'intervalle.
        end (int): La fin de l'intervalle.
        petits_premiers (list[int]): La liste des nombres premiers à utiliser pour le criblage.

    Returns:
        list[int]: Une liste des nombres premiers trouvés dans l'intervalle [start, end].
    """
    size = end - start + 1
    # On suppose au départ que tous les nombres du segment sont premiers
    is_prime = [True] * size

    for p in petits_premiers:
        # Trouver le premier multiple de p qui est >= start
        # C'est le point de départ pour le criblage dans ce segment
        debut = max(p * p, ((start + p - 1) // p) * p)

        for j in range(debut, end + 1, p):
            is_prime[j - start] = False

    # Cas spécial : si le segment commence à 1, il faut le marquer comme non premier
    if start == 1:
        is_prime[0] = False

    return [start + i for i, val in enumerate(is_prime) if val]

def t_premiers_nombres(start, t):
    """
    Trouve et affiche les `t` premiers nombres premiers à partir de `start`.
    La recherche s'effectue par segments de taille croissante pour optimiser les performances.

    Args:
        start (int): Le nombre à partir duquel commencer la recherche.
        t (int): Le nombre de nombres premiers à trouver.
    """
    if t <= 0:
        print("[bold red]Erreur :[/bold red] t doit être un entier positif.")
        return
    if start < 2:
        start = 2

    nombres_premiers = []
    increment = 1000  # Taille initiale de la fenêtre de recherche

    # On continue tant qu'on n'a pas trouvé assez de nombres premiers
    while len(nombres_premiers) < t:
        end = start + increment

        # 1. Obtenir les petits premiers nécessaires pour cribler jusqu'à `end`
        petits = petits_nombres_premiers(end)

        # 2. Cribler le segment actuel
        segment = crible_segmenté(start, end, petits)
        nombres_premiers.extend(segment)

        # 3. Préparer le prochain segment
        start = end + 1
        increment *= 2  # On double la taille de la fenêtre pour être plus efficace sur les grands nombres

    # Affichage des résultats
    print(f"[bold green]Les {t} premiers nombres premiers trouvés sont :[/bold green]")
    for i, n in enumerate(nombres_premiers[:t], 1):
        tag = ""
        if i == 1: tag = "(premier trouvé)"
        if i == t: tag = "(dernier trouvé)"
        print(f"{i}. {n} {tag}")

# ----- Point d'entrée du script -----
if __name__ == "__main__":
    try:
        start_input = int(input("Entrez le nombre de départ : "))
        t_input = int(input("Entrez le nombre de nombres premiers à afficher : "))
        t_premiers_nombres(start_input, t_input)
    except ValueError:
        print("[bold red]Erreur :[/bold red] veuillez entrer des entiers valides.")
    except KeyboardInterrupt:
        print("\n[bold yellow]Programme interrompu par l'utilisateur.[/bold yellow]")
