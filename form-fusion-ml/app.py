from fastapi import FastAPI, Body, Response
from helpers import mp_script, get_message

app = FastAPI()

@app.post("/formfusion")
async def process(response: Response, numbers: dict[str, list[int]] = Body(...)):
    mp_script(numbers["numbers"])
    return_message = get_message(numbers["numbers"])
    response.status_code = 200
    return {"msg": return_message}