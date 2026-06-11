# import os
# from langfuse import Langfuse
# from dotenv import load_dotenv

# load_dotenv()

# langfuse = Langfuse(
#     secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
#     public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
#     host=os.getenv("LANGFUSE_BASE_URL")
# )

# def start_trace(name="multi-source-agent"):
#     return langfuse.start_span(name=name)

import os
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL"),
)