from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algorithms.problems_csp import DroneAssignmentCSP


def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Basic backtracking search without optimizations.

    Tips:
    - An assignment is a dictionary mapping variables to values (e.g. {X1: Cell(1,2), X2: Cell(3,4)}).
    - Use csp.assign(var, value, assignment) to assign a value to a variable.
    - Use csp.unassign(var, assignment) to unassign a variable.
    - Use csp.is_consistent(var, value, assignment) to check if an assignment is consistent with the constraints.
    - Use csp.is_complete(assignment) to check if the assignment is complete (all variables assigned).
    - Use csp.get_unassigned_variables(assignment) to get a list of unassigned variables.
    - Use csp.domains[var] to get the list of possible values for a variable.
    - Use csp.get_neighbors(var) to get the list of variables that share a constraint with var.
    - Add logs to measure how good your implementation is (e.g. number of assignments, backtracks).

    You can find inspiration in the textbook's pseudocode:
    Artificial Intelligence: A Modern Approach (4th Edition) by Russell and Norvig, Chapter 5: Constraint Satisfaction Problems
    
    1ERA VERSION: 
def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:    
    stats = {"assignments": 0, "backtracks": 0}

    def backtrack(cs: dict[str, str]) -> dict[str, str] | None:
      v = unassigned[0]
      for value in csp.domains[v]:
          stats["assignments"] += 1

          if csp.is_consistent(v, value, cs):

              csp.assign(v, value, cs)
              result = backtrack(cs)

              if result is not None:
                  return result

              csp.unassign(v, cs)
              stats["backtracks"] += 1

      return None

    cs: dict[str, str] = {}
    result = backtrack(cs)

    return result
    
    Prompt:Corrige y completa el siguiente algoritmo de backtracking para que funcione correctamente para un CSP de asignación de drones. 
    Debe seguir la lógica estándar de backtracking y usar correctamente los métodos del objeto DroneAssignmentCSP. 
    Mantén la estructura general del código, la función backtracking_search, la función interna backtrack y el diccionario de stats. 
    Solo corrige errores, agrega lo que falta y haz que el algoritmo sea funcional y coherente.
    """
    stats = {"assignments": 0, "backtracks": 0}

    def backtrack(cs: dict[str, str]) -> dict[str, str] | None:

      if csp.is_complete(cs):
          return cs

      unassigned = csp.get_unassigned_variables(cs)
      v = unassigned[0]

      for value in csp.domains[v]:
          stats["assignments"] += 1

          if csp.is_consistent(v, value, cs):

              csp.assign(v, value, cs)
              result = backtrack(cs)

              if result is not None:
                  return result

              csp.unassign(v, cs)
              stats["backtracks"] += 1

      return None

    cs: dict[str, str] = {}
    result = backtrack(cs)

    print(f"[backtracking] Asignaciones intentadas: {stats['assignments']}")
    print(f"[backtracking] Backtracks realizados:   {stats['backtracks']}")

    return result

def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with Forward Checking.

    Tips:
    - Forward checking: After assigning a value to a variable, eliminate inconsistent values from
      the domains of unassigned neighbors. If any neighbor's domain becomes empty, backtrack immediately.
    - Save domains before forward checking so you can restore them on backtrack.
    - Use csp.get_neighbors(var) to get variables that share constraints with var.
    - Use csp.is_consistent(neighbor, val, assignment) to check if a value is still consistent.
    - Forward checking reduces the search space by detecting failures earlier than basic backtracking.
    
    1ERSA VERSION:
def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    stats = {"assignments": 0, "backtracks": 0}

    def forward_check(var: str, assignment: dict[str, str]) -> dict[str, list[str]] | None:

        eliminated: dict[str, list[str]] = {}

        for neighbor in csp.get_neighbors(var):
            if neighbor not in assignment:
                eliminated[neighbor] = []

            for val in list(domains[neighbor]):
              if not csp.is_consistent(neighbor, val, assignment):
                  csp.domains[neighbor].remove()
                  eliminated[neighbor].append()

        return eliminated

    def backtrack(cs: dict[str, str]) -> dict[str, str] | None:

      if csp.is_complete(cs):
          return cs

      unassigned = csp.get_unassigned_variables(cs)
      v = unassigned[0]

      for value in csp.domains[v]:
          stats["assignments"] += 1

          if csp.is_consistent(v, value, cs):

              csp.assign(v, value, cs)
              result = backtrack(cs)

              if result is not None:
                  return result

              csp.unassign(v, cs)
              stats["backtracks"] += 1

      return None

    cs: dict[str, str] = {}
    result = backtrack(cs)

    return result

Prompt: Corrige y completa el siguiente algoritmo de backtracking con Forward Checking para que funcione correctamente para un CSP de asignación de drones. 
Este debe seguir la lógica estándar de backtracking con forward checking, es decir seleccionar variable no asignada, probar valores del dominio, verificar consistencia, aplicar forward checking para eliminar valores inconsistentes en vecinos, restaurar dominios al hacer backtrack y usar correctamente los métodos del objeto.
Mantén la estructura general del código, la función backtracking_fc, las funciones internas como forward_check y backtrack. Solo corrige errores, agrega lo que falta y haz que el algoritmo sea funcional y coherente.    
    """
    stats = {"assignments": 0, "backtracks": 0}

    def forward_check(var: str, assignment: dict[str, str]) -> tuple[dict[str, list[str]], bool]:

        eliminated: dict[str, list[str]] = {}

        for neighbor in csp.get_neighbors(var):
            if neighbor not in assignment:
                eliminated[neighbor] = []

                for val in list(csp.domains[neighbor]):
                    if not csp.is_consistent(neighbor, val, assignment):
                        csp.domains[neighbor].remove(val)
                        eliminated[neighbor].append(val)

                if not csp.domains[neighbor]:
                    return eliminated, False  

        return eliminated, True

    def backtrack(cs: dict[str, str]) -> dict[str, str] | None:

        if csp.is_complete(cs):
            return cs

        v = csp.get_unassigned_variables(cs)[0]

        for value in list(csp.domains[v]):
            stats["assignments"] += 1

            if csp.is_consistent(v, value, cs):
                csp.assign(v, value, cs)
                eliminated, success = forward_check(v, cs)

                if success:
                    result = backtrack(cs)
                    if result is not None:
                        return result

                for neighbor, values in eliminated.items():
                    csp.domains[neighbor].extend(values)

                csp.unassign(v, cs)
                stats["backtracks"] += 1

        return None

    cs: dict[str, str] = {}
    result = backtrack(cs)

    print(f"[backtracking_fc] Asignaciones intentadas: {stats['assignments']}")
    print(f"[backtracking_fc] Backtracks realizados:   {stats['backtracks']}")

    return result

def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with AC-3 arc consistency.

    Tips:
    - AC-3 enforces arc consistency: for every pair of constrained variables (Xi, Xj), every value
      in Xi's domain must have at least one supporting value in Xj's domain.
    - Run AC-3 before starting backtracking to reduce domains globally.
    - After each assignment, run AC-3 on arcs involving the assigned variable's neighbors.
    - If AC-3 empties any domain, the current assignment is inconsistent - backtrack.
    - You can create helper functions such as:
      - a values_compatible function to check if two variable-value pairs are consistent with the constraints.
      - a revise function that removes unsupported values from one variable's domain.
      - an ac3 function that manages the queue of arcs to check and calls revise.
      - a backtrack function that integrates AC-3 into the search process.
    
    Primera_version:
    def values_compatible(xi, vi, xj, vj):
        return csp.is_consistent(xi, vi, xj, vj)
    
    def revise(domains, xi, xj):
        revised = False
        for vi in domains[xi][:]:
            supported = False
            for vj in domains[xj]:
                if values_compatible(xi, vi, xj, vj):
                    supported = True
                    break
            if not supported:
                domains[xi].remove(vi)
                revised = True
        return revised

    def ac3(domains, queue):
        while queue:
            xi, xj = queue.pop(0)
            if revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in csp.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True
    
    def backtrack(assignment, domains):
        if len(assignment) == len(csp.variables):
            return assignment
        
        for var in csp.variables:
            if var not in assignment:
                break

        for value in domains[var]:

            new_assignment = assignment.copy()
            new_assignment[var] = value

            new_domains = {v: domains[v][:] for v in domains}
            new_domains[var] = [value]

            queue = []
            for neighbor in csp.get_neighbors(var):
                queue.append((neighbor, var))

            if ac3(new_domains, queue):
                result = backtrack(new_assignment, new_domains)
                if result is not None:
                    return result

        return None
    
    domains = {v: csp.domains[v][:] for v in csp.variables}
    
    queue = []
    for xi in csp.variables:
        for xj in csp.get_neighbors(xi):
            queue.append((xi, xj))
            
    if not ac3(domains, queue):
        return None
    
    return backtrack({}, domains)
    
    Prompt:Estoy implementando el algoritmo backtracking_ac3 para un CSP de asignación de drones, al ejecutar el siguiente comando:
            python main.py -m csp -a backtracking_ac3 -l heavy_cargo -n 20 -q 
            obtengo “No solution found”, revisa si el problema está en la implementación de AC3 (revise, values_compatible) o en la función is_consistent? 
    
    """
    def values_compatible(xi, vi, xj, vj):
        if xi == xj:
            return False
        
        return True
    
    def revise(domains, xi, xj):
        revised = False
        for vi in domains[xi][:]:
            supported = False
            for vj in domains[xj]:
                if values_compatible(xi, vi, xj, vj):
                    supported = True
                    break
            if not supported:
                domains[xi].remove(vi)
                revised = True
        return revised

    def ac3(domains, queue):
        while queue:
            xi, xj = queue.pop(0)
            if revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in csp.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True
    
    def backtrack(assignment, domains):
        if len(assignment) == len(csp.variables):
            return assignment
        
        for var in csp.variables:
            if var not in assignment:
                break

        for value in domains[var]:

            new_assignment = assignment.copy()
            new_assignment[var] = value

            new_domains = {v: domains[v][:] for v in domains}
            new_domains[var] = [value]

            queue = []
            for neighbor in csp.get_neighbors(var):
                queue.append((neighbor, var))

            if ac3(new_domains, queue):
                result = backtrack(new_assignment, new_domains)
                if result is not None:
                    return result

        return None
    
    domains = {v: csp.domains[v][:] for v in csp.variables}
    
    queue = []
    for xi in csp.variables:
        for xj in csp.get_neighbors(xi):
            queue.append((xi, xj))
            
    if not ac3(domains, queue):
        return None
    
    return backtrack({}, domains)
    


def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking with Forward Checking + MRV + LCV.

    Tips:
    - Combine the techniques from backtracking_fc, mrv_heuristic, and lcv_heuristic.
    - MRV (Minimum Remaining Values): Select the unassigned variable with the fewest legal values.
      Tie-break by degree: prefer the variable with the most unassigned neighbors.
    - LCV (Least Constraining Value): When ordering values for a variable, prefer
      values that rule out the fewest choices for neighboring variables.
    - Use csp.get_num_conflicts(var, value, assignment) to count how many values would be ruled out for neighbors if var=value is assigned.
    
    Primera_version:
    def bactrack(assignment,domains):
        if len(assignment) == len(csp.variables):
            return assignment
        
        unnassigned = [v for v in csp.variables if v not in assignment]
        var = min(unnassigned, key=lambda var: len(domains[var]))
        
        values = sorted(domains[var], key=lambda val: csp.get_num_conflicts(mrv, val, assignment))

        for value in values:
            if csp.is_consistent(var, value, assignment):
                new_assignment = assignment.copy()
                new_assignment[var] = value

                new_domains = {v: domains[v][:] for v in domains}
                new_domains[var] = [value]

                for neighbor in csp.get_neighbors(var):
                    if neighbor not in new_assignment:
                        new_domains[neighbor] = [v for v in new_domains[neighbor] if csp.is_consistent(neighbor, v, new_assignment)]
                        if not new_domains[neighbor]:
                            break
                result = backtrack(new_assignment, new_domains)
                if result is not None:
                    return result
            return None
        domains = {v: csp.domains[v][:] for v in csp.variables}
        return backtrack({}, domains)
        
        Promt: Estoy implementando backtracking con MRV y LCV para un CSP de asignación de drones, esta es mi primera versión del código, pero no encuentra solución o tiene errores, ayudame a corregirlo y completar la implementación correctamente.
        """
    def backtrack(assignment,domains):
        if len(assignment) == len(csp.variables):
            return assignment
        
        unnassigned = [v for v in csp.variables if v not in assignment]
        var = min(unnassigned, key=lambda v: (len(domains[v]), -len(csp.get_neighbors(v))))
        
        values = sorted(domains[var], key=lambda val: csp.get_num_conflicts(var, val, assignment))

        for value in values:
            if csp.is_consistent(var, value, assignment):
                new_assignment = assignment.copy()
                new_assignment[var] = value

                new_domains = {v: domains[v][:] for v in domains}
                new_domains[var] = [value]
                failed = False

                for neighbor in csp.get_neighbors(var):
                    if neighbor not in new_assignment:
                        filtered = []

                        for v in new_domains[neighbor]:
                            temp_assignment = new_assignment.copy()
                            temp_assignment[neighbor] = v

                            if csp.is_consistent(neighbor, v, temp_assignment):
                                filtered.append(v)

                        new_domains[neighbor] = filtered
                        if not filtered:
                            failed = True
                            break

                if failed:
                    continue
                result = backtrack(new_assignment, new_domains)
                if result is not None:
                    return result
        return None
    domains = {v: csp.domains[v][:] for v in csp.variables}
    return backtrack({}, domains)