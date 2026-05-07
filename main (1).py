from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class InputBiseccion(BaseModel):
    a: float
    b: float
    tolerancia: float
    max_iter: int

class InputSecante(BaseModel):
    x0: float
    x1: float
    tolerancia: float
    max_iter: int


def f(x):

    return 0.5 * (x**3) - 4 * x + 3


@app.get("/")
def inicio():
    return {"mensaje": "API de métodos numéricos funcionando correctamente"}


@app.post("/biseccion")
def biseccion(data: InputBiseccion):
    a, b = data.a, data.b
    tol, max_iter = data.tolerancia, data.max_iter
    iteraciones = []


    if f(a) * f(b) >= 0:
        return {"resultado": "Error: f(a) y f(b) deben tener signos opuestos", "iteraciones": []}

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        iteraciones.append({
            "iteracion": i + 1,
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "f(c)": round(fc, 6)
        })

        if abs(fc) < tol:
            break

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return {"resultado": round(c, 6), "iteraciones": iteraciones}


@app.post("/secante")
def secante(data: InputSecante):
    x0, x1 = data.x0, data.x1
    tol, max_iter = data.tolerancia, data.max_iter
    iteraciones = []

    for i in range(max_iter):
        fx0, fx1 = f(x0), f(x1)

        if fx1 - fx0 == 0:
            break

        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)

        iteraciones.append({
            "iteracion": i + 1,
            "x0": round(x0, 6),
            "x1": round(x1, 6),
            "x2": round(x2, 6),
            "f(x2)": round(f(x2), 6)
        })

        if abs(x2 - x1) < tol:
            return {"resultado": round(x2, 6), "iteraciones": iteraciones}

        x0, x1 = x1, x2

    return {"resultado": round(x2, 6), "iteraciones": iteraciones}
