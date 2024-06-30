from fastapi import FastAPI, Request
from pydantic import BaseModel
import pickle
import sqlite3

app = FastAPI()

model_path = "C:/Users/SHREY SHUKLA/mental helth/model.pkl"
vectorizer_path = "C:/Users/SHREY SHUKLA/mental helth/vectorizer.pkl"

with open(model_path, 'rb') as file:
    model = pickle.load(file)

with open(vectorizer_path, 'rb') as file:
    vectorizer = pickle.load(file)


class InputData(BaseModel):
    sentence: str


def fetch_resources(category):
    conn = sqlite3.connect('mental_health_resources.db')
    c = conn.cursor()
    c.execute("SELECT type, title, description, link FROM resources WHERE category=?", (category,))
    resources = c.fetchall()
    conn.close()
    return resources


@app.post("/predict")
def predict(data: InputData):
    input_sentence = [data.sentence]
    input_sentence_transformed = vectorizer.transform(input_sentence)
    prediction = model.predict(input_sentence_transformed)
    predicted_issue = prediction[0]
    resources = fetch_resources(predicted_issue)
    formatted_resources = [
        {
            "type": r[0],
            "title": r[1],
            "description": r[2],
            "link": r[3]
        }
        for r in resources
    ]
    return {"prediction": predicted_issue, "resources": formatted_resources}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        req = await request.json()
        query_text = req["queryResult"]["queryText"]
        input_data = InputData(sentence=query_text)
        prediction_result = predict(input_data)

        resources_text = "\n\n".join([
            f"Type: {resource['type']}\n"
            f"Title: {resource['title']}\n"
            f"Description: {resource['description']}\n"
            f"Link: {resource['link']}"
            for resource in prediction_result['resources']
        ])

        response = {
            "fulfillmentText": f"I see that you might be suffer about {prediction_result['prediction']}\n. Here are some descriptions and articles that could benefit your mental health.:\n\n{resources_text}"

        }
        return response
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception occurred: {str(e)}")

        # Return a default response in case of error
        return {
            "fulfillmentText": "An error occurred while processing your request."
        }


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
