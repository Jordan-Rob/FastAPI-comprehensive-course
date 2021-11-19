from sqlalchemy.orm import Session
from fastapi import FastAPI,  Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor

from .database import engine, get_db
from . import models, config
from .routers import post, user, vote

print(config.settings.database_username)

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




app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)



#### ORM TEST Route
@app.get("/sql")
def orm_test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
def get_home():
    return {"mess": "Hello World"}



