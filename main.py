from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
app = FastAPI(title="My FastAPI App", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE: dict[str,dict] = {}

class PostCreate(BaseModel):
    username: str = Field(title="Username", min_length=3, max_length=100)
    password: str = Field(title="Password", min_length=3, max_length=100)
    email: str = Field(title="Email", min_length=3, max_length=100)

class PostResponse(PostCreate):
    post_id:str
    create_at:str

@app.get("/")
async def root():
    return {"message": "Hello this is first Sardor's API! ",
            'date': str(datetime.now()),
            'author': 'mr_bekmuratov',}

@app.get("/posts/{post_id}")
async def get_post(post_id: str):
    dic = {}
    for i in DATABASE:
        if DATABASE[i]["post_id"] == post_id:
            dic = DATABASE[i]
            return dic
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get("/posts", response_model= list[PostResponse])
async def get_all_posts():
    return list(DATABASE.values())


@app.post('/posts', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def post_create(post: PostCreate):
    post_id = str(uuid4())
    new_post = post.dict()
    date = str(datetime.now())
    date = date[:19].replace(' ', '-')
    new_post["post_id"] = post_id
    new_post["created_at"] = date
    DATABASE[post_id] = new_post
    return new_post




