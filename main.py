from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def get_home():
    return {"mess": "Hello World"}

@app.post("/createpost")
#def craete_post(payload: dict = Body(...)):
def create_post(new_post: Post):
    print(new_post)
    print(new_post.dict())
    #return {"new post": f"title: {payload['title']} content: {payload['content']}"}
    return {"data": "new post"}