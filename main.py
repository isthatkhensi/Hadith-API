import json
import os
from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def reverse_arabic_text(text):
    return text[::-1]

@app.get("/api/collections", response_class=HTMLResponse)
async def show_collections(request: Request):
    collection_data = []
    collection_dir = os.listdir("collections")
    for filename in collection_dir:
        if filename.endswith(".json"):
            with open(os.path.join("collections", filename), "r") as f:
                collection_data.append(json.load(f))
    return templates.TemplateResponse("collections.html", {"request": request, "collections": collection_data})

@app.get("/api/collections/{collection_id}")
async def get_collection(collection_id: str):
    filename = f"{collection_id}.json"
    filepath = os.path.join("collections", filename)
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return json.loads(f.read())
    else:
        return {"error": f"Collection {collection_id} not found"}
    

def get_collection_data(collection_id):
    collection_path = f"./hadiths/{collection_id}"
    if not os.path.exists(collection_path):
        return None

    collection_data = []
    for filename in os.listdir(collection_path):
        if filename.endswith(".json"):
            file_path = os.path.join(collection_path, filename)
            try:
                data = read_json_file(file_path)
                if isinstance(data, list) and len(data) > 0:
                    for item in data:
                        for key, value in item.items():
                            if key == "hadith_arabic":
                                item[key] = reverse_arabic_text(value)
                        collection_data.append(item)
            except Exception as e:
                print(f"Error reading file: {file_path}\n{e}")

    return collection_data


@app.get("/api/hadiths/{collection_id}")
def get_hadiths(collection_id: str):
    collection_data = get_collection_data(collection_id)
    if collection_data is None:
        return {"message": f"Collection '{collection_id}' not found."}
    return collection_data

@app.get("/api/hadiths/{collection_id}/{book_id}")
def get_hadith(collection_id: str, book_id: str):
    collection_path = f"./hadiths/{collection_id}"
    if not os.path.exists(collection_path):
        return {"message": f"Collection '{collection_id}' not found."}

    file_path = os.path.join(collection_path, f"{book_id}.json")
    if not os.path.isfile(file_path):
        return {"message": f"Book '{book_id}' not found in collection '{collection_id}'."}

    try:
        data = read_json_file(file_path)
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                for key, value in item.items():
                    if key == "hadith_arabic":
                        item[key] = reverse_arabic_text(value)
        return data
    except Exception as e:
        return {"message": f"Error reading file: {file_path}\n{e}"}

# Testing JSON
@app.get("/api/hadiths/{collection_id}/test")
def test_hadiths(collection_id: str):
    collection_data = get_collection_data(collection_id)
    if collection_data is None:
        return {"message": f"Collection '{collection_id}' not found."}

    # Print the first five dictionaries
    for i, item in enumerate(collection_data[:5], 1):
        print(f"{item}")

    return {"message": "Test completed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
