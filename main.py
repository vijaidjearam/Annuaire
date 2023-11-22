
import arrr
from pyscript import document


def submit(event):
    lang = document.querySelector("#Service")
    language = lang.value
    output_div = document.querySelector("#output")
    output_div.innerText = language

