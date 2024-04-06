import json
import os
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def reverse_arabic_text(text):
    return text[::-1]
@app.get("/")
def root():
    return {"message": "Welcome to the Sunnah Hadith API!"}

def get_collection_data(collection_id, book_id=None):
    collection_path = f"./hadiths/{collection_id}"
    if not os.path.exists(collection_path):
        return None

    if book_id:
        file_path = os.path.join(collection_path, f"{book_id}.json")
        if not os.path.isfile(file_path):
            return None
        try:
            data = read_json_file(file_path)
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    for key, value in item.items():
                        if key == "hadith_arabic":
                            item[key] = reverse_arabic_text(value)
            return data
        except Exception as e:
            print(f"Error reading file: {file_path}\n{e}")
            return None
    else:
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
                        collection_data.extend(data)
                except Exception as e:
                    print(f"Error reading file: {file_path}\n{e}")
        return collection_data

@app.get("/collection/{collection_id}")
async def get_collection_hadiths(collection_id: str):
    """
    Retrieve Hadiths from a specific collection by its ID.

    - `collection_id`: ID of the collection to retrieve Hadiths from.
    Retrieve a hadith collection's details. 
    Available collections include:
        - Sunan Abi Dawud (id: abudawud)
        - Sahih Al-Bukhari (id: bukhari)
        - Sunan Ibn Majah (id: ibnmajah)
        - Muslim (id: muslim)
        - Nasai (id: nasai)
        - Jami` at-Tirmidhi (id: tirmidhi)
    - Returns a JSON response with all the information regarding the hadith book.
    - Raises HTTP 404 if collection or collection file is not found.
    """
    filename = f"{collection_id}.json"
    filepath = os.path.join("collections", filename)
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_id}' not found.")
    
    
@app.get("/hadiths/{collection_id}")
def get_hadiths(collection_id: str):
    """
    Retrieve all hadiths from every book in collection by its ID.

    - `collection_id`: ID of the collection to retrieve details for.
    - Returns JSON response with all hadiths of the specified collection.
    - Raises HTTP 404 if collection is not found.

    """
    collection_data = get_collection_data(collection_id)
    if collection_data is None:
        return {"message": f"Collection '{collection_id}' not found."}
    return collection_data

@app.get("/hadiths/{collection_id}/{book_id}")
def get_hadith(collection_id: str, book_id: str):
    """
    Retrieve all hadiths from specified book in specified collection by their ID.

    - `collection_id`: ID of the collection to retrieve details for.
    - Pro-tip: Use `/collection/collection_id` to locate ID for specific book
    - Returns JSON response with all hadiths of the specified collection.
    - Raises HTTP 404 if collection is not found.
    
    """
    hadiths_data = get_collection_data(collection_id, book_id)
    if hadiths_data is None:
        return {"message": f"Book '{book_id}' not found in collection '{collection_id}'."}
    return hadiths_data

# Testing JSON
@app.get("/hadiths/{collection_id}/test")
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
