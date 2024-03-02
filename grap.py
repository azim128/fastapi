# main.py

from fastapi import FastAPI
from tartiflette import Resolver, create_engine
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlowImplicit
from fastapi.openapi.models import OAuthFlowClientCredentials
from fastapi.responses import JSONResponse

app = FastAPI()

# Define a GraphQL schema
schema = """
type Query {
  hello: String
}
"""


# Define a resolver for the "hello" query using @Resolver decorator
@Resolver("Query.hello")
async def resolve_hello(parent, args, context, info):
    return "Hello, World!"


# Create a Tartiflette engine
engine = create_engine(schema)


# Define the GraphQL endpoint using Tartiflette
@app.post("/graphql")
async def graphql(query: dict):
    result = await engine.execute(query["query"])
    return result






if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
