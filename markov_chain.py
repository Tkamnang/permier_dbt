# -*- coding: utf-8 -*-

"""
Ce script simule une chaîne de Markov simple pour modéliser l'évolution d'un système.
Exemple : Modèle météorologique (Beau, Nuageux, Pluie).
"""

import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()

def simuler_markov(transition_matrix, initial_state, steps):
    """
    Simule l'évolution d'un vecteur d'état à travers une chaîne de Markov.

    Args:
        transition_matrix (np.ndarray): Matrice de transition (stochastique par ligne).
        initial_state (np.ndarray): Vecteur d'état initial.
        steps (int): Nombre d'étapes de simulation.

    Returns:
        list[np.ndarray]: Historique des états.
    """
    history = [initial_state]
    current_state = initial_state

    for _ in range(steps):
        current_state = np.dot(current_state, transition_matrix)
        history.append(current_state)

    return history

def trouver_etat_stationnaire(transition_matrix):
    """
    Trouve la distribution stationnaire de la chaîne de Markov.
    Résout pi * P = pi  => pi * (P - I) = 0.
    """
    # On cherche le vecteur propre à gauche associé à la valeur propre 1
    eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

    # Trouver l'indice de la valeur propre la plus proche de 1
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    stationary = np.real(eigenvectors[:, idx])

    # Normaliser pour que la somme soit égale à 1
    stationary = stationary / np.sum(stationary)
    return stationary

def main():
    # Définition des états
    etats = ["Beau", "Nuageux", "Pluie"]

    # Matrice de transition
    # P[i][j] est la probabilité de passer de l'état i à l'état j
    P = np.array([
        [0.7, 0.2, 0.1],  # Si Beau : 70% Beau, 20% Nuageux, 10% Pluie
        [0.3, 0.4, 0.3],  # Si Nuageux : 30% Beau, 40% Nuageux, 30% Pluie
        [0.2, 0.3, 0.5]   # Si Pluie : 20% Beau, 30% Nuageux, 50% Pluie
    ])

    # État initial (il fait Beau à 100%)
    v0 = np.array([1.0, 0.0, 0.0])

    steps = 10
    historique = simuler_markov(P, v0, steps)

    # Affichage du tableau d'évolution
    table = Table(title=f"Évolution de la Chaîne de Markov ({steps} étapes)")
    table.add_column("Étape", justify="right", style="cyan")
    for etat in etats:
        table.add_column(etat, justify="center")

    for i, etat_v in enumerate(historique):
        row = [str(i)] + [f"{p:.4f}" for p in etat_v]
        table.add_row(*row)

    console.print(table)

    # Calcul de l'état stationnaire
    stationnaire = trouver_etat_stationnaire(P)
    console.print("\n[bold green]Distribution stationnaire (Convergence) :[/bold green]")
    for etat, prob in zip(etats, stationnaire):
        console.print(f" - {etat}: {prob:.4f}")

if __name__ == "__main__":
    main()
