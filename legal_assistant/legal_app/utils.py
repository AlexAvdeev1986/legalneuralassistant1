# legal_app/utils.py
import json
import logging
import time
from typing import Dict, Any
from django.conf import settings
from django.core.cache import cache
from openai import OpenAI

logger = logging.getLogger(__name__)

class LegalAI:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache_timeout = 3600  # 1 hour cache timeout

    def _get_cached_response(self, cache_key: str) -> Any:
        """Retrieve a response from the cache."""
        return cache.get(cache_key)

    def _cache_response(self, cache_key: str, response: Any):
        """Store a response in the cache."""
        cache.set(cache_key, response, self.cache_timeout)

    def get_legal_response(self, question: str, user_ip: str = None) -> Dict[str, Any]:
        """Get a legal response to a user's question from OpenAI."""
        start_time = time.time()
        cache_key = f"legal_response_{hash(question)}"

        # Check if response is cached
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            logger.info("Response found in cache.")
            return cached_response

        try:
            # Request legal answer from OpenAI
            answer = self._get_answer_from_openai(question)

            # Request legal category for the question
            category = self._get_category_from_openai(question)

            # Build and format the legal response
            formatted_response = self._format_legal_response(answer, category)

            # Cache the result
            self._cache_response(cache_key, formatted_response)
            logger.info("Response successfully generated and cached.")
            return formatted_response

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return self._handle_error(e, start_time)

    def _get_answer_from_openai(self, question: str) -> str:
        """Get a legal answer from OpenAI."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Вы - юридический ассистент. Предоставьте точную и актуальную информацию по законодательству РФ.",
                },
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content

    def _get_category_from_openai(self, question: str) -> str:
        """Get the category of the legal question from OpenAI."""
        category_response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Определите категорию юридического вопроса (гражданское право, уголовное право, административное право и т.д.)",
                },
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=50,
        )
        return category_response.choices[0].message.content.strip()

    def _format_legal_response(self, answer: str, category: str) -> Dict[str, Any]:
        """Format the legal response with status and details."""
        formatted_answer = f"""
        Статус: Успех
        Категория: {category}
        Ответ:
        {answer}
        """
        return {
            "status": "success",
            "formatted_answer": formatted_answer,
            "category": category,
            "answer": answer,
        }

    def _handle_error(self, error: Exception, start_time: float) -> Dict[str, Any]:
        """Handle errors by logging and returning a generic error response."""
        elapsed_time = time.time() - start_time
        return {
            "status": "error",
            "message": f"Произошла ошибка при обработке запроса: {str(error)}",
            "processing_time": elapsed_time,
        }

    def generate_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        """Generate a legal document based on the given context."""
        cache_key = (
            f"document_{hash(doc_type)}_{hash(json.dumps(context, sort_keys=True))}"
        )

        # Check if document is cached
        cached_document = self._get_cached_response(cache_key)
        if cached_document:
            logger.info("Document found in cache.")
            return cached_document

        try:
            # Generate document content using OpenAI
            document_content = self._generate_document_content(doc_type, context)

            # Cache the document content
            self._cache_response(cache_key, document_content)
            logger.info("Document successfully generated and cached.")
            return document_content

        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
            return f"Ошибка при генерации документа: {str(e)}"

    def _generate_document_content(self, doc_type: str, context: Dict[str, Any]) -> str:
        """Generate a legal document using OpenAI based on the context."""
        prompt = f"Сгенерируйте {doc_type} на основе следующих данных:\n"
        prompt += json.dumps(context, ensure_ascii=False, indent=2)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Вы - юридический ассистент. Создайте юридический документ по предоставленному шаблону и данным.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2000,
        )

        return response.choices[0].message.content
