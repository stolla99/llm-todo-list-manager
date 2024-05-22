import uuid

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

import utils.constants


class Message:
    def __init__(self, sender, text, uuid_message=None, is_you=True):
        self.sender = sender
        self.text = text
        self.uuid = str(uuid_message) if uuid_message is not None else str(uuid.uuid4())
        self.src_image: str = "/assets/avatar_you.png" if is_you else "/assets/avatar_bot.png"
        self.component = None

    def get_message(self, timestamp):
        self.component = html.Div(
            className="messageContainer",
            style={
                "width": "100%",
                "borderRadius": "5px",
                "marginTop": 5,
            },
            children=[dmc.Paper(
                style={
                    "padding": "10px 10px",
                    "backgroundColor": "transparent",
                },
                children=[
                    html.Div(
                        id={"type": "notificationsContainer", "index": self.uuid},
                        className="notificationsContainerClass",
                    ),
                    dmc.Group(
                        align="start",
                        children=[
                            dmc.Avatar(
                                src=self.src_image,
                                alt="Avatar",
                                radius="xl",
                                size="md",
                                style={
                                    "width": "10",
                                    "backgroundColor": "white",
                                }
                            ),
                            dmc.Stack(
                                children=[
                                    dmc.Group(
                                        spacing="2px",
                                        position="apart",
                                        children=[
                                            dmc.Text(
                                                self.sender,
                                                style={
                                                    "fontWeight": "bold",
                                                }
                                            ),
                                            html.Button(
                                                id={"type": "playTextToVoice", "index": self.uuid},
                                                className="smallButtonMessageClass",
                                                children=[
                                                    DashIconify(
                                                        className="smallIcon",
                                                        icon="mdi:speak",
                                                        color="#A6808C",
                                                        width=15,
                                                        height=15
                                                    ),
                                                    html.Div(
                                                        className="smallText",
                                                        children="Read",
                                                    )
                                                ],
                                            )
                                        ],
                                    ),
                                    html.Div(
                                        id={"type": "messageText", "index": self.uuid},
                                        children=self.text,
                                    ),
                                    html.Div(
                                        children=timestamp,
                                        style={
                                            "fontSize": "10px",
                                            "color": utils.constants.custom_colors['mountbatten_pink'],
                                            "display": "flex",
                                            "justifyContent": "flex-end",
                                            "marginRight": "5px",
                                        }
                                    )
                                ],
                                spacing="5px",
                                style={
                                    "paddingTop": "8px",
                                    "width": "90%",
                                    "flex": 1,
                                }
                            )
                        ],
                    )
                ])]
        )
        return self.component

    def get_message_user(self, timestamp):
        return self.get_message(timestamp)

    def get_message_bot(self, timestamp):
        self.component = self.component = html.Div(
            className="messageContainerBot",
            style={
                "width": "100%",
                "borderRadius": "5px",
                "marginTop": 5,
            },
            children=[dmc.Paper(
                style={
                    "padding": "10px 10px",
                    "backgroundColor": "transparent",
                },
                children=[
                    dmc.Group(
                        align="start",
                        children=[
                            dmc.Avatar(
                                src=self.src_image,
                                alt="Avatar",
                                radius="xl",
                                size="md",
                                style={
                                    "width": "10",
                                    "backgroundColor": "white",
                                }
                            ),
                            dmc.Stack(
                                children=[
                                    html.Div(
                                        id={"type": "notificationsContainer", "index": self.uuid},
                                        className="notificationsContainerClass",
                                    ),
                                    dmc.Group(
                                        spacing="2px",
                                        position="apart",
                                        children=[
                                            dmc.Text(
                                                self.sender,
                                                style={
                                                    "fontWeight": "bold",
                                                }
                                            ),
                                            html.Button(
                                                id={"type": "playTextToVoice", "index": self.uuid},
                                                className="smallButtonMessageClass",
                                                children=[
                                                    DashIconify(
                                                        className="smallIcon",
                                                        icon="mdi:speak",
                                                        color="#A6808C",
                                                        width=15,
                                                        height=15
                                                    ),
                                                    html.Div(
                                                        className="smallText",
                                                        children="Read",
                                                    )
                                                ],
                                            )
                                        ],
                                    ),
                                    dcc.Markdown(
                                        id={"type": "messageText", "index": self.uuid},
                                        children=self.text,
                                    ),
                                    html.Div(
                                        children=timestamp,
                                        style={
                                            "fontSize": "10px",
                                            "color": utils.constants.custom_colors['mountbatten_pink'],
                                            "display": "flex",
                                            "justifyContent": "flex-end",
                                            "marginRight": "5px",
                                        }
                                    )
                                ],
                                spacing="5px",
                                style={
                                    "paddingTop": "8px",
                                    "width": "90%",
                                    "flex": 1,
                                }

                            )
                        ],
                    )
                ])]
        )
        return self.component
