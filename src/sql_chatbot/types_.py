from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str

class OutputSqlJson(BaseModel):
    SQLQuery: str = Field(description="Output SQL Query")
