from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.db.deps import get_db
from src.exceptions import StoryException
from src.models.articles import DBArticle
from src.schemas.article_schema import ArticleDisplay, ArticleBase
from auth.oauth2 import oauth2_scheme, get_current_user
from src.schemas.user_schema import UserBase

articles_router = APIRouter(prefix="/article", tags=["article"])


@articles_router.post(
    "/create",
    response_model=ArticleDisplay,
    status_code=status.HTTP_201_CREATED,
    response_description="Create a new article",
)
def create_article(
    request: ArticleBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    if request.content.startswith("Once upon a time"):
        raise StoryException("No stories please")
    new_article = DBArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@articles_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_article(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    article = db.query(DBArticle).filter(DBArticle.id == id).first()
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return {"data": article, "current_user": current_user}
