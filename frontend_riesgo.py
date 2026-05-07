import reflex as rx
import requests
import math
from typing import List, Dict


class State(rx.State):

    a: str = ""
    b: str = ""
    tolerancia: str = ""

    resultado_biseccion: str = ""
    resultado_secante: str = ""

    iteraciones_biseccion: List[Dict] = []
    iteraciones_secante: List[Dict] = []

    
    grafica_data = [
        {
            "x": x / 10,
            "y": 0.5 * (x / 10) ** 3 - 4 * (x / 10) + 3
        }
        for x in range(-50, 51)
    ]

    def set_a(self, v):
        self.a = v

    def set_b(self, v):
        self.b = v

    def set_tolerancia(self, v):
        self.tolerancia = v

    def calcular(self):

 
        try:
            r1 = requests.post(
                "http://127.0.0.1:8000/biseccion",
                json={
                    "a": float(self.a),
                    "b": float(self.b),
                    "tolerancia": float(self.tolerancia),
                    "max_iter": 20
                }
            )

            res1 = r1.json()

            self.iteraciones_biseccion = res1.get("iteraciones", [])
            self.resultado_biseccion = str(
                res1.get("resultado", "Error")
            )

        except:
            self.resultado_biseccion = "Error"
            self.iteraciones_biseccion = []

        
        try:
            r2 = requests.post(
                "http://127.0.0.1:8000/secante",
                json={
                    "x0": float(self.a),
                    "x1": float(self.b),
                    "tolerancia": float(self.tolerancia),
                    "max_iter": 20
                }
            )

            res2 = r2.json()

            self.iteraciones_secante = res2.get("iteraciones", [])
            self.resultado_secante = str(
                res2.get("resultado", "Error")
            )

        except:
            self.resultado_secante = "Error"
            self.iteraciones_secante = []



def tabla(data):

    return rx.box(

      
        rx.hstack(
            rx.text(
                "Iter",
                width="60px",
                weight="bold",
                border_right="1px solid gray"
            ),

            rx.text(
                "a/x0",
                width="80px",
                weight="bold",
                border_right="1px solid gray"
            ),

            rx.text(
                "b/x1",
                width="80px",
                weight="bold",
                border_right="1px solid gray"
            ),

            rx.text(
                "c/x2",
                width="80px",
                weight="bold",
                border_right="1px solid gray"
            ),

            rx.text(
                "f(x)",
                width="120px",
                weight="bold"
            ),

            border_bottom="2px solid white",
            padding="4px"
        ),

        rx.divider(),

        
        rx.foreach(
            data,

            lambda row: rx.hstack(

                rx.text(
                    row["iteracion"],
                    width="60px",
                    border_right="1px solid gray"
                ),

                rx.text(
                    row.get("a", row.get("x0")),
                    width="80px",
                    border_right="1px solid gray"
                ),

                rx.text(
                    row.get("b", row.get("x1")),
                    width="80px",
                    border_right="1px solid gray"
                ),

                rx.text(
                    row.get("c", row.get("x2")),
                    width="80px",
                    border_right="1px solid gray"
                ),

                rx.text(
                    row.get("f(c)", row.get("f(x2)")),
                    width="120px"
                ),

                border_bottom="1px solid gray",
                padding="4px"
            )
        ),

        border="1px solid white",
        padding="10px",
        width="100%"
    )



def index():

    return rx.box(

        rx.hstack(


            rx.box(

                rx.vstack(

                    rx.heading(
                        "Sistema de Riego Inteligente",
                        color="white"
                    ),

                    rx.input(
                        placeholder="Valor a",
                        value=State.a,
                        on_change=State.set_a
                    ),

                    rx.input(
                        placeholder="Valor b",
                        value=State.b,
                        on_change=State.set_b
                    ),

                    rx.input(
                        placeholder="Tolerancia",
                        value=State.tolerancia,
                        on_change=State.set_tolerancia
                    ),

                    rx.button(
                        "Calcular",
                        on_click=State.calcular,
                        color_scheme="blue"
                    ),

                    spacing="4"
                ),

                width="30%",
                bg="rgba(0,0,60,0.75)",
                backdrop_filter="blur(10px)",
                padding="20px",
                height="100vh"
            ),


            rx.box(

                rx.vstack(

                    rx.heading(
                        "Resultados",
                        color="blue"
                    ),


                    rx.text(
                        "Bisección:",
                        weight="bold"
                    ),

                    rx.text(State.resultado_biseccion),

                    rx.text(
                        "Secante:",
                        weight="bold"
                    ),

                    rx.text(State.resultado_secante),

                    rx.divider(),

                    rx.heading("Iteraciones Bisección"),

                    tabla(State.iteraciones_biseccion),

                    rx.divider(),

                    rx.heading("Iteraciones Secante"),

                    tabla(State.iteraciones_secante),

                    rx.divider(),
                    rx.heading(
                        "Gráfica de la Función",
                        color="blue"
                    ),

                    rx.recharts.line_chart(

                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3"
                        ),

                        rx.recharts.x_axis(data_key="x"),

                        rx.recharts.y_axis(),

                        rx.recharts.tooltip(),

                        rx.recharts.line(
                            data_key="y",
                            stroke="blue",
                            type_="monotone"
                        ),

                        data=State.grafica_data,

                        width="100%",
                        height=400,
                    ),

                    rx.divider(),

                    rx.box(

                        rx.heading(
                            "Comparativa de Métodos",
                            color="blue"
                        ),

                        rx.hstack(


                            rx.box(

                                rx.vstack(

                                    rx.text(
                                        "Bisección",
                                        weight="bold"
                                    ),

                                    rx.text(
                                        "Iteraciones:"
                                    ),

                                    rx.text(
                                        State.iteraciones_biseccion.length()
                                    ),

                                    rx.text(
                                        "Resultado:"
                                    ),

                                    rx.text(
                                        State.resultado_biseccion
                                    ),
                                ),

                                bg="white",
                                padding="10px",
                                border_radius="10px",
                                width="200px"
                            ),

                            rx.box(

                                rx.vstack(

                                    rx.text(
                                        "Secante",
                                        weight="bold"
                                    ),

                                    rx.text(
                                        "Iteraciones:"
                                    ),

                                    rx.text(
                                        State.iteraciones_secante.length()
                                    ),

                                    rx.text(
                                        "Resultado:"
                                    ),

                                    rx.text(
                                        State.resultado_secante
                                    ),
                                ),

                                bg="white",
                                padding="10px",
                                border_radius="10px",
                                width="200px"
                            ),

                            spacing="5"
                        ),

                        rx.divider(),

                        rx.text(
                            "El método Secante normalmente converge más rápido que Bisección."
                        ),

                        bg="white",
                        padding="20px",
                        border_radius="10px",
                        width="100%"
                    ),

                    spacing="4"
                ),

                width="70%",
                padding="20px",
                bg="rgba(255,255,255,0.9)",
                backdrop_filter="blur(10px)",
                border_radius="10px"
            ),
        ),


        style={
            "background": "url('/background_space.jpeg') no-repeat center center fixed",
            "background_size": "cover",
            "min_height": "100vh"
        }
    )



app = rx.App()
app.add_page(index)
