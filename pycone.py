import requests
import pynecone as pc
import base64


def api_call(text):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    response = requests.get(f'https://cataas.com/cat/says/{text}', headers=headers)
    base64_image = base64.b64encode(response.content).decode()
    return f"data:image/jpeg;base64,{base64_image}"
    

class State(pc.State):
    text: str = "cat"
    photo: str = ""
    image_processing = False
    image_made = False

    def process_image(self):
        self.image_made = False
        self.image_processing = True

    def get_cat(self):
        try: 
            self.photo = api_call(self.text)
            self.image_processing = False
            self.image_made = True
        except:
            self.image_processing = False
            return pc.window_alert("Error with OpenAI Execution.")
        

def index():
    return pc.container(
        pc.vstack(
            pc.heading("Random Cats", margin_top="90px"),
            pc.input(
                on_blur=State.set_text,
                placeholder="Add a text...",
                bg="white",
            ),
            pc.button("Start The Magic", on_click=[State.process_image, State.get_cat]),
            pc.link("TeaOverFlow Channel", href="https://t.me/TeaOverFlow", color="rgb(107,99,246)"),
            pc.divider(),
            pc.cond(
                State.image_processing,
                pc.spinner(color="black", thickness=5, speed="0.8s", size="xl"),
                pc.cond(
                    State.image_made,
                    pc.image(src=State.photo, height="25em", width="25em", border_radius="15px",),
                    pc.badge("No Photo Loaded", variant="subtle", color_scheme="red"),
                ),
            ),
        )
    )
    

app = pc.App(state=State)
app.add_page(index, title="Random Cats")
app.compile()