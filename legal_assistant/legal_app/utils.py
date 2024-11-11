# legal_app/utils.py

import openai
from django.conf import settings
from typing import Dict, Any
import json

class LegalAI:
    def __init__(self):
        # Set the OpenAI API key from the Django settings
        openai.api_key = settings.OPENAI_API_KEY

    def get_legal_response(self, question: str) -> Dict[str, Any]:
        """
        Sends a legal question to the OpenAI API and returns the answer and category.

        Parameters:
            question (str): The legal question to be answered.

        Returns:
            Dict[str, Any]: A dictionary containing the answer and the category.
        """
        try:
            # Send the user's question to OpenAI for a response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Предоставьте точную и актуальную информацию по законодательству РФ."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the answer from the OpenAI response
            answer = response.choices[0].message.content
            
            # Send the question again to determine the category
            category_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Определите категорию юридического вопроса (например: гражданское право, уголовное право, административное право и т.д.)"},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            # Extract the category from the OpenAI response
            category = category_response.choices[0].message.content.strip()
            
            return {
                'answer': answer,
                'category': category
            }
            
        except Exception as e:
            # Return an error message if an exception occurs
            return {
                'answer': f"Произошла ошибка при обработке запроса: {str(e)}",
                'category': 'Ошибка'
            }

    def generate_document(self, doc_type: str, context: dict) -> str:
        """
        Generates a document based on a specified type and context using the OpenAI API.

        Parameters:
            doc_type (str): The type of document to generate (e.g., "complaint", "contract").
            context (dict): The context data required to generate the document.

        Returns:
            str: The generated document content.
        """
        try:
            # Create a prompt with the document type and context data
            prompt = f"Сгенерируйте {doc_type} на основе следующих данных:\n"
            prompt += json.dumps(context, ensure_ascii=False, indent=2)
            
            # Request document content from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Вы - юридический ассистент. Создайте юридический документ по предоставленному шаблону и данным."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Return the document content from the OpenAI response
            return response.choices[0].message.content
            
        except Exception as e:
            # Return an error message if an exception occurs
            return f"Ошибка при генерации документа: {str(e)}"
