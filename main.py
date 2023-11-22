
import arrr
from pyscript import document


def submit(event):
    lang = document.querySelector("#lang")
    language = lang.value
    output_div = document.querySelector("#output1")
    output_div.innerText = language

