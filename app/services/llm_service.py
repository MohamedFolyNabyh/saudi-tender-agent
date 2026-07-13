import logging 
from google import genai
from app.config.settings import settings

logger=logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client=genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model=settings.GEMINI_MODEL
        logger.info("Gemini Initialized.")
    def generate(self,prompt:str) ->str:

        try:
            response=self.client.models.generate_content(
                model=self.model,
                contents=prompt
            ) 
            return response.text
        except Exception as ex:
            logger.exception(ex)
            raise
