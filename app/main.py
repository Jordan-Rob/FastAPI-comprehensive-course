from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#### connect to DB
# 1. No ORM
try:
    connection = psycopg2.connect(host='localhost', port=5432, database='fastAPI', user='postgres', password="myPassword", cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connecting to Database failed")
    print(f"Error: {error}")

cursor.execute("""CREATE TABLE IF NOT EXISTS posts (id serial PRIMARY KEY, title VARCHAR ( 255 ) NOT NULL, content VARCHAR NOT NULL, published BOOLEAN NOT NULL, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL) """)
#cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, ("post1", "post1content", True))

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
    {"title":"title of post 2", "content":"content of post 2", "id":2}
]


@app.get("/")
def get_home():
    return {"mess": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    #print(type(id))
    #post_id = int(id)
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    post = cursor.fetchone()
    if post:
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

    """
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 10000)
    print(post_dict["id"])
    print(type(post_dict["id"]))
    my_posts.append(post_dict)
    """
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    (new_post.title, new_post.content, new_post.published))

    post = cursor.fetchone()
    connection.commit()
    #return {"new post": f"title: {payload['title']} content: {payload['content']}"}
    return {"data": post}


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