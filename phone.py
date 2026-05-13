import os
import webbrowser
import phonenumbers
import folium

from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from key import keys


banner = r"""
 ▄    ▄        ▄▄▄▄▄  ▄    ▄  ▄▄▄▄  ▄▄   ▄ ▄▄▄▄▄▄
  █  █         █   ▀█ █    █ ▄▀  ▀▄ █▀▄  █ █
   ██          █▄▄▄█▀ █▄▄▄▄█ █    █ █ █▄ █ █▄▄▄▄▄
  ▄▀▀▄   ▀▀▀   █      █    █ █    █ █  █ █ █
 ▄▀  ▀▄        █      █    █  █▄▄█  █   ██ █▄▄▄▄▄

             By ST4R-SHINY
"""


def localizar_numero():
    os.system("cls" if os.name == "nt" else "clear")

    print(banner)

    numero = input("Número de teléfono > ")

    try:
        numero_procesado = phonenumbers.parse(numero)

        ubicacion = geocoder.description_for_number(numero_procesado, "es")
        operadora = carrier.name_for_number(numero_procesado, "es")

        geo = OpenCageGeocode(keys)
        resultados = geo.geocode(ubicacion)

        if not resultados:
            print("\nNo se encontró la ubicación.")
            return

        datos = resultados[0]

        latitud = datos["geometry"]["lat"]
        longitud = datos["geometry"]["lng"]

        zona_horaria = datos["annotations"]["timezone"]["name"]
        moneda = datos["annotations"]["currency"]["name"]
        simbolo = datos["annotations"]["currency"]["symbol"]
        bandera = datos["annotations"]["flag"]

        link_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

        print("\n═════════════════════════════════════════════════════════════════════")
        print(f" Número      : {numero}")
        print(f" Ubicación   : {ubicacion}")
        print(f" Operadora   : {operadora}")
        print(f" Zona Horaria: {zona_horaria}")
        print(f" Moneda      : {moneda} ({simbolo})")
        print(f" Bandera     : {bandera}")
        print(f" Latitud     : {latitud}")
        print(f" Longitud    : {longitud}")
        print(f" Google Maps : {link_maps}")
        print("════════════════════════════════════════════════════════════════════════")

        mapa = folium.Map(location=[latitud, longitud], zoom_start=8)

        folium.Marker(
            [latitud, longitud],
            popup=f"{ubicacion} {bandera}",
            tooltip=numero
        ).add_to(mapa)

        mapa.save("localizacion.html")

        webbrowser.open(link_maps)

    except Exception as error:
        print(f"\nError: {error}")

    input("\nPresiona ENTER para salir...")


localizar_numero()