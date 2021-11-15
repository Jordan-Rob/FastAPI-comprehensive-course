from typing import Optional, List

from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

from .database import engine, get_db
from . import models, schemas, utils

#### connect to DB
#  ORM SQLALCHEMY
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#### connect to DB
#  No ORM
#try:
#    connection = psycopg2.connect(host='localhost', port=5432, database='fastAPI', user='postgres', password="myPassword", cursor_factory=RealDictCursor)
#    cursor = connection.cursor()
#    print("Database connection was successful")
#    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (id serial PRIMARY KEY, title VARCHAR ( 255 ) NOT NULL, content VARCHAR NOT NULL, published BOOLEAN NOT NULL, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL) """)
#    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, ("post1", "post1content", True))

#except Exception as error:
#    print("Connecting to Database failed")
#    print(f"Error: {error}")

"""
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
    {"title":"title of post 2", "content":"content of post 2", "id":2}
]
"""

#### ORM TEST Route
@app.get("/sql")
def orm_test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
def get_home():
    return {"mess": "Hello World"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    ## No ORM ##
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    ## ORM ##
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    #print(type(id))
    #post_id = int(id)

    ## NO ORM ##
    #cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    #post = cursor.fetchone()

    ## ORM ##
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"error":f"post with id:{id} does not exist!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#def craete_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #print(new_post)
    #print(new_post.dict())

    """
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 10000)
    print(post_dict["id"])
    print(type(post_dict["id"]))
    my_posts.append(post_dict)
    """
    ## No ORM ##
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #(new_post.title, new_post.content, new_post.published))

    #post = cursor.fetchone()
    #connection.commit()
    #return {"new post": f"title: {payload['title']} content: {payload['content']}"}
    
    
    ## ORM ##
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    ## NO ORM ##
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #connection.commit()

    ## ORM ##
    post = db.query(models.Post).filter(models.Post.id == id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")   
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    ## NO ORM ##
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #connection.commit()

    ## ORM ##
    queried_post = db.query(models.Post).filter(models.Post.id == id)
    pos = queried_post.first()
    if pos == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")
    
    queried_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return queried_post.first()


###### USERS #######
@app.get("/users/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user