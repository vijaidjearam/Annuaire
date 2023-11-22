
import arrr
from pyscript import document


def translate_english(event):
    input_text = document.querySelector("#english")
    english = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = arrr.translate(english)
    lang = document.querySelector("#lang")
    language = lang.value
    output_div = document.querySelector("#output1")
    output_div.innerText = arrr.translate(language)

