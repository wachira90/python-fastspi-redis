#!python
from fastapi import FastAPI, HTTPException
import redis
import json

app = FastAPI()

# Initialize the Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Create data in JSON format
def create_data(key, data):
    redis_client.set(key, json.dumps(data))
    return data

# Get data from Redis by key
def get_data(key):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Update data in JSON format
def update_data(key, data):
    if get_data(key):
        redis_client.set(key, json.dumps(data))
        return data
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Delete data by key
def delete_data(key):
    if get_data(key):
        redis_client.delete(key)
        return {"message": "Item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/create/{key}")
async def create_item(key: str, data: dict):
    return create_data(key, data)

@app.get("/read/{key}")
async def read_item(key: str):
    return get_data(key)

@app.put("/update/{key}")
async def update_item(key: str, data: dict):
    return update_data(key, data)

@app.delete("/delete/{key}")
async def delete_item(key: str):
    return delete_data(key)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
