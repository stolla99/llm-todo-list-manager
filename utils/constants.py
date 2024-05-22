# custom variables
from dash_iconify import DashIconify

custom_colors = {
    "davy_grey": "#565264",
    "dim_grey": "#706677",
    "mountbatten_pink": "#A6808C",
    "pale_dogwood": "#CCB7AE",
    "timberwolf": "#D6CFCB",
    "jet": "#333138",
    "dark": "#1a1b1e",
}
header_height = 50
footer_height = 30
small_margin = 5
container_height = f"calc(100vh - {header_height + footer_height}px)"
style = {
    "height": container_height,
    "marginTop": header_height,
    "marginBottom": footer_height,
}

voice_micro = DashIconify(icon="mdi:microphone", width=30, height=30)
voice_record = DashIconify(icon="mdi:record", width=30, height=30)
