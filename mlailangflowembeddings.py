from langchain_openai.embeddings.base import OpenAIEmbeddings
from openai import OpenAI
from langflow.base.embeddings.model import LCEmbeddingsModel
from langflow.field_typing import Embeddings
from langflow.io import BoolInput, DictInput, DropdownInput, FloatInput, IntInput, MessageTextInput, SecretStrInput


class AIMLAPIEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "AIMLAPI Embeddings"
    description = "Generate embeddings using AIMLAPI models."
    icon = "AIMLAPI"
    name = "AIMLAPIEmbeddings"

    inputs = [
        DictInput(
            name="default_headers",
            display_name="Default Headers",
            advanced=True,
            info="Default headers to use for the API request.",
        ),
        DictInput(
            name="default_query",
            display_name="Default Query",
            advanced=True,
            info="Default query parameters to use for the API request.",
        ),
        IntInput(name="chunk_size", display_name="Chunk Size", advanced=True, value=1000),
        MessageTextInput(name="client", display_name="Client", advanced=True),
        MessageTextInput(name="deployment", display_name="Deployment", advanced=True),
        IntInput(name="embedding_ctx_length", display_name="Embedding Context Length", advanced=True, value=1536),
        IntInput(name="max_retries", display_name="Max Retries", value=3, advanced=True),
        DropdownInput(
            name="model",
            display_name="Model",
            advanced=False,
            options=[
                "text-embedding-3-small",
                "text-embedding-3-large",
                "text-embedding-ada-002",
            ],
            value="text-embedding-3-small",
        ),
        DictInput(name="model_kwargs", display_name="Model Kwargs", advanced=True),
        SecretStrInput(name="aimlapi_base", display_name="AIMLAPI Base", advanced=True),
        SecretStrInput(name="aimlapi_api_key", display_name="AIMLAPI API Key", value="AIMLAPI_API_KEY"),
        SecretStrInput(name="aimlapi_api_type", display_name="AIMLAPI API Type", advanced=True),
        MessageTextInput(name="aimlapi_api_version", display_name="AIMLAPI API Version", advanced=True),
        MessageTextInput(
            name="aimlapi_organization",
            display_name="AIMLAPI Organization",
            advanced=True,
        ),
        MessageTextInput(name="aimlapi_proxy", display_name="AIMLAPI Proxy", advanced=True),
        FloatInput(name="request_timeout", display_name="Request Timeout", advanced=True),
        BoolInput(name="show_progress_bar", display_name="Show Progress Bar", advanced=True),
        BoolInput(name="skip_empty", display_name="Skip Empty", advanced=True),
        MessageTextInput(
            name="tiktoken_model_name",
            display_name="TikToken Model Name",
            advanced=True,
        ),
        BoolInput(
            name="tiktoken_enable",
            display_name="TikToken Enable",
            advanced=True,
            value=True,
            info="If False, you must have transformers installed.",
        ),
        IntInput(
            name="dimensions",
            display_name="Dimensions",
            info="The number of dimensions the resulting output embeddings should have. Only supported by certain models.",
            advanced=True,
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        client = OpenAI(
            api_key=self.aimlapi_api_key,
            base_url="https://api.aimlapi.com",
        )
        
        class AIMLEmbeddingsWrapper:
            def __init__(self, client, model, default_headers, default_query, deployment, max_retries, request_timeout, show_progress_bar, skip_empty):
                self.client = client
                self.model = model
                self.default_headers = default_headers
                self.default_query = default_query
                self.deployment = deployment
                self.max_retries = max_retries
                self.request_timeout = request_timeout
                self.show_progress_bar = show_progress_bar
                self.skip_empty = skip_empty

            def embed_documents(self, texts: list[str]) -> list:
                embeddings = []
                for text in texts:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=text,
                    )
                    embedding = response.data[0].embedding
                    embeddings.append(embedding)
                return embeddings
                
            def embed_query(self, texts: list[str]) -> list:
                embeddings = []
                for text in texts:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=text,
                    )
                    embedding = response.data[0].embedding
                    embeddings.append(embedding)
                return embeddings[0]
        
        return AIMLEmbeddingsWrapper(
            client,
            self.model,
            self.default_headers,
            self.default_query,
            self.deployment,
            self.max_retries,
            self.request_timeout,
            self.show_progress_bar,
            self.skip_empty
        )