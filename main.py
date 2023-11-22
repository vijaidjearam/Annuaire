
import arrr
from pyscript import document


def submit(event):
    service = document.querySelector("#Service")
    output_div = document.querySelector("#output")
    output_div.innerText = service.value

