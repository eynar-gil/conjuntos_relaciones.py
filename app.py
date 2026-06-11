import flet as ft
import requests
from urllib.parse import urlparse

def main(page: ft.Page):
    page.title = "Método Iterativo de Gauss-Seidel"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    a11 = ft.TextField(value="5", label="A[1,1]", width=80, text_align=ft.TextAlign.CENTER)
    a12 = ft.TextField(value="2", label="A[1,2]", width=80, text_align=ft.TextAlign.CENTER)
    a13 = ft.TextField(value="1", label="A[1,3]", width=80, text_align=ft.TextAlign.CENTER)
    
    a21 = ft.TextField(value="1", label="A[2,1]", width=80, text_align=ft.TextAlign.CENTER)
    a22 = ft.TextField(value="4", label="A[2,2]", width=80, text_align=ft.TextAlign.CENTER)
    a23 = ft.TextField(value="2", label="A[2,3]", width=80, text_align=ft.TextAlign.CENTER)
    
    a31 = ft.TextField(value="1", label="A[3,1]", width=80, text_align=ft.TextAlign.CENTER)
    a32 = ft.TextField(value="2", label="A[3,2]", width=80, text_align=ft.TextAlign.CENTER)
    a33 = ft.TextField(value="5", label="A[3,3]", width=80, text_align=ft.TextAlign.CENTER)
    
    b1 = ft.TextField(value="11", label="b[1]", width=80, text_align=ft.TextAlign.CENTER)
    b2 = ft.TextField(value="15", label="b[2]", width=80, text_align=ft.TextAlign.CENTER)
    b3 = ft.TextField(value="20", label="b[3]", width=80, text_align=ft.TextAlign.CENTER)
    
    txt_solucion = ft.Text(value="", size=18, color="green", weight=ft.FontWeight.BOLD)
    txt_iteraciones = ft.Text(value="", size=14)
    txt_condicion = ft.Text(value="", size=14)
    txt_clasificacion = ft.Text(value="", size=14)
    txt_error = ft.Text(value="", size=16, color="red")
    
    lista_convergencia_vertical = ft.ListView(expand=True, height=350, spacing=8)
    
    def boton_resolver_click(e):
        txt_error.value = ""
        txt_solucion.value = ""
        txt_iteraciones.value = ""
        txt_condicion.value = ""
        txt_clasificacion.value = ""
        lista_convergencia_vertical.controls.clear()
        page.update()
        
        payload = {
            "matrix": [
                [float(a11.value), float(a12.value), float(a13.value)],
                [float(a21.value), float(a22.value), float(a23.value)],
                [float(a31.value), float(a32.value), float(a33.value)]
            ],
            "vector": [float(b1.value), float(b2.value), float(b3.value)]
        }
        
        # INICIALIZAMOS LA VARIABLE FUERA DEL TRY PARA EVITAR ERRORES DE ÁMBITO
        url_api = ""
        
        try:
            # DETECCIÓN AUTOMÁTICA DE LA RED (Celular o PC)
            parsed_url = urlparse(page.url)
            ip_actual = parsed_url.hostname if parsed_url.hostname else "127.0.0.1"
            
            # Ajuste dinámico inteligente para convivir con el Modo Host de Docker
            if ip_actual == "127.0.0.1" or ip_actual == "localhost":
                url_api = "http://127.0.0.1:8000/api/gauss-seidel"
            else:
                url_api = f"http://{ip_actual}:8000/api/gauss-seidel"
            
            response = requests.post(url_api, json=payload, timeout=5)
            data = response.json()
            
            if data.get("exito"):
                if data.get("converge"):
                    txt_solucion.value = f"Solución final: {data['solucion']}"
                    txt_solucion.color = "green"
                else:
                    txt_solucion.value = f"Divergencia (No convergió): {data['solucion']}"
                    txt_solucion.color = "orange"
                    
                txt_iteraciones.value = f"Iteraciones ejecutadas: {data['iteraciones']}"
                txt_condicion.value = f"Número de condición Matrix: {data['numero_condicion']}"
                txt_clasificacion.value = f"Estabilidad: {data['clasificacion']}"
                
                for paso in data["traza"]:
                    card_iteracion = ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(f"Iteración k = {paso['k']}", weight=ft.FontWeight.BOLD, color="blue"),
                                    ft.Text(f" • Valor X: {paso['x']}", size=14),
                                    ft.Text(f" • Valor Y: {paso['y']}", size=14),
                                    ft.Text(f" • Valor Z: {paso['z']}", size=14),
                                ],
                                spacing=3
                            ),
                            padding=10
                        )
                    )
                    lista_convergencia_vertical.controls.append(card_iteracion)
            else:
                txt_error.value = f"{data['error']}"
                
        except Exception as ex:
            txt_error.value = f"Error de conexión al servidor en {url_api if url_api else 'la API'}"
            
        page.update()

    btn_calcular = ft.ElevatedButton(
        "Resolver Sistema", 
        on_click=boton_resolver_click, 
        bgcolor="blue", 
        color="white"
    )
    
    contenido_columna = ft.Column(
        controls=[
            ft.Text("Analizador Computacional Gauss-Seidel", size=22, weight=ft.FontWeight.BOLD),
            ft.Text("Ajuste de Convergencia Dinámica y Traza Vertical", size=13, italic=True, color="grey"),
            ft.Divider(),
            
            ft.Text("Coeficientes de la Matriz (A):", size=15, weight=ft.FontWeight.W_500),
            ft.Row(controls=[a11, a12, a13]),
            ft.Row(controls=[a21, a22, a23]),
            ft.Row(controls=[a31, a32, a33]),
            
            ft.Text("Términos Independientes (b):", size=15, weight=ft.FontWeight.W_500),
            ft.Row(controls=[b1, b2, b3]),
            
            ft.Container(content=btn_calcular, padding=10),
            
            ft.Text("RESULTADOS DEL SERVIDOR", size=15, weight=ft.FontWeight.BOLD),
            txt_error,
            txt_solucion,
            txt_iteraciones,
            txt_condicion,
            txt_clasificacion,
            
            ft.Divider(),
            ft.Text("Historial de Convergencia Lineal (Vertical)", size=15, weight=ft.FontWeight.BOLD, color="blue"),
            lista_convergencia_vertical
        ],
        spacing=10
    )
    
    layout_final = ft.Container(content=contenido_columna, padding=15)
    page.add(layout_final)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
