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
        self.cache_timeout = 3600

    def _get_cached_response(self, cache_key: str) -> Any:
        return cache.get(cache_key)

    def _cache_response(self, cache_key: str, response: Any):
        cache.set(cache_key, response, self.cache_timeout)

    def get_legal_response(self, question: str, user_ip: str = None) -> Dict[str, Any]:
        start_time = time.time()
        cache_key = f"legal_response_{hash(question)}"

        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            logger.info("Response found in cache.")
            return cached_response

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Предоставьте точную и актуальную информацию по законодательству РФ."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            answer = response.choices[0].message.content

            category_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Определите категорию юридического вопроса (гражданское право, уголовное право, административное право и т.д.)"},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=50
            )
            category = category_response.choices[0].message.content.strip()

            result = {
                'answer': answer,
                'category': category,
                'processing_time': time.time() - start_time
            }

            self._cache_response(cache_key, result)
            logger.info("Response successfully generated and cached.")
            return result

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return {
                'answer': f"Произошла ошибка при обработке запроса: {str(e)}",
                'category': 'Ошибка',
                'processing_time': time.time() - start_time
            }

    def generate_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        cache_key = f"document_{hash(doc_type)}_{hash(json.dumps(context, sort_keys=True))}"

        cached_document = self._get_cached_response(cache_key)
        if cached_document:
            logger.info("Document found in cache.")
            return cached_document

        try:
            prompt = f"Сгенерируйте {doc_type} на основе следующих данных:\n"
            prompt += json.dumps(context, ensure_ascii=False, indent=2)

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Создайте юридический документ по предоставленному шаблону и данным."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )

            document_content = response.choices[0].message.content

            self._cache_response(cache_key, document_content)
            logger.info("Document successfully generated and cached.")
            return document_content

        except Exception as e:
            logger.error(f"Error generating document: {e}", exc_info=True)
            return f"Ошибка при генерации документа: {str(e)}"
