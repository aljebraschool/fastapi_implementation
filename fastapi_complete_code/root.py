#import fastapi_project
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import Annotated, Literal, Optional, Any
from enum import Enum

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from starlette import status
from starlette.responses import HTMLResponse

#create fastapi_project app
app = FastAPI()


#use the fastapi_project decorator to create a root route or endpoint (e.g: https://aljebraschool.hashnode.dev)
@app.get("/") #define a path operation decorator
async def root(): #define the path operation function
    return {"message": "Hello world!!!"}

"""
Declaring path parameter or variable
"""

@app.get("/items_1/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}

"""
Declaring path parameter or variable with type
"""
@app.get("/items_2/{item_id}")
def read_item(item_id : int):
    return {"item_id": item_id}

"""
When you have to define dynamic and fixed path, make sure the fixed path is placed ahead of the the dynamic path
"""

@app.get("/users/me") #fixed path
def find_user():
    return {"user": "current user found!!!"}

@app.get("/users/{user_id}") #dynamic path which can take any user ID
def find_any_user(user_id : int):
    return {"user": user_id}


"""
if you want you use predifined parameters (variables) for you endpoint (route) use Enum to declare these parameters
"""

#define enum class that takes in string as fields
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    vgg = "vgg"

#now define your endpoint
@app.get("/model/{model_name}")
def get_model_name(model_name : ModelName):
    if model_name is ModelName.alexnet:
        return {"model name ": model_name, "message": "Dataset for image recognition"}
    if model_name == ModelName.resnet:
        return {"model name ": model_name, "message ": "It can be finetune for CNN"}
    return {"model name ": model_name, "message ": "finetuning is allowed!!!"}


"""
Creating a path parameter that contains a path (itself)
"""

@app.get("/files/file_path : path")
def read_file(file_path : str ):
    return {"file path ": file_path}

"""
Query parameter are parameters that are defined only in the function heading but not in the path heading
"""

fake_item_db = [{"item_name": "Foo" }, {"item_name ": "Ball"}]

@app.get("/item_3")
def read_item(skip : int = 0, limit : int = 10):
    return fake_item_db[skip : skip + limit]

"""
Optional parameters
"""

@app.get("/item_4/{item_id}")
def read_item(item_id : int, q : str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id" : item_id}

"""
Request body : used by the client (browser) to send data to  your API. 
It should be declared with a Pydantic class
"""

#define the request body class
class Item(BaseModel):
    name : str
    description : str | None = None #optional
    price : float
    tax : float | None = None #optional

#define your path operation
@app.post("/item_5")
def read_item(item : Item):
    item_dict = item.model_dump() #convert the pydantic class to dictionary
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

"""
Request body + Path Parameter
"""

@app.put("/item_6/{item_id}")
def create_item(item_id : int, item : Item):
    return {"item_id": item_id, **item.model_dump()}


"""
Request body + path + query parameters
"""

@app.put("/item_7/{item_id}")
def create_item(item_id : int, item : Item, q : str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

"""
Query parameters and String Validation

"""

#restricting the length of character of a query parameter
@app.get("/item_8")
def read_item(q : Annotated[str | None, Query(max_length=50)] = None):
    result = {"items" : [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result

"""
How to declare a value is required using Ellipsis (...)
"""

@app.get("/item_9")
def read_item(q : Annotated[str,Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "foo"}, {"item_id": "Zoo"}]}
    if q:
        results.update({"q": q})
    return results


"""
Query parameter list / multiple values
add more metadata to describe the query parameter
Also show that the parameter is now deprecated
"""

@app.get("/item_10")
def read_item(q : Annotated[list[str] | None, Query(
    title= "String parameter",
    description= "This is a string parameter",
    min_length=3,
    deprecated=True
)] = None):
    return {"q": q}

"""
Path Parameters and Numeric Validations
"""


@app.get("/item_11/{item_id}")
def read_item(item_id : Annotated[int | None, Path(title="the ID of the item of get", gt= 3, le=10), ],
              q: Annotated[str | None, Query(alias="item 11 route")] = None):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

"""
Declaring Query Parameters that are related using Pydantic model
"""

class FilterParams(BaseModel):
    limit : int = Field(100, gt=0, le=100)
    offset : int = Field(0, ge=0)
    order_by : Literal ["created_at", "updated_at"] = "created_at"
    tags : list[str] = Field(default_factory=list)

@app.get("item_12")
def read_item(filter_query : Annotated[FilterParams, Query()]):
    return filter_query

"""
Making Request Body Parameter Optional
"""

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None


@app.put("/item_12/{item_id}")
def read_item(
        item_id : Annotated[int, Path(title = "the ID of the item", ge=0, le=10)],
        q : str | None = None,
        item : Item | None = None #making request body optional
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

"""
Declaring Multiple Body Parameters
"""

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float

class User(BaseModel):
    email : EmailStr
    password : str

@app.put("/item_13/{item_id}")
def read_input(
        item_id : Annotated[int, Path(title="user ID", ge=0, gt=6)],
        item : Item,
        user : Annotated[User, Query()]
):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

"""
Using Body to add more body parameter
"""

@app.get("/item_14")
def read_item(
        item : Item,
        user : User,
        importance : Annotated[str, Body()]
):
    result = {"item": item, "user": user}
    if importance:
        result.update({"importance": importance})
    return result

"""
using Field to add more validation in Body parameter
"""

class Item(BaseModel):
    name : str
    description : str | None = Field(None, title= "using Field for body parameter")
    price : float = Field(gt=0, lt=50)
    tax : float | None = None

@app.get("/item_15")
def read_item(item : Annotated[Item, Body(embed=True)]):
    return {"item": item}

"""
Nexted model with valid URL
"""

class Image(BaseModel):
    name : str
    url : HttpUrl

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    image : Image | None = None

@app.get("/item_16")
def read_item(item : Item):
    return {"item": item}

"""
How to declare body parameter with example
"""

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

    model_config = {
        'json_schema_extra' : {
            "examples": [
                {
                    "name": "Ayo",
                    "description": "This contains an Item",
                    "price": 23.5,
                    "tax" : 2.5
                }
            ]
    }

    }

@app.get("/item_17/item_id")
def update_item(item_id : int, item : Item):
    return {"item_id": item_id, "item": item}

"""
This can also be implemented more compactly using Field
"""

class Item(BaseModel):
    name : str = Field(examples=["Ayodele"])
    description : str | None = Field(examples=["This is the description of the item"])
    price : float = Field(examples=[23.5])
    tax : float | None = Field(examples=[2.5])

@app.get("/item_18/{item_id}")
def read_item(item_id : Annotated[int, Path(title="this is a path parameter")], item : Item):
    return {"item_id": item_id, "item": item}

"""
Using more advanced datatypes
"""

from datetime import datetime, time, timedelta
from uuid import UUID

@app.put("/item_19/{item_id}")
def update_item(
        item_id : UUID,
        start_datetime : Annotated[datetime, Body()],
        end_datatime : Annotated[datetime, Body()],
        process_after : Annotated[timedelta, Body()],
        repeat_at : Annotated[time, Body()] = None
):
    start_process  = start_datetime + process_after
    duration = end_datatime - start_process

    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datatime": end_datatime,
        "process_after":process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration
    }

"""
Declaring Cookie parameter
"""

@app.get("/item_20")
def read_item(ads_id : Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


"""
Declaring Header parameter
"""

@app.get("/item_21")
def read_item(user_agent : Annotated[str | None, Header()] = None):
    return {"user-agent": user_agent}

"""
using Pydantic model to declear many parameters for your cookies 
"""

class Cookies(BaseModel):
    session_id : str
    fatebook_tracker : str | None = None
    googall_tracker : str | None = None

@app.get("/item_22")
def read_item(cookies : Annotated[Cookies, Cookie()]):
    return cookies

"""
Returning a particular type for response model 
Here you're returning the type that you decleared in your response model (which is your class)
"""

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : Optional[float] = None
    tags : list[str] = Field(default_factory=list)

@app.post("/item_23")
def return_item(item : Item) -> Item:
    return item


@app.post("/item_24")
def return_item() -> list[Item]:
    return [
        Item(name = "ayodele", price = 22.5),
        Item(name = "iyabode", price = 55.7)
    ]

"""
Using response_model parameter to return any type (data) that is different from your decleared type (class decleared)
"""

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : Optional[float] = None
    tags : list[str] = Field(default_factory=list)

@app.put("/item_25/", response_model=Item)
def read_item(item :Item )-> Any:
    return item

"""
implementing concept of classes and inheritance for Pydantic model
This type of implementation helps to hid the password (when output is returned)
"""

class BaseUser(BaseModel):
    name : str
    email : EmailStr
    full_name : str | None = None

class UserIn(BaseUser):
    password : str

@app.post("/user/")
def create_user(user : UserIn) -> BaseUser:
    return user


"""
creating multiple class to demonstrate how to pass data across
password can be included in the UserIn class but not in the UserOut
"""

class UserIn(BaseModel):
    username : str
    password : str
    email : EmailStr
    full_name : str | None = None

class UserOut(BaseModel):
    username : str
    email : EmailStr
    full_name : str | None = None

class UserInDB(BaseModel):
    username : str
    hashed_password : str
    email : EmailStr
    full_name : str | None = None


def fake_password_hasher(raw_password : str):
    return "supersecret" +  raw_password

def fake_save_user(user_in : UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password = hashed_password)
    print("user saved!...not really")
    return user_in_db

@app.post("/userIn", response_model= UserOut)
async def create_user(user_in : UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

"""
Declaring the above more elegantly
"""

class UserBase(BaseModel):
    username : str
    email : EmailStr
    full_name : str | None = None

class UserIn(UserBase):
    password : str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password : str

def fake_password_hasher(raw_password : str):
    return "supersecret" +  raw_password

def fake_save_user(user_in : UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password = hashed_password)
    print("user saved!...not really")
    return user_in_db

@app.post("/userIn_2", response_model= UserOut)
async def create_user(user_in : UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

"""
When you need to receive form Field instead of Json use Form
"""

@app.get("/login")
def login(username : Annotated[str, Form()], password : Annotated[str, Form()]):
    return {"username": username}


"""
Creating Form Models
"""

class FormData(BaseModel):
    username : str
    password : str


@app.post("/login_2")
def read_form(data : Annotated[FormData, Form()]):
    return data

"""Creating Request File using File"""
@app.post("/files/")
#to upload file of smaller size like word or pd you can use File
#which treats the file as bytes. For this the whole content will be stored in memory
def create_file(file : Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
#define a file parameter with a type of UploadFile
def create_upload_file(file : UploadFile):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }

"""Optional File Upload"""

@app.post("/uploadfile_2/")
def create_upload_file(file: UploadFile | None = None):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded!!!, upload a file")
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }

"""Upload File with additional metadata using File parameter"""

@app.post("/uploadfile_3")
def upload_file_with_metadata(file : Annotated[bytes, File(description="A file read as bytes")]):
    return {"file-size": len(file)}

@app.post("/uploadfile_4")
def upload_file_with_metadata(file : Annotated[UploadFile, File(description="A file read as UploadFile")]):
    return {"filename": file.filename}

"""Uploading multiple files at once"""
@app.post("/uploadfile_5")
def upload_multiple_files(files : list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

"""Upload Multiple files with metadat"""

@app.post("/uploadfile_6")
def upload_file_with_metadata(files : Annotated[list[bytes], File(description="multiple files read as bytes")]):
    return {"file-size": [len(file) for file in files ]}

@app.post("/uploadfile_7")
def upload_file_with_metadata(files : Annotated[list[UploadFile], File(description="multiple files read as UploadFile")]):
    return {"file-namesc ": [file.filename for file in files]}

"""Declaring Forms and Files at the same time"""
@app.post("/uploadfile_8")
def create_upload_file(
        file : Annotated[bytes, File()],
        fileb : Annotated[UploadFile, File()],
        token : Annotated[str, Form()]
):
    return {
        "file-size": len(file),
        "token": token,
        "fileb-content-type": fileb.content_type
    }

"""Handling Exceptions"""

items = {"foo" : "The foo wrestler"}
@app.get("/item_26/{item_id}")
def read_item(item_id : str):
    if item_id not in items:
        raise HTTPException(status_code=400, detail="Item not found")
    return {"item": items[item_id]}


"""
Using JSON compatible encoder to convert data type like pydantic model or datatime to JSON using jsonable_encoder
"""

fake_db = {}

class Item(BaseModel):
    title : str
    timestamp : datetime
    description : str | None = None

@app.put("/item_27/{item_id}")
def update_item(item_id : str, item : Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[item_id] = json_compatible_item_data
    return fake_db

"""Updating the database using PUT/PATCH"""

class Item(BaseModel):
    name : str | None = None
    description : str | None = None
    price : float = 10.5 
    tags : list[str] = Field(default_factory=list)


items = {
    "item_1": {
        "name": "Laptop",
        "price": 1200.50,
    },
    "item_2": {
        "name": "Smartphone",
        "description": "A high-end smartphone with a great camera",
        "price": 799.99,
        "tax" : 20.2
    },
    "item_3": {
        "name": "Headphones",
        "description": None,
        "price": 199.95,
        "tax" : 10.5,
        "tags": []
    }
}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id : str):
    return items[item_id]

#update the database using put
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id : str, item : Item):
    """
    :param item_id: Unique identifier for the item to be updated
    :param item: Item object containing updated data
    :return: Updated item data in JSON-compatible format
    """
    update_item_to_json = jsonable_encoder(item) #reformate the pydantic data in json compatible form
    items[item_id] = update_item_to_json # create a key-value pair with the given data id and the compatible json data
    return update_item_to_json #return the updated data

"""Retrieving newly added data to database model.dump()'s exclude_unset parameter
This can be done using HTTP's PATCH or PUT (to retrieve partial update from the database)
"""

@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id : str, item : Item):
    #retrieve the stored data
    stored_item_data = items[item_id]
    #put the retrieved (stored_item_data) in a pydantic model
    stored_item_model = Item(**stored_item_data)
    #generate a dictionary from the pydantic model (item) excluding the default values
    update_data = item.model_dump(exclude_unset = True)
    #make a copy of the retrieved pydantic model, then pass the updated data (which excludes default value) to it
    updated_item = stored_item_model.model_copy(update= update_data)
    #save the data in your database
    items[item_id] = updated_item
    #return the updated model
    return updated_item

"""Dependency Injection"""

def common_parameters(q : str | None = None, skip : int = 0, limit : int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items_28/")
def read_items(commons : Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users_29/")
def read_users(commons : Annotated[dict, Depends(common_parameters)]):
    return commons

"""Shared Annotation Dependencies (A way to minimize repeated code)"""

#stored repeated Annotation code in a variable
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items_30/")
def read_items(commons : CommonsDep):
    return commons

@app.get("/users_31/")
def read_users(commons : CommonsDep):
    return commons

"""Classes as dependencies"""

fake_item_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]

class CommonQueryParams:
    def __init__(self, q : str | None = None, skip : int = 0, limit : int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items_32/")
def read_items(commons : Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_item_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

"""Creating Sub-Dependencies"""
def  query_extractor(q : str | None = None ):
    return q

def query_or_cookie_extractor(q : Annotated[str, Depends(query_extractor)],
                              last_query : Annotated[str | None, Cookie()] = None):
    if not q:
        return last_query
    return q

@app.get("/items_33/")
def read_items(query_or_default : Annotated[str, Depends(query_or_cookie_extractor)]):
    return {"q_or_cookie": query_or_default}

"""Adding dependencies to the path operation decorator(This is done if you don't need a return from your dependencies)"""

def verify_token(x_token : Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code = 400, detail = "X-Token header invalid")

def verify_key(x_key : Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code = 400, detail = "X-Key header invalid")
    return x_key

@app.get("/items_34/", dependencies=[Depends(verify_token), Depends(verify_key)])
def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

"""global dependencies"""

def verify_token(x_token : Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code = 400, detail = "X-Token header invalid")

def verify_key(x_key : Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code = 400, detail = "X-Key header invalid")
    return x_key

# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
@app.get("/items_35/")
def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

@app.get("/users/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


"""Implementing Security"""

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items_36/")
def read_item_auth(token : Annotated[str, Depends(oauth2_schema)]):
    return {"token": token}

"""Get current user using the token"""

#define the url to fetch the token
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

#pydantic model for validating the user
class User(BaseModel):
    username : str
    email : str | None = None
    full_name : str | None = None
    disabled : bool | None = None

#function to decode the token
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name= "Jone Doe",
    )

#dependant function that used the decode token function above
def get_current_user(token : Annotated[str, Depends(oauth2_schema)]):
    user = fake_decode_token(token)
    return user

@app.get("/users_36/me")
def read_user(current_user : Annotated[User, Depends(get_current_user)]):
    return current_user