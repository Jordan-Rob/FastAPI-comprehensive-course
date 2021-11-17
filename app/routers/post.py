from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    ## No ORM ##
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    ## ORM ##
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#def craete_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
get_current_user: int = Depends(oauth2.get_current_user)):
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.PostResponse)
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