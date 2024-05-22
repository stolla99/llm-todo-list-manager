import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify


class Todo:
    def __init__(self, header_height, footer_height, custom_colors, small_margin):
        self.aside = dmc.Aside(
            width={"base": 400},
            height=f"calc(100vh - {header_height + footer_height}px)",
            withBorder=True,
            fixed=True,
            position={"left": 0, "top": header_height},
            sx={
                "mt": small_margin,
                "mb": small_margin,
            },
            style={
                "border": "1px solid #333138",
                "backgroundColor": custom_colors["jet"],
            },
            children=[
                html.Div(
                    id="notificationContainerTodoList",
                    children=[""],
                ),
                html.Div(
                    id="notificationContainerLocation",
                    children=[""],
                ),
                dmc.Modal(
                    id="aboutModal",
                    className="modal",
                    title="Information",
                    overflow="outside",
                    zIndex=10000,
                    radius="15px",
                    size="45%",
                    centered=True,
                    children=[
                        dcc.Markdown(
                            """
                            ## 🎓 About Me
                            
                            Hello! I'm **Arne**, currently pursuing a degree in **Computer Science** at **RPTU Kaiserslautern**. I'm passionate about harnessing the power of **Generative AI and Large Language Models (LLMs)** to create solutions that address real-world challenges. When I'm not coding, you can find me exploring nature through hiking and biking.
                            
                            ## 🌟 Why This Project?
                            
                            This project stemmed from my fascination with **LLMs and Generative AI**. It's designed to streamline the process of converting user inputs into actionable to-do tasks, enhancing productivity and interaction. It reflects my commitment to advancing how we interact with digital systems in our daily lives.
                            
                            ## 🔗 Let's Connect!
                            
                            -   **LinkedIn:** [Arne Stoll | LinkedIn](https://www.linkedin.com/in/arne-stoll-8163321b6/)
                            -   **GitHub:** [stolla99 (github.com)](https://github.com/stolla99)
                            
                            I'm eager to connect with you all and discuss how we can push the boundaries of what's possible with AI. Your feedback is invaluable—it helps refine this application and fuels my personal and professional growth. Thank you for your engagement and interest!
                            """
                        )
                    ],
                ),
                dmc.Modal(
                    id="tourModal",
                    className="tourModal",
                    title="",
                    overflow="outside",
                    zIndex=10000,
                    fullScreen=True,
                    overlayOpacity=0.0,
                    closeOnEscape=True,
                    children=[
                        html.Div(
                            className="listGuide",
                            children=[
                                dmc.Tooltip(
                                    className="tourTooltip",
                                    label="Here the todo list is displayed. "
                                          "New tasks will appear here based on your queries.",
                                    position="bottom",
                                    opened=True,
                                )]
                        ),
                        html.Div(
                            className="inputGuide",
                            children=[
                                dmc.Tooltip(
                                    className="tourTooltip",
                                    label="Here you can put in some queries to manage your todo list.",
                                    position="right-start",
                                    opened=True
                                )
                            ]
                        ),
                        html.Div(
                            className="chatWindowGuide",
                            children=[
                                dmc.Tooltip(
                                    className="tourTooltip",
                                    label="Here you can chat with the AI to manage your todo list. "
                                          "Messages will appear here.",
                                    position="right-start",
                                    opened=True
                                )
                            ]
                        ),
                    ],
                ),
                dmc.Stack(
                    [
                        html.Div(
                            children=[
                                dmc.Container(
                                    children=[
                                        dcc.Interval(
                                            id="waitForNewDataTrigger",
                                            interval=2000,
                                            n_intervals=0,
                                        ),
                                        html.Div(
                                            id="todoStack",
                                            className="todoStackList",
                                            children=[]
                                        ),
                                    ],
                                    style={
                                        "padding": 10,
                                    },
                                ),
                            ],
                            style={
                                "backgroundColor": custom_colors["jet"],
                                "margin": 0,
                                "mah": header_height,
                            },
                        ),
                        html.Div(
                            children=[
                                dmc.Container(
                                    style={
                                        "padding": 10,
                                    },
                                    children=[
                                        html.Div(
                                            className="locationDivClass",
                                            children=[
                                                html.Div(
                                                    className="locationIconDiv",
                                                    children=[
                                                        DashIconify(
                                                            className="locationIcon",
                                                            icon="streamline:location-compass-1",
                                                            width=20,
                                                            height=20,
                                                        )
                                                    ]
                                                ),
                                                dmc.Stack(
                                                    spacing=0,
                                                    className="locationStack",
                                                    children=[
                                                        dmc.Text(
                                                            "Location for weather",
                                                            className="mainTextButton"
                                                        ),
                                                        html.Div(
                                                            className="locationInputDiv",
                                                            children=[
                                                                dcc.Input(
                                                                    id="locationInput",
                                                                    className="locationInputClass",
                                                                    placeholder="Location for weather forecast ...",
                                                                    style={
                                                                        "width": "auto", "flex": 1
                                                                    },
                                                                    value="Kaiserslautern"
                                                                ),
                                                                html.Button(
                                                                    id="locationSubmit",
                                                                    className="locationSubmitClass",
                                                                    children=[
                                                                        DashIconify(
                                                                            className="locationIconSave",
                                                                            icon="fluent:save-20-filled",
                                                                            width=25,
                                                                            height=25,
                                                                            color="#adacb0"
                                                                        )
                                                                    ],
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),

                                            ]
                                        ),
                                        html.Div(
                                            className="weatherDivClass",
                                            children=[
                                                html.Div(
                                                    className="weatherDiv",
                                                    children=[
                                                        DashIconify(
                                                            className="placeholderIcon",
                                                            icon="carbon:radio-button",
                                                            width=21,
                                                            height=21,
                                                        )
                                                    ]
                                                ),
                                                dmc.Stack(
                                                    spacing=0,
                                                    children=[
                                                        dmc.Text(
                                                            "Weather forecast",
                                                            className="mainTextButton"
                                                        ),
                                                        dmc.Text(
                                                            "Disable weather forecast rag feature.",
                                                            className="subTextButton"
                                                        ),
                                                        dmc.Switch(
                                                            id="locationSwitch",
                                                            className="locationSwitchClass",
                                                            offLabel=DashIconify(icon="flat-color-icons:cancel",
                                                                                 width=20),
                                                            onLabel=DashIconify(icon="twemoji:sun-behind-rain-cloud",
                                                                                width=20),
                                                            size="lg",
                                                            checked=False,
                                                            persistence=True,
                                                        )
                                                    ]
                                                )
                                            ],
                                            style={
                                                "marginBottom": "10px",
                                            }
                                        ),
                                        dmc.Button(
                                            children=[
                                                dmc.Stack(
                                                    spacing="0px",
                                                    children=[
                                                        dmc.Text(
                                                            "Tour",
                                                            className="mainTextButton"
                                                        ),
                                                        dmc.Text(
                                                            "Take a tour through the app.",
                                                            className="subTextButton"
                                                        ),
                                                    ]
                                                )
                                            ],
                                            leftIcon=DashIconify(icon="carbon:help", width=20),
                                            id="tourButton",
                                            className="settingsButton",
                                        ),
                                        dmc.Button(
                                            children=[
                                                dmc.Stack(
                                                    spacing="0px",
                                                    children=[
                                                        dmc.Text(
                                                            "About",
                                                            className="mainTextButton"
                                                        ),
                                                        dmc.Text(
                                                            "Learn more about the app.",
                                                            className="subTextButton"
                                                        ),
                                                    ]
                                                )
                                            ],
                                            leftIcon=DashIconify(icon="carbon:information", width=20),
                                            id="aboutButton",
                                            className="settingsButton",
                                        ),
                                    ]
                                )
                            ],
                            style={
                                "backgroundColor": custom_colors["jet"],
                                "margin": 0,
                                "mah": header_height,
                            },
                        )
                    ],
                    align="stretch",
                    spacing="0px",
                    style={
                        "height": "inherit"
                    },
                    justify="space-between",
                )
            ],
        )

    def get_aside(self):
        return self.aside
