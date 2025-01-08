from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from rich.console import Console
from rich.table import Table
from rich import print
import time
import warnings

warnings.filterwarnings("ignore")

DG_KEY = "YOUR DEEPGRAM KEY"
deepgram = DeepgramClient(DG_KEY)

##############################
options = PrerecordedOptions(
    model="nova-2",
    language="en",
    smart_format=True,
    detect_language=True
)
##############################

def transcribe_wav_file(full_path_wav):
    try:
        with open(full_path_wav, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        send = time.time()
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options, timeout=1000).to_dict()
        latency = time.time() - send

        return response, latency

    except Exception as e:
        print(e)

def main(filename):
    console = Console()
    table = Table()

    response, latency = transcribe_wav_file(filename)
    print(f"DG call Latency: {latency*1000:.2f} ms")

    transript = response['results']['channels'][0]['alternatives'][0]['transcript']
    words = response['results']['channels'][0]['alternatives'][0]['words']

    table.add_column("Word", justify="left", style="cyan", no_wrap=True)
    table.add_column("Start", justify="right", style="magenta")
    table.add_column("End", justify="right", style="green")

    for word in words:
        table.add_row(word['word'], str(f"{word['start']:.2f}"), str(f"{word['end']:.2f}"))

    console.print(table)

if __name__ == "__main__":
    main('test.wav')
    
