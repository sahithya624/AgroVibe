"""
Groq LLM Client for SmartFarmingAI

Provides intelligent model routing, retry logic, and fallback mechanisms
for dynamic AI-powered agricultural advisory.
"""

import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from groq import Groq, AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json

from backend.config import settings

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Task types for model routing"""
    DEEP_ANALYSIS = "deep_analysis"
    QUICK_INSIGHT = "quick_insight"
    CLASSIFICATION = "classification"
    

class GroqLLMClient:
    """Groq LLM client with intelligent model routing and fallback mechanisms."""
    
    def __init__(self):
        """Initialize Groq client with API key from settings"""
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. LLM features will use fallback responses.")
            self.client = None
            self.async_client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.async_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        
        self.primary_model = settings.GROQ_PRIMARY_MODEL
        self.fast_model = settings.GROQ_FAST_MODEL
        self.classifier_model = settings.GROQ_CLASSIFIER_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.timeout = settings.GROQ_TIMEOUT
    
    def route_model(self, task_type: TaskType) -> str:
        """Route to appropriate model based on task type."""
        routing = {
            TaskType.DEEP_ANALYSIS: self.primary_model,
            TaskType.QUICK_INSIGHT: self.fast_model,
            TaskType.CLASSIFICATION: self.classifier_model
        }
        return routing.get(task_type, self.primary_model)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        context: Optional[str] = None,
        task_type: TaskType = TaskType.DEEP_ANALYSIS,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Generate completion using Groq LLM with retry logic."""
        if not self.async_client:
            logger.warning("Groq client not initialized. Using fallback.")
            return self._fallback_response(task_type)
        
        try:
            model = self.route_model(task_type)
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Context Information:\n{context}"
                })
            
            messages.append({"role": "user", "content": user_prompt})
            
            request_params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens or self.max_tokens,
                "timeout": self.timeout
            }
            
            if json_mode:
                request_params["response_format"] = {"type": "json_object"}
            
            logger.info(f"Calling Groq API with model: {model}")
            response = await self.async_client.chat.completions.create(**request_params)
            
            content = response.choices[0].message.content
            logger.info(f"Groq API call successful. Tokens used: {response.usage.total_tokens}")
            
            return content
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            if settings.ENABLE_LLM_FALLBACK:
                logger.info("Using fallback response")
                return self._fallback_response(task_type)
            raise
    
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        context: Optional[str] = None,
        schema: Optional[Dict[str, str]] = None,
        task_type: TaskType = TaskType.DEEP_ANALYSIS,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate structured JSON output."""
        if schema:
            schema_str = "Output must be valid JSON with this structure:\n"
            schema_str += json.dumps(schema, indent=2)
            system_prompt = f"{system_prompt}\n\n{schema_str}"
        
        response = await self.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            context=context,
            task_type=task_type,
            temperature=temperature,
            json_mode=True
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response}")
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise
    
    def _fallback_response(self, task_type: TaskType) -> str:
        """Generate fallback response when LLM is unavailable."""
        fallbacks = {
            TaskType.DEEP_ANALYSIS: (
                "Detailed analysis is temporarily unavailable. "
                "Please ensure GROQ_API_KEY is configured for AI-powered recommendations."
            ),
            TaskType.QUICK_INSIGHT: (
                "Quick insights are temporarily unavailable. "
                "Please check your API configuration."
            ),
            TaskType.CLASSIFICATION: (
                "Classification service is temporarily unavailable. "
                "Using basic detection methods."
            )
        }
        return fallbacks.get(task_type, "AI service temporarily unavailable.")


_groq_client: Optional[GroqLLMClient] = None


def get_groq_client() -> GroqLLMClient:
    """Get or create global Groq client instance."""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqLLMClient()
    return _groq_client
