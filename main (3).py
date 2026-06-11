from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def garantizar_dominancia_diagonal(A, b):
    """ Reordena las filas de la matriz para intentar maximizar los elementos diagonales """
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n = len(b_np)
    
    A_opt = np.zeros_like(A_np)
    b_opt = np.zeros_like(b_np)
    filas_usadas = set()
    
    for i in range(n):
        # Buscar la fila que tenga el valor absoluto máximo en la columna 'i'
        mejor_fila = -1
        max_val = -1.0
        for r in range(n):
            if r not in filas_usadas:
                if abs(A_np[r, i]) > max_val:
                    max_val = abs(A_np[r, i])
                    mejor_fila = r
        
        if mejor_fila != -1:
            A_opt[i] = A_np[mejor_fila]
            b_opt[i] = b_np[mejor_fila]
            filas_usadas.add(mejor_fila)
        else:
            # Si no se encuentra una fila óptima ideal, se mantiene la original para evitar colapsos
            return A_np, b_np
            
    return A_opt, b_opt

@app.post("/api/gauss-seidel")
async def api_gauss_seidel(request: Request):
    try:
        data = await request.json()
        A_raw = data.get("matrix")
        b_raw = data.get("vector")
        tol = float(data.get("tol", 1e-5))
        max_iter = int(data.get("max_iter", 50))
        
        # Estabilizamos automáticamente el orden de las ecuaciones
        A_np, b_np = garantizar_dominancia_diagonal(A_raw, b_raw)
        
        n = len(b_np)
        x = np.zeros(n)
        historial_traza = []
        convergencia_exitosa = False
        
        for k in range(1, max_iter + 1):
            x_anterior = x.copy()
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    if j != i:
                        suma += A_np[i, j] * x[j]
                # Prevenir división por cero si la diagonal es nula
                diagonal = A_np[i, i] if A_np[i, i] != 0 else 1e-12
                x[i] = (b_np[i] - suma) / diagonal
            
            historial_traza.append({
                "k": k,
                "x": round(x[0], 4),
                "y": round(x[1], 4),
                "z": round(x[2], 4) if n > 2 else 0.0
            })
            
            if np.max(np.abs(x - x_anterior)) < tol:
                convergencia_exitosa = True
                break
                
        num_condicion = np.linalg.cond(A_np)
        clasificacion = "Estable" if num_condicion < 100 else "Mal Condicionado"
        
        return {
            "exito": True,
            "converge": convergencia_exitosa,
            "solucion": [round(val, 4) for val in x],
            "iteraciones": k,
            "numero_condicion": round(num_condicion, 2),
            "clasificacion": clasificacion,
            "traza": historial_traza
        }
        
    except Exception as e:
        return {"exito": False, "error": str(e)}
