import dash_mantine_components as dmc

from dash import html


def get_task(uuid: str, position: str, title: str, deadline: str, priority: str, context: str):
    return html.Div(
        id="task" + uuid,
        className="task",
        children=[
            html.Div(
                className="taskPosition",
                children=[position]
            ),
            html.Div(
                className="taskContent",
                children=[
                    html.Div(
                        className="taskHeader",
                        children=[title]
                    ),
                    dmc.Badge(
                        className="taskBadge",
                        children=str("💀 " + deadline)
                    ),
                    dmc.Badge(
                        className="taskBadge",
                        children="⭐ " + priority
                    ),
                    dmc.Badge(
                        className="taskBadge",
                        children="📃 " + context
                    )]
            )
        ])


def get_title(title: str):
    return html.Div(
        className="taskTitle",
        children=title
    )
