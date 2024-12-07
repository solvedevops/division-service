from fastapi import FastAPI


def division(firstNumber, secondNumber):
    return (firstNumber / secondNumber)


app = FastAPI()

@app.get("/")
async def pickArgs(first_number: int = 0, second_number: int = 0):
    return division(first_number, second_number)
