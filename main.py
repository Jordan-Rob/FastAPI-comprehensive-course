from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
    {"title":"title of post 2", "content":"content of post 2", "id":2}
]


@app.get("/")
def get_home():
    return {"mess": "Hello World"}


@app.get("/posts")
def get_posts():
    return {'data': my_posts}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    #print(type(id))
    #post_id = int(id)
    for post in my_posts:
        if post["id"] == id:
            return {"data": post}
        else:
            #response.status_code = status.HTTP_404_NOT_FOUND
            #return {"error":f"post with id:{id} does not exist!"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")


@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def craete_post(payload: dict = Body(...)):
def create_post(new_post: Post):
    #print(new_post)
    #print(new_post.dict())
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 10000)
    print(post_dict["id"])
    print(type(post_dict["id"]))
    my_posts.append(post_dict)
    #return {"new post": f"title: {payload['title']} content: {payload['content']}"}
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    updated_post_dict = updated_post.dict()
    
    for post in my_posts:
        if post["id"] == id:
            post_index = my_posts.index(post, 0, len(my_posts))
            my_posts[post_index] = updated_post_dict
            return {"data":f"post {post['title']} updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")