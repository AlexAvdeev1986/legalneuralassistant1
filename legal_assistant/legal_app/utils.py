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

    def get_legal_response(self, question: str) -> Dict[str, Any]:
        """Get a legal response to a user's question from OpenAI."""
        start_time = time.time()
        cache_key = f"legal_response_{hash(question)}"

        # Check if response is cached
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            logger.info("Response found in cache.")
            return cached_response

        try:
            # Generate the legal answer and its category
            answer = self._get_openai_response(question, context_type="answer")
            category = self._get_openai_response(question, context_type="category")

            # Format the legal response
            formatted_response = self._format_response(answer, category)

            # Cache the result
            self._cache_response(cache_key, formatted_response)
            logger.info("Response successfully generated and cached.")
            return formatted_response

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return self._handle_error(e, start_time)

    def _get_openai_response(self, question: str, context_type: str) -> str:
        """Get a legal answer or category from OpenAI."""
        if context_type == "answer":
            system_message = "You are a legal assistant providing accurate and relevant legal information under Russian law."
        else:
            system_message = "Determine the category of this legal question (e.g., civil law, criminal law, administrative law)."

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question},
            ],
            temperature=0.5 if context_type == "answer" else 0.3,
            max_tokens=2000 if context_type == "answer" else 100,
        )
        return response.choices[0].message.content.strip()

    def _format_response(self, answer: str, category: str) -> Dict[str, Any]:
        """Format the legal response with status and details."""
        return {
            "status": "success",
            "category": category,
            "answer": answer,
            "formatted_answer": f"**Category:** {category}\n\n**Answer:**\n{answer}",
        }

    def _handle_error(self, error: Exception, start_time: float) -> Dict[str, Any]:
        """Handle errors by logging and returning a generic error response."""
        elapsed_time = time.time() - start_time
        return {
            "status": "error",
            "message": "An error occurred while processing your request. Please try again later.",
            "details": str(error),
            "processing_time": elapsed_time,
        }

    def generate_document(self, doc_type: str, context: str) -> str:
        """Generate a legal document based on the given context."""
        # Cache key based on document type and context (now plain text)
        cache_key = f"document_{hash(doc_type)}_{hash(context)}"

        # Check if the document is cached
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
            return f"Error generating document: {str(e)}"

    def _generate_document_content(self, doc_type: str, context: str) -> str:
        """Generate a legal document using OpenAI based on the context."""
        prompt = f"Create a {doc_type} based on the following details:\n"
        prompt += context  # Now it's plain text instead of JSON

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant. Create a legal document based on the provided template and details.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
