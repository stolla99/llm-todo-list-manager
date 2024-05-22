import dash_mantine_components as dmc


class Layout:
    def __init__(self, footer_height, header_height, custom_colors):
        self.custom_colors = custom_colors
        self.header = dmc.Header(
            height=header_height,
            fixed=True,
            children=[
                dmc.Container(
                    fluid=True,
                    style={
                        "height": "100%",
                        "width": "100%",
                        "margin": "0 0 0 0",
                        "padding": "0 0 0 0"
                    },
                    children=dmc.Group(
                        align="apart",
                        grow=True,
                        style={
                            "width": "100%",
                            "height": "100%",
                        },
                        children=[
                            dmc.Container(
                                fluid=True,
                                children=[
                                    dmc.Group(
                                        children=[
                                            dmc.Image(src="../assets/brain.png", width=header_height - 5,
                                                      height=header_height - 5),
                                            dmc.Stack(
                                                children=[
                                                    dmc.Text(
                                                        "Aeon Task Mind",
                                                        variant="gradient",
                                                        sx={"margin": "0 0 0 0", "padding": "0 0 0 0"},
                                                        gradient={"from": "#c14d56", "to": "#7b82db", "deg": 45},
                                                        style={
                                                            "fontSize": 20,
                                                        },
                                                    ),
                                                    dmc.Text(
                                                        "An app written by Arne Stoll for the course "
                                                        "Engineering with Generative AI",
                                                        variant="gradient",
                                                        gradient={"from": "#c14d56", "to": "#7b82db", "deg": 45},
                                                        style={
                                                            "fontSize": 8,
                                                        },
                                                    )
                                                ],
                                                spacing="0px",
                                            ),

                                        ],
                                        style={
                                            "height": "100%",
                                        },
                                        position="left"
                                    )
                                ],
                                style={
                                    "padding": "0 0 0 0",
                                    "margin": "0 0 0 0",
                                }),
                            dmc.Container(
                                children=[
                                    dmc.Group(
                                        position="right",
                                        children=[
                                            dmc.Image(
                                                src="../assets/transparent-rptu_logo_u.png",
                                                height=35,
                                                width=35,
                                                style={
                                                    "margin": 5,
                                                }
                                            )
                                        ],
                                        align="apart",
                                    )
                                ],
                                style={
                                    "padding": "0 0 0 0",
                                    "margin": "0 0 0 0",
                                },
                                fluid=True,
                            ),
                        ],
                    )
                )
            ],
            style={
                "border": "1px solid #333138",
                "backgroundColor": custom_colors["jet"],
            }
        )
        self.footer = dmc.Footer(
            height=footer_height,
            fixed=True,
            children=[
                dmc.Text(
                    "© 2024 Aeon Task Mind. All rights reserved.",
                    inline=True,
                    color="dimmed",
                    style={
                        "marginTop": 10,
                        "fontSize": 10,
                        "textAlign": "center",
                        "height": "100%",
                    },
                )
            ],
            style={
                "border": "1px solid #333138",
                "backgroundColor": custom_colors["jet"],
            },
        )

    def get_header(self):
        return self.header

    def get_footer(self):
        return self.footer
