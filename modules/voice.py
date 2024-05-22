import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from dash_recording_components import AudioRecorder

import utils.constants as c


class Voice:
    def __init__(self):
        self.voice_layout = html.Div(
            id="voiceLayout",
            className="voiceLayout",
            children=[
                html.Div(
                    id="notificationContainerMic",
                    className="notificationsContainerClass",
                ),
                dcc.Markdown(
                    "### Voice Recorder",
                    className="voiceRecorderHeader"
                ),
                html.Button(
                    id="recordButton",
                    className="recordButton",
                    children=[
                        c.voice_micro,
                    ]),
                html.Div(
                    id="audioTranscribeOutput",
                    className="audioTranscribeOutput",
                    children=[],
                ),
                html.Div(id="dummyOutput", style={"display": "none"}),
                html.Div(
                    id="audioRecorderDiv",
                    children=[
                        AudioRecorder(id="audioRecorder"),
                    ]
                ),
                dmc.Group(
                    className="modalGroup",
                    spacing=10,
                    style={
                        "margin": "0 0 0 0",
                        "padding": "0 0 0 0",
                    },
                    children=[
                        dmc.Button(
                            children=[
                                dmc.Stack(
                                    spacing="0px",
                                    children=[
                                        dmc.Text(
                                            "Submit",
                                            className="mainTextButton"
                                        ),
                                        dmc.Text(
                                            "Transfer transcription",
                                            className="subTextButton"
                                        ),
                                    ]
                                )
                            ],
                            leftIcon=DashIconify(icon="carbon:arrow-down", width=20),
                            id="submitTranscriptionButton",
                            className="modalButton",
                        ),
                        dmc.Button(
                            children=[
                                dmc.Stack(
                                    spacing="0px",
                                    children=[
                                        dmc.Text(
                                            "Close",
                                            className="mainTextButton"
                                        ),
                                        dmc.Text(
                                            "Discard transcription",
                                            className="subTextButton"
                                        ),
                                    ]
                                )
                            ],
                            leftIcon=DashIconify(icon="carbon:close-large", width=20),
                            id="closeTranscriptionButton",
                            className="modalButton",
                        )],
                ),
            ])

    def get_voice_recorder(self):
        return self.voice_layout
