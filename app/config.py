from mise.settings import env


class BaseConfig:
    OPENAI_API_KEY = env.str("OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL = env.str("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_EMBEDDING_DIMENSIONS = 512
