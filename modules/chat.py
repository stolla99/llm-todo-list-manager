import dash_mantine_components as dmc
from dash import dcc
from dash import html
from dash_iconify import DashIconify

import utils.constants as c
from modules.voice import Voice


class Chat:
    def __init__(self, custom_colors, style):
        self.input_height = 40
        self.custom_colors = custom_colors
        self.style = style
        self.chat_layout = dmc.Container(
            [
                dmc.Stack(
                    [
                        dmc.Container(
                            fluid=True,
                            children=[
                                dmc.Stack(
                                    id="chatContainerMain",
                                    className="chatContainerMainClass",
                                    align="stretch",
                                    justify="flex-end",
                                    spacing=5,
                                    style={
                                        "height": "100%",
                                        "width": "100%",
                                        "paddingLeft": 5,
                                        "paddingRight": 5,
                                    },
                                    children=[
                                        html.Div(
                                            id="scrollbarDiv",
                                            className="chatContainer",
                                            children=[
                                                # message will go here be callback
                                            ],
                                            style={
                                                "height": f"calc({c.container_height} - 70px)",
                                                "width": "100%",
                                                "padding": "0 0 0 0",
                                                "margin": "0 0 0 0",
                                            }
                                        )
                                    ],
                                )
                            ],
                            style={
                                "flex": 1,
                                "width": "100%",
                                "padding": "0 0 0 0",
                                "margin": "0 0 0 0",
                            }),
                        dmc.Paper(
                            children=[
                                dmc.Group(
                                    id="inputGroup",
                                    className="inputGroup",
                                    children=[
                                        dmc.Modal(
                                            id="voiceModal",
                                            className="modal",
                                            title="",
                                            overflow="outside",
                                            zIndex=10000,
                                            radius="15px",
                                            size="15%",
                                            withCloseButton=False,
                                            closeOnEscape=False,
                                            closeOnClickOutside=False,
                                            withFocusReturn=False,
                                            centered=True,
                                            children=[
                                                Voice().get_voice_recorder()
                                            ],
                                        ),
                                        dcc.Input(
                                            id="messageInput",
                                            className="messageInputClass",
                                            placeholder="Type message...",
                                            style={
                                                "marginLeft": 4,
                                                "width": "auto", "flex": 1},
                                        ),
                                        dmc.ActionIcon(
                                            id="recordVoiceButton",
                                            className="actionButton",
                                            children=[DashIconify(icon="mingcute:voice-line", width=25)],
                                            color="gray",
                                            variant="filled",
                                            style={"marginLeft": 5, "marginRight": 2, "width": self.input_height,
                                                   "height": self.input_height}
                                        ),
                                        dmc.ActionIcon(
                                            id="sendButton",
                                            className="actionButton",
                                            children=[DashIconify(icon="lets-icons:send-hor-fill", width=30, rotate=3)],
                                            color="gray",
                                            variant="filled",
                                            size="lg",
                                            style={"marginLeft": 2, "marginRight": 5, "width": self.input_height,
                                                   "height": self.input_height}
                                        ),
                                    ],
                                    spacing=0,
                                    style={
                                        "paddingTop": 4,
                                        "paddingBottom": 5,
                                    }
                                )
                            ],
                            sx={
                                "backgroundColor": custom_colors["jet"],
                                "margin": 5,
                                "maxHeight": 50,
                            },
                        ),
                    ],
                    spacing=5,
                    align="stretch",
                    justify="flex-end",
                    style={
                        "height": "100%",
                        "width": "100%",
                    }
                )
            ],
            style=style,
        )

    def get_chat(self):
        return self.chat_layout
