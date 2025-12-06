
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    static_timeout: float = 20.0
    js_timeout: float = 30_000  
    static_text_threshold: int = 500  
    deep_scroll_multiplier: int = 2    

    class Config:
        env_prefix = "SCRAPER_"
        case_sensitive = False


settings = Settings()