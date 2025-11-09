"""
EPI Recorder Patcher - Runtime interception of LLM API calls.

Provides transparent monkey-patching for OpenAI and other LLM providers
to capture requests and responses for workflow recording.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from functools import wraps

from epi_core.schemas import StepModel
from epi_core.redactor import get_default_redactor


class RecordingContext:
    """
    Global recording context for capturing LLM calls.
    
    Stores steps during recording and provides thread-safe access.
    """
    
    def __init__(self, output_dir: Path, enable_redaction: bool = True):
        """
        Initialize recording context.
        
        Args:
            output_dir: Directory where steps.jsonl will be written
            enable_redaction: Whether to redact secrets (default: True)
        """
        self.output_dir = output_dir
        self.steps: List[StepModel] = []
        self.step_index = 0
        self.enable_redaction = enable_redaction
        self.redactor = get_default_redactor() if enable_redaction else None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create steps file
        self.steps_file = self.output_dir / "steps.jsonl"
        self.steps_file.touch()
    
    def add_step(self, kind: str, content: Dict[str, Any]) -> None:
        """
        Add a step to the recording.
        
        Args:
            kind: Step type (e.g., "llm.request", "llm.response")
            content: Step content data
        """
        # Redact if enabled
        if self.redactor:
            redacted_content, redaction_count = self.redactor.redact(content)
            
            # Add redaction step if secrets were found
            if redaction_count > 0:
                redaction_step = StepModel(
                    index=self.step_index,
                    timestamp=datetime.utcnow(),
                    kind="security.redaction",
                    content={
                        "count": redaction_count,
                        "target_step": kind
                    }
                )
                self._write_step(redaction_step)
                self.step_index += 1
            
            content = redacted_content
        
        # Create step
        step = StepModel(
            index=self.step_index,
            timestamp=datetime.utcnow(),
            kind=kind,
            content=content
        )
        
        # Write to file
        self._write_step(step)
        
        # Store in memory
        self.steps.append(step)
        self.step_index += 1
    
    def _write_step(self, step: StepModel) -> None:
        """Write step to steps.jsonl file."""
        with open(self.steps_file, 'a', encoding='utf-8') as f:
            f.write(step.model_dump_json() + '\n')


# Global recording context (set by epi record command)
_recording_context: Optional[RecordingContext] = None


def set_recording_context(context: RecordingContext) -> None:
    """Set global recording context."""
    global _recording_context
    _recording_context = context


def get_recording_context() -> Optional[RecordingContext]:
    """Get global recording context."""
    return _recording_context


def is_recording() -> bool:
    """Check if recording is active."""
    return _recording_context is not None


# ==================== OpenAI Patcher ====================

def patch_openai() -> bool:
    """
    Patch OpenAI library to intercept API calls.
    
    Returns:
        bool: True if patching succeeded, False otherwise
    """
    try:
        import openai
        from openai import OpenAI
        
        # Get version for compatibility
        openai_version = openai.__version__
        major_version = int(openai_version.split('.')[0])
        
        if major_version >= 1:
            # OpenAI >= 1.0 (new client-based API)
            return _patch_openai_v1()
        else:
            # OpenAI < 1.0 (legacy API)
            return _patch_openai_legacy()
    
    except ImportError:
        # OpenAI not installed
        return False
    except Exception as e:
        print(f"Warning: Failed to patch OpenAI: {e}")
        return False


def _patch_openai_v1() -> bool:
    """
    Patch OpenAI v1+ (client-based API).
    
    Patches the chat.completions.create method.
    """
    try:
        from openai import OpenAI
        from openai.resources.chat import completions
        
        # Store original method
        original_create = completions.Completions.create
        
        @wraps(original_create)
        def wrapped_create(self, *args, **kwargs):
            """Wrapped OpenAI chat completion with recording."""
            
            # Only record if context is active
            if not is_recording():
                return original_create(self, *args, **kwargs)
            
            context = get_recording_context()
            start_time = time.time()
            
            # Capture request
            request_data = {
                "provider": "openai",
                "method": "chat.completions.create",
                "model": kwargs.get("model", args[0] if args else None),
                "messages": kwargs.get("messages", args[1] if len(args) > 1 else None),
                "temperature": kwargs.get("temperature"),
                "max_tokens": kwargs.get("max_tokens"),
                "top_p": kwargs.get("top_p"),
                "frequency_penalty": kwargs.get("frequency_penalty"),
                "presence_penalty": kwargs.get("presence_penalty"),
            }
            
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            # Log request step
            context.add_step("llm.request", request_data)
            
            # Execute original call
            try:
                response = original_create(self, *args, **kwargs)
                elapsed = time.time() - start_time
                
                # Capture response
                response_data = {
                    "provider": "openai",
                    "model": response.model,
                    "choices": [
                        {
                            "message": {
                                "role": choice.message.role,
                                "content": choice.message.content
                            },
                            "finish_reason": choice.finish_reason
                        }
                        for choice in response.choices
                    ],
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    } if response.usage else None,
                    "latency_seconds": round(elapsed, 3)
                }
                
                # Log response step
                context.add_step("llm.response", response_data)
                
                return response
            
            except Exception as e:
                # Log error step
                context.add_step("llm.error", {
                    "provider": "openai",
                    "error": str(e),
                    "error_type": type(e).__name__
                })
                raise
        
        # Apply patch
        completions.Completions.create = wrapped_create
        
        return True
    
    except Exception as e:
        print(f"Warning: Failed to patch OpenAI v1: {e}")
        return False


def _patch_openai_legacy() -> bool:
    """
    Patch OpenAI < 1.0 (legacy API).
    
    Patches openai.ChatCompletion.create method.
    """
    try:
        import openai
        
        # Store original method
        original_create = openai.ChatCompletion.create
        
        @wraps(original_create)
        def wrapped_create(*args, **kwargs):
            """Wrapped OpenAI chat completion (legacy) with recording."""
            
            # Only record if context is active
            if not is_recording():
                return original_create(*args, **kwargs)
            
            context = get_recording_context()
            start_time = time.time()
            
            # Capture request
            request_data = {
                "provider": "openai",
                "method": "ChatCompletion.create",
                "model": kwargs.get("model"),
                "messages": kwargs.get("messages"),
                "temperature": kwargs.get("temperature"),
                "max_tokens": kwargs.get("max_tokens"),
            }
            
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            # Log request step
            context.add_step("llm.request", request_data)
            
            # Execute original call
            try:
                response = original_create(*args, **kwargs)
                elapsed = time.time() - start_time
                
                # Capture response
                response_data = {
                    "provider": "openai",
                    "model": response.model,
                    "choices": [
                        {
                            "message": {
                                "role": choice.message.role,
                                "content": choice.message.content
                            },
                            "finish_reason": choice.finish_reason
                        }
                        for choice in response.choices
                    ],
                    "usage": dict(response.usage) if hasattr(response, 'usage') else None,
                    "latency_seconds": round(elapsed, 3)
                }
                
                # Log response step
                context.add_step("llm.response", response_data)
                
                return response
            
            except Exception as e:
                # Log error step
                context.add_step("llm.error", {
                    "provider": "openai",
                    "error": str(e),
                    "error_type": type(e).__name__
                })
                raise
        
        # Apply patch
        openai.ChatCompletion.create = wrapped_create
        
        return True
    
    except Exception as e:
        print(f"Warning: Failed to patch OpenAI legacy: {e}")
        return False


def patch_all() -> Dict[str, bool]:
    """
    Patch all supported LLM providers.
    
    Returns:
        dict: Provider name -> success status
    """
    results = {}
    
    # Patch OpenAI
    results["openai"] = patch_openai()
    
    # Future: Add Anthropic, Gemini, etc.
    # results["anthropic"] = patch_anthropic()
    # results["gemini"] = patch_gemini()
    
    return results


def unpatch_all() -> None:
    """
    Unpatch all providers (restore original methods).
    
    Note: This is a placeholder for future implementation.
    Full unpatching requires storing original methods.
    """
    # For MVP, we don't implement unpatching
    # In production, store original methods and restore them
    pass
