import flet as ft
import requests
import matplotlib.pyplot as plt
import numpy as np
import time

# FUNCION

def f(x):
    return 0.5 * (x**3) - 4 * x + 3

# MAIN
def main(page: ft.Page):

    page.title = "Sistema de Riego Inteligente"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1400
    page.window_height = 900
    page.scroll = "auto"
    page.padding = 0

# INPUNT
    ip_input = ft.TextField(
        label="IP Backend",
        value="http://127.0.0.1:8000",
        bgcolor="white",
        color="black"
    )

    a_input = ft.TextField(
        label="Valor A / X0",
        bgcolor="white",
        color="black"
    )

    b_input = ft.TextField(
        label="Valor B / X1",
        bgcolor="white",
        color="black"
    )

    tol_input = ft.TextField(
        label="Tolerancia",
        value="0.001",
        bgcolor="white",
        color="black"
    )

# RESULTADOS
    resultado_bis = ft.Text(
        size=18,
        weight="bold",
        color="white"
    )

    resultado_sec = ft.Text(
        size=18,
        weight="bold",
        color="white"
    )

    comparacion = ft.Text(
        size=18,
        weight="bold",
        color="black"
    )
# TABLA BISS
    tabla_bis = ft.DataTable(

        bgcolor="#1e293b",

        border=ft.Border.all(1, "white54"),

        columns=[

            ft.DataColumn(
                ft.Text("Iter", color="white")
            ),

            ft.DataColumn(
                ft.Text("a", color="white")
            ),

            ft.DataColumn(
                ft.Text("b", color="white")
            ),

            ft.DataColumn(
                ft.Text("c", color="white")
            ),

            ft.DataColumn(
                ft.Text("f(c)", color="white")
            ),

        ],

        rows=[]
    )

    # TABLA SECANTE
    tabla_sec = ft.DataTable(

        bgcolor="#1e293b",

        border=ft.Border.all(1, "white54"),

        columns=[

            ft.DataColumn(
                ft.Text("Iter", color="white")
            ),

            ft.DataColumn(
                ft.Text("x0", color="white")
            ),

            ft.DataColumn(
                ft.Text("x1", color="white")
            ),

            ft.DataColumn(
                ft.Text("x2", color="white")
            ),

            ft.DataColumn(
                ft.Text("f(x2)", color="white")
            ),

        ],

        rows=[]
    )

    # GRAFICA
    grafica = ft.Image(
        src="",
        width=750,
        height=400,
        fit="contain"
    )

    #  FUNCIÓN CALCULAR
    def calcular(e):

        try:

            tabla_bis.rows.clear()
            tabla_sec.rows.clear()

            base_url = ip_input.value

            a = float(a_input.value)
            b = float(b_input.value)
            tol = float(tol_input.value)

            #  BISECCIÓN
            payload_bis = {
                "a": a,
                "b": b,
                "tolerancia": tol,
                "max_iter": 50
            }

            r_bis = requests.post(
                f"{base_url}/biseccion",
                json=payload_bis
            )

            data_bis = r_bis.json()

            resultado_bis.value = (
                f"Resultado Bisección: "
                f"{data_bis.get('resultado')}"
            )

            iteraciones_bis = data_bis.get(
                "iteraciones",
                []
            )

            for row in iteraciones_bis:

                tabla_bis.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("iteracion", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("a", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("b", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("c", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("f(c)", "")),
                                    color="white"
                                )
                            ),

                        ]

                    )

                )

            # SECANTE
            payload_sec = {
                "x0": a,
                "x1": b,
                "tolerancia": tol,
                "max_iter": 50
            }

            r_sec = requests.post(
                f"{base_url}/secante",
                json=payload_sec
            )

            data_sec = r_sec.json()

            resultado_sec.value = (
                f"Resultado Secante: "
                f"{data_sec.get('resultado')}"
            )

            iteraciones_sec = data_sec.get(
                "iteraciones",
                []
            )

            for row in iteraciones_sec:

                tabla_sec.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("iteracion", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("x0", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("x1", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("x2", "")),
                                    color="white"
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(row.get("f(x2)", "")),
                                    color="white"
                                )
                            ),

                        ]

                    )

                )

            # COMPARACION
            total_bis = len(iteraciones_bis)
            total_sec = len(iteraciones_sec)

            if total_bis < total_sec:

                ganador = "Bisección"

            elif total_sec < total_bis:

                ganador = "Secante"

            else:

                ganador = "Empate"

            comparacion.value = (
                f"🏆 Método más eficiente: {ganador}\n"
                f"Bisección: {total_bis} iteraciones\n"
                f"Secante: {total_sec} iteraciones"
            )

            # GRAFICA
            x = np.linspace(-5, 5, 400)

            y = f(x)

            plt.figure(figsize=(8, 4))

            plt.plot(x, y)

            plt.axhline(0)

            plt.grid(True)

            plt.title("Gráfica de la Función")

            plt.xlabel("x")

            plt.ylabel("f(x)")

            nombre_grafica = f"assets/grafica_{int(time.time())}.png"

            plt.savefig(nombre_grafica)

            plt.close()

            grafica.src = nombre_grafica

        except Exception as ex:

            comparacion.value = f"Error: {ex}"

        page.update()

    # BOTON
    boton = ft.ElevatedButton(
        "Calcular",
        on_click=calcular
    )

    # PANEL IZQUIERDO
    panel_izquierdo = ft.Container(

        width=350,

        image=ft.DecorationImage(
            src="assets/goat.jpeg",
            fit="cover"
        ),

        content=ft.Container(

            bgcolor="#000000AA",

            padding=20,

            content=ft.Column(

                [

                    ft.Text(
                        "Sistema de Riego Inteligente",
                        size=28,
                        weight="bold",
                        color="white"
                    ),

                    ip_input,

                    a_input,

                    b_input,

                    tol_input,

                    boton

                ]

            )

        )

    )

    # PANEL DERECHO
    panel_derecho = ft.Container(

        expand=True,

        padding=20,

        bgcolor="white",

        content=ft.Column(

            scroll="auto",

            controls=[

                ft.Text(
                    "Resultados",
                    size=30,
                    weight="bold",
                    color="blue"
                ),

                resultado_bis,

                resultado_sec,

                ft.Divider(),

                ft.Text(
                    "Iteraciones Bisección",
                    size=20,
                    weight="bold"
                ),

                ft.Row(
                    [tabla_bis],
                    scroll="auto"
                ),

                ft.Divider(),

                ft.Text(
                    "Iteraciones Secante",
                    size=20,
                    weight="bold"
                ),

                ft.Row(
                    [tabla_sec],
                    scroll="auto"
                ),

                ft.Divider(),

                ft.Text(
                    "Gráfica de la Función",
                    size=20,
                    weight="bold",
                    color="blue"
                ),

                grafica,

                ft.Divider(),

                ft.Text(
                    "Comparativa",
                    size=20,
                    weight="bold",
                    color="blue"
                ),

                comparacion

            ]

        )

    )

    #  LAYOUT
    page.add(

        ft.Row(

            [

                panel_izquierdo,

                panel_derecho

            ],

            expand=True

        )

    )


# RUN
ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=8550,
    assets_dir="assets"
)
