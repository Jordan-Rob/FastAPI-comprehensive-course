from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


@router.get("/", )
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, 
search: Optional[str] = ""):
    ## No ORM ##
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    ## ORM ##
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts


@router.get("/{id}", )
def get_post(id: int, db: Session = Depends(get_db)):
    #print(type(id))
    #post_id = int(id)

    ## NO ORM ##
    #cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    #post = cursor.fetchone()

    ## ORM ##
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"error":f"post with id:{id} does not exist!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#def craete_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
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
    print(current_user.id)
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ## NO ORM ##
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #connection.commit()

    ## ORM ##
    post = db.query(models.Post).filter(models.Post.id == id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist!")   
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to carry out selected action")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    
    if pos.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to carry out selected action")

    queried_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return queried_post.first()