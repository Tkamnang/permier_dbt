# -*- coding: utf-8 -*-

"""
Ce script résout un problème de transport classique (optimisation linéaire).
On cherche à minimiser le coût de transport entre des sources (usines) et des destinations (entrepôts).
"""

import numpy as np
from scipy.optimize import linprog
from rich.console import Console
from rich.table import Table

console = Console()

def resoudre_transport(costs, supply, demand):
    """
    Résout le problème de transport en utilisant la programmation linéaire.

    Args:
        costs (np.ndarray): Matrice des coûts C[i][j].
        supply (list): Liste des capacités des sources.
        demand (list): Liste des besoins des destinations.
    """
    num_sources = len(supply)
    num_dest = len(demand)

    # Le vecteur c à minimiser est la matrice des coûts aplatie
    c = costs.flatten()

    # Contraintes d'offre (Supply constraints) : somme par ligne <= supply
    # Pour chaque source i : sum_j x_ij <= supply[i]
    A_ub = []
    b_ub = []
    for i in range(num_sources):
        constraint = np.zeros(num_sources * num_dest)
        for j in range(num_dest):
            constraint[i * num_dest + j] = 1
        A_ub.append(constraint)
        b_ub.append(supply[i])

    # Contraintes de demande (Demand constraints) : somme par colonne == demand
    # Pour chaque destination j : sum_i x_ij == demand[j]
    A_eq = []
    b_eq = []
    for j in range(num_dest):
        constraint = np.zeros(num_sources * num_dest)
        for i in range(num_sources):
            constraint[i * num_dest + j] = 1
        A_eq.append(constraint)
        b_eq.append(demand[j])

    # Résolution
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')

    if res.success:
        # Remodeler le résultat en matrice x_ij
        plan = res.x.reshape((num_sources, num_dest))
        return plan, res.fun
    else:
        return None, None

def main():
    # Données du problème
    sources = ["Usine A", "Usine B"]
    destinations = ["Entrepôt 1", "Entrepôt 2", "Entrepôt 3"]

    # Coût de transport unitaire
    costs = np.array([
        [8, 6, 10],
        [9, 12, 13]
    ])

    supply = [20, 30]
    demand = [10, 15, 25]

    console.print("[bold blue]Problème du Transport[/bold blue]")
    console.print(f"Offre totale : {sum(supply)}")
    console.print(f"Demande totale : {sum(demand)}\n")

    plan, cout_total = resoudre_transport(costs, supply, demand)

    if plan is not None:
        table = Table(title="Plan de Transport Optimal")
        table.add_column("Source / Destination", style="cyan")
        for d in destinations:
            table.add_column(d, justify="right")

        for i, s_name in enumerate(sources):
            row = [s_name] + [f"{val:.0f}" for val in plan[i]]
            table.add_row(*row)

        console.print(table)
        console.print(f"\n[bold green]Coût total minimal : {cout_total:.2f}[/bold green]")
    else:
        console.print("[bold red]Erreur : Impossible de trouver une solution optimale.[/bold red]")

if __name__ == "__main__":
    main()
