import io
import queue
import tempfile
import time
import uuid

import dash_mantine_components as dmc
import numpy as np
import simpleaudio as sau
import soundfile as sf
from dash import Dash, Input, Output, State, Patch, no_update, ctx, dcc, MATCH, ALL
from dash_iconify import DashIconify
from dash_recording_components import AudioRecorder
from wit import Wit

import logic_llm.manager_llm as manager_llm
import logic_todo.todo_cmd as todo_cmd
import logic_voice.wit_ai as wit_ai
import modules.chat as chat
import modules.layout as layout
import modules.message as msg
import utils.constants as c
from logic_weather import weather_api
from modules import task, task_list

# voice recording and transcribing
audio_samples = []
client = Wit(wit_ai.wit_api_token)

# api response queue
api_response_queue = queue.Queue()
todo_update_queue = queue.Queue()

# for api response flags and status
api_response = manager_llm.ApiResponse()

# modules
layout = layout.Layout(footer_height=30, header_height=50, custom_colors=c.custom_colors)
chat = chat.Chat(
    custom_colors=c.custom_colors,
    style={
        "height": f"calc(100vh - {c.header_height + c.footer_height + 2 * c.small_margin}px)",
        "marginTop": c.header_height + c.small_margin,
        "marginBottom": c.footer_height + c.small_margin,
        "padding": "0 0 0 0"
    }
)
todo = task_list.Todo(
    header_height=c.header_height,
    footer_height=c.footer_height,
    custom_colors=c.custom_colors,
    small_margin=c.small_margin
)

# dash app layout
app = Dash(__name__)
app.title = "Aeon Task Mind"
app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={
        "colorScheme": "dark",
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "dark",
        "modules": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        }
    },
    children=dmc.NotificationsProvider(
        position="top-center",
        zIndex=10002,
        autoClose=3000,
        children=[
            dcc.Store(id="waitForNewData", data=0),
            dcc.Store(
                id="locationData",
                data={
                    "name": "Kaiserslautern,DE",
                    "lon": "49.4401",
                    "lat": "7.7491"
                }
            ),
            dcc.Store(
                id="forceRagWeatherIncorporate",
                data=False
            ),
            layout.get_header(),
            layout.get_footer(),
            chat.get_chat(),
            todo.get_aside()
        ]
    )
)


def get_interval(_uuid):
    return dcc.Interval(
        id={"type": "intervalTrigger", "index": _uuid},
        interval=1000,
        n_intervals=0,
    )


def start_api_call(value: str, data: dict, enable_check: bool):
    api_response.done = False
    api_response.request_done = False
    manager_llm.start_thread(
        _api_response=api_response,
        prompt=value,
        location_data=data,
        enable_check=enable_check,
        api_response_queue=api_response_queue,
        todo_update_queue=todo_update_queue
    )


@app.callback(
    Output("scrollbarDiv", "children"),
    Output("messageInput", "value", allow_duplicate=True),
    Output("messageInput", "disabled"),
    Output("sendButton", "disabled"),
    Output("recordVoiceButton", "disabled"),
    Output("waitForNewData", "data"),
    Input('sendButton', 'n_clicks'),
    Input('messageInput', 'n_submit'),
    State("messageInput", "value"),
    State("locationData", "data"),
    State("forceRagWeatherIncorporate", "data"),
    prevent_initial_call=True,
)
def update_chat(n_clicks, n_submit, value, data, check):
    if value:
        if (ctx.triggered_id == 'sendButton'
                or n_clicks is not None
                or ctx.triggered_id == 'messageInput'
                or n_submit is not None):
            start_api_call(value, data, check)
            return patch_chat(value)
    return no_update, no_update, False, False, False, no_update


def patch_chat(value):
    patched_children = Patch()
    uuid_message = str(uuid.uuid4())
    user_message = msg.Message("You", value, is_you=True, uuid_message=None)
    bot_message = msg.Message("Bot", "⚪", is_you=False, uuid_message=uuid_message)
    patched_children.append(user_message.get_message(time.strftime('%H:%M:%S')))
    patched_children.append(bot_message.get_message_bot(time.strftime('%H:%M:%S')))
    patched_children.append(get_interval(uuid_message))
    return patched_children, "", True, True, True, 1


@app.callback(
    Output({'type': 'messageText', 'index': MATCH}, 'children'),
    Output({'type': 'intervalTrigger', 'index': MATCH}, 'disabled'),
    Input({'type': 'intervalTrigger', 'index': MATCH}, 'n_intervals'),
    State({'type': 'messageText', 'index': MATCH}, 'children'),
    prevent_initial_call=True,
)
def update_message(n, children):
    loading_token = "⚪"
    if not api_response.done:
        if api_response_queue.empty() and api_response.request_done:
            api_response.done = True
            children = children.replace(loading_token, "")
            print(" ☝️ ", len(children), "~", api_response.char_length)
            return children, True
        else:
            if not api_response_queue.empty():
                collect_token = ""
                while not api_response_queue.empty():
                    collect_token += api_response_queue.get()
                    api_response_queue.task_done()
                existing_text = children.replace(loading_token, "")
                new_children = existing_text + collect_token + loading_token
                return new_children, False
            else:
                return no_update, no_update
    else:
        children = children.replace(loading_token, "")
        print(" ☝️ ", len(children), "~", api_response.char_length)
        return children, True


@app.callback(
    Output("messageInput", "disabled", allow_duplicate=True),
    Output("sendButton", "disabled", allow_duplicate=True),
    Output("recordVoiceButton", "disabled", allow_duplicate=True),
    Input({"type": "intervalTrigger", "index": ALL}, "disabled"),
    prevent_initial_call=True,
)
def enable_input_fields_for_user(values):
    return (False, False, False) if all(values) else (True, True, True)


@app.callback(
    Output({'type': 'playTextToVoice', 'index': MATCH}, 'disabled'),
    Output({'type': 'notificationsContainer', 'index': MATCH}, 'children'),
    Input({'type': 'playTextToVoice', 'index': MATCH}, 'n_clicks'),
    State({'type': 'messageText', 'index': MATCH}, 'children'),
    prevent_initial_call=True,
)
def play_sound_in_user_message(n_clicks, value):
    if n_clicks:
        response = wit_ai.synthesize_speech_from_text(value)
        error_not = dmc.Notification(
            id="errorNotification",
            color="#565264",
            title="There was an error synthesizing message text.",
            action="show",
            message="Please try again.",
            icon=DashIconify(icon="mdi:alert-circle", color="#e40d0d"),
        )
        success_not = dmc.Notification(
            id="successNotification",
            color="#565264",
            title="Message text synthesized successfully.",
            action="show",
            message="You should have heard the message.",
            icon=DashIconify(icon="mdi:check-circle", color="#08ea08"),
        )
        if response.status_code == 200:
            print(" 🎙️ ", "Playing sound for message.")
            try:
                wav_bytes = response.content
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                    audio_content = wav_bytes
                    temp_audio.write(audio_content)
                    temp_audio.flush()
                    wave_object = sau.WaveObject.from_wave_file(temp_audio.name)
                    play_object = wave_object.play()
                    play_object.wait_done()
                    return False, success_not
            except Exception as e:
                print(e)
                print(" 🎙️ ", "Error playing sound.")
                return False, error_not
        else:
            print(" 🎙️ ", "Error synthesizing message text. " + str(response.status_code))
            return False, error_not


def patch_todo_list():
    patch_list = []
    for position, title, priority, context, deadline in todo_cmd.compile_todo_list(todo_cmd.get_flat_todo_list()):
        patch_list.append(
            task.get_task(
                uuid=str(uuid.uuid4()),
                position=position,
                title=title,
                priority=priority,
                context=context,
                deadline=deadline
            )
        )
    return patch_list


@app.callback(
    Output("todoStack", "children"),
    Output("waitForNewDataTrigger", "disabled"),
    Output("notificationContainerTodoList", "children"),
    Input("waitForNewData", "data"),
    Input("waitForNewDataTrigger", "n_intervals"),
)
def update_todo_list(n_wait, _):
    if n_wait == 0:
        print(" 🔃 ", "Initialising todo list...")
        return patch_todo_list(), True, no_update
    if n_wait > 0:
        if not todo_update_queue.empty():
            try:
                update_not = dmc.Notification(
                    id="updateNotification",
                    color="#565264",
                    title="Todo list updated.",
                    action="show",
                    message="You should see the changes in the list on the left.",
                    icon=DashIconify(icon="mdi:check-circle", color="#08ea08"),
                )
                print(" 🔃 ", "Updating todo list...")
                return patch_todo_list(), True, update_not
            finally:
                todo_update_queue.get()
                todo_update_queue.task_done()
        else:
            return no_update, False, no_update
    return no_update, True, no_update


@app.callback(
    Output("aboutModal", "opened"),
    Output("audioRecorderDiv", "children"),
    Input("aboutButton", "n_clicks"),
    State("aboutModal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    if n_clicks:
        if opened:
            return False, no_update
        else:
            patchedAudioRecorder = Patch()
            patchedAudioRecorder.append(AudioRecorder(id="audioRecorder"))
            return True, patchedAudioRecorder
    return not opened if n_clicks else opened


@app.callback(
    Output("tourModal", "opened"),
    Input("tourButton", "n_clicks"),
    State("tourModal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened if n_clicks else opened


@app.callback(
    Output("voiceModal", "opened", allow_duplicate=True),
    Input("recordVoiceButton", "n_clicks"),
    State("voiceModal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened if n_clicks else opened


@app.callback(
    [
        Output("audioRecorder", "recording", allow_duplicate=True),
        Output("recordButton", "children", allow_duplicate=True),
        Output("audioTranscribeOutput", "children"),
        Output("submitTranscriptionButton", "disabled"),
        Output("notificationContainerMic", "children")],
    [
        Input("recordButton", "n_clicks"),
        State("audioRecorder", "recording")],
    prevent_initial_call=True
)
def control_recording(_, recording):
    global audio_samples
    no_mic_not = dmc.Notification(
        id="noMicNotification",
        color="#565264",
        title="No microphone detected.",
        action="show",
        message="Please connect a microphone and refresh.",
        icon=DashIconify(icon="mdi:alert-circle", color="#e40d0d"),
    )
    if not recording:
        audio_samples.clear()
        return True, DashIconify(icon="system-uicons:record", width=30, height=30), "Recording...", True, no_update
    else:
        try:
            if audio_samples:
                audio_array = np.array(audio_samples)
                with (io.BytesIO() as wav_buffer):
                    sf.write(wav_buffer, audio_array, 16000, format="WAV")
                    wav_bytes = wav_buffer.getvalue()
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                        audio_content = wav_bytes
                        temp_audio.write(audio_content)
                        temp_audio.flush()
                        with open(temp_audio.name, 'rb') as f:
                            res = client.speech(f, {'Content-Type': 'audio/wav'})
                            print(" 🎙️ ", "Synthesized: " + str(res["text"]))
                            return False, c.voice_micro, str(res["text"]), False, no_update
        except Exception as e:
            print(e)
            return False, c.voice_micro, "Error recording audio.", False, no_update


@app.callback(
    Output("dummyOutput", "children"),
    Input("audioRecorder", "audio"),
    prevent_initial_call=True
)
def update_audio(audio):
    global audio_samples
    if audio is not None:
        audio_samples += list(audio.values())
    return ""


@app.callback(
    Output("audioRecorder", "recording", allow_duplicate=True),
    Output("messageInput", "value", allow_duplicate=True),
    Output("voiceModal", "opened", allow_duplicate=True),
    Output("audioTranscribeOutput", "children", allow_duplicate=True),
    Output("recordButton", "children", allow_duplicate=True),
    Input("submitTranscriptionButton", "n_clicks"),
    State("audioTranscribeOutput", "children"),
    prevent_initial_call=True
)
def update_input_field(n_clicks, children):
    if n_clicks:
        if not children:
            return False, no_update, False, "", c.voice_micro
        else:
            return False, str(children), False, "", c.voice_micro
    else:
        return no_update, no_update, no_update, no_update, no_update


@app.callback(
    Output("audioRecorder", "recording", allow_duplicate=True),
    Output("voiceModal", "opened", allow_duplicate=True),
    Output("audioTranscribeOutput", "children", allow_duplicate=True),
    Output("recordButton", "children", allow_duplicate=True),
    Input("closeTranscriptionButton", "n_clicks"),
    State("audioRecorder", "recording"),
    prevent_initial_call=True
)
def close_voice_modal(n_clicks, recording):
    if recording is not None:
        if n_clicks > 0:
            return False, False, "", c.voice_micro
        else:
            return False, no_update, no_update, no_update
    else:
        return no_update, False, "", c.voice_micro


@app.callback(
    Output("notificationContainerLocation", "children"),
    Output("locationData", "data"),
    Input("locationSubmit", "n_clicks"),
    State("locationInput", "value"),
    State("locationData", "data"),
    prevent_initial_call=True
)
def save_location_data(n_clicks, value, data):
    success_not = dmc.Notification(
        id="successNotification",
        color="#565264",
        title="Location was updated sucessfully.",
        action="show",
        message="New weather forecast will be fetched next time.",
        icon=DashIconify(icon="mdi:check-circle", color="#08ea08"),
    )
    error_not = dmc.Notification(
        id="errorNotification",
        color="#565264",
        title="Error updating location.",
        action="show",
        message="Please try again.",
        icon=DashIconify(icon="mdi:alert-circle", color="#e40d0d"),
    )
    if n_clicks and value != "":
        try:
            if value == data["name"]:
                return success_not, no_update
            else:
                lon, lat = weather_api.fetch_geocode(value, 'DE', 1)
                return success_not, {"name": value, "lon": str(lon), "lat": str(lat)}
        except Exception as e:
            print(" 🌍 ", "Error updating location. " + str(e))
            return error_not, no_update
    else:
        return no_update, no_update


@app.callback(
    Output("forceRagWeatherIncorporate", "data"),
    Input("locationSwitch", "checked"),
    prevent_initial_call=True
)
def force_rag_weather(checked):
    return checked if checked else False


if __name__ == '__main__':
    app.run_server(debug=True)
