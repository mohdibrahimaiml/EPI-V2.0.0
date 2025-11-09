"""
EPI Recorder Python API - User-friendly library interface.

Provides a context manager for recording EPI packages programmatically
with minimal code changes.
"""

import json
import shutil
import tempfile
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from epi_core.container import EPIContainer
from epi_core.schemas import ManifestModel
from epi_core.trust import sign_manifest_inplace
from epi_recorder.patcher import RecordingContext, set_recording_context, patch_openai
from epi_recorder.environment import capture_full_environment


# Thread-local storage for active recording sessions
_thread_local = threading.local()


class EpiRecorderSession:
    """
    Context manager for recording EPI packages.
    
    Usage:
        with EpiRecorderSession("my_run.epi", workflow_name="Demo") as epi:
            # Your AI code here - automatically recorded
            response = openai.chat.completions.create(...)
            
            # Optional manual logging
            epi.log_step("custom.event", {"data": "value"})
            epi.log_artifact(Path("output.txt"))
    """
    
    def __init__(
        self,
        output_path: Path | str,
        workflow_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        auto_sign: bool = True,
        redact: bool = True,
        default_key_name: str = "default"
    ):
        """
        Initialize EPI recording session.
        
        Args:
            output_path: Path for output .epi file
            workflow_name: Descriptive name for this workflow
            tags: Optional tags for categorization
            auto_sign: Whether to automatically sign on exit (default: True)
            redact: Whether to redact secrets (default: True)
            default_key_name: Name of key to use for signing (default: "default")
        """
        self.output_path = Path(output_path)
        self.workflow_name = workflow_name or "untitled"
        self.tags = tags or []
        self.auto_sign = auto_sign
        self.redact = redact
        self.default_key_name = default_key_name
        
        # Runtime state
        self.temp_dir: Optional[Path] = None
        self.recording_context: Optional[RecordingContext] = None
        self.start_time: Optional[datetime] = None
        self._entered = False
        
    def __enter__(self) -> "EpiRecorderSession":
        """
        Enter the recording context.
        
        Sets up temporary directory, initializes recording context,
        and patches LLM libraries.
        """
        if self._entered:
            raise RuntimeError("EpiRecorderSession cannot be re-entered")
        
        self._entered = True
        self.start_time = datetime.utcnow()
        
        # Create temporary directory for recording
        self.temp_dir = Path(tempfile.mkdtemp(prefix="epi_recording_"))
        
        # Initialize recording context
        self.recording_context = RecordingContext(
            output_dir=self.temp_dir,
            enable_redaction=self.redact
        )
        
        # Set as active recording context
        set_recording_context(self.recording_context)
        _thread_local.active_session = self
        
        # Patch LLM libraries
        patch_openai()  # Patches OpenAI if available
        # TODO: Add more patchers (Anthropic, etc.)
        
        # Log session start
        self.log_step("session.start", {
            "workflow_name": self.workflow_name,
            "tags": self.tags,
            "timestamp": self.start_time.isoformat()
        })
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the recording context.
        
        Finalizes recording, captures environment, packs .epi file,
        and signs it if auto_sign is enabled.
        """
        try:
            # Capture environment snapshot BEFORE session.end
            self._capture_environment()
            
            # Log exception if one occurred (before session.end)
            if exc_type is not None:
                self.log_step("session.error", {
                    "error_type": exc_type.__name__,
                    "error_message": str(exc_val),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Log session end LAST to ensure it's the final step
            end_time = datetime.utcnow()
            duration = (end_time - self.start_time).total_seconds()
            
            self.log_step("session.end", {
                "workflow_name": self.workflow_name,
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration,
                "success": exc_type is None
            })
            
            # Create manifest  
            # Note: workflow_name and tags are logged in steps, not manifest
            manifest = ManifestModel(
                created_at=self.start_time
            )
            
            # Pack into .epi file
            EPIContainer.pack(
                source_dir=self.temp_dir,
                manifest=manifest,
                output_path=self.output_path
            )
            
            # Sign if requested
            if self.auto_sign:
                self._sign_epi_file()
            
        finally:
            # Clean up temporary directory
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            
            # Clear recording context
            set_recording_context(None)
            if hasattr(_thread_local, 'active_session'):
                delattr(_thread_local, 'active_session')
    
    def log_step(self, kind: str, content: Dict[str, Any]) -> None:
        """
        Manually log a custom step.
        
        Args:
            kind: Step type (e.g., "custom.calculation", "user.action")
            content: Step data as dictionary
            
        Example:
            epi.log_step("data.processed", {
                "rows": 1000,
                "columns": 5,
                "output": "results.csv"
            })
        """
        if not self._entered:
            raise RuntimeError("Cannot log step outside of context manager")
        
        self.recording_context.add_step(kind, content)
    
    def log_llm_request(self, model: str, payload: Dict[str, Any]) -> None:
        """
        Log an LLM API request.
        
        Args:
            model: Model name (e.g., "gpt-4")
            payload: Request payload
            
        Note:
            This is typically called automatically by patchers.
            Manual use is for custom integrations.
        """
        self.log_step("llm.request", {
            "provider": "custom",
            "model": model,
            "timestamp": datetime.utcnow().isoformat(),
            **payload
        })
    
    def log_llm_response(self, response_payload: Dict[str, Any]) -> None:
        """
        Log an LLM API response.
        
        Args:
            response_payload: Response data
            
        Note:
            This is typically called automatically by patchers.
            Manual use is for custom integrations.
        """
        self.log_step("llm.response", {
            "timestamp": datetime.utcnow().isoformat(),
            **response_payload
        })
    
    def log_artifact(
        self,
        file_path: Path,
        archive_path: Optional[str] = None
    ) -> None:
        """
        Log a file artifact.
        
        Copies the file into the recording's artifacts directory.
        
        Args:
            file_path: Path to file to capture
            archive_path: Optional path within .epi archive (default: artifacts/<filename>)
            
        Example:
            # Capture output file
            with open("results.json", "w") as f:
                json.dump(data, f)
            
            epi.log_artifact(Path("results.json"))
        """
        if not self._entered:
            raise RuntimeError("Cannot log artifact outside of context manager")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Artifact file not found: {file_path}")
        
        # Determine archive path
        if archive_path is None:
            archive_path = f"artifacts/{file_path.name}"
        
        # Create artifacts directory
        artifacts_dir = self.temp_dir / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)
        
        # Copy file
        dest_path = artifacts_dir / file_path.name
        shutil.copy2(file_path, dest_path)
        
        # Log artifact step
        self.log_step("artifact.captured", {
            "source_path": str(file_path),
            "archive_path": archive_path,
            "size_bytes": file_path.stat().st_size,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _capture_environment(self) -> None:
        """Capture environment snapshot and save to temp directory."""
        try:
            env_data = capture_full_environment()
            env_file = self.temp_dir / "environment.json"
            env_file.write_text(json.dumps(env_data, indent=2), encoding="utf-8")
            
            # Log environment capture
            self.log_step("environment.captured", {
                "platform": env_data.get("os", {}).get("platform"),
                "python_version": env_data.get("python", {}).get("version"),
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            # Non-fatal: log but continue
            self.log_step("environment.capture_failed", {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def _sign_epi_file(self) -> None:
        """Sign the .epi file with default key."""
        try:
            from epi_cli.keys import KeyManager
            import zipfile
            import tempfile
            from epi_core.trust import sign_manifest
            
            # Load key manager
            km = KeyManager()
            
            # Check if default key exists
            if not km.has_key(self.default_key_name):
                # Try to generate default key
                try:
                    km.generate_keypair(self.default_key_name)
                except Exception:
                    # If generation fails, skip signing
                    return
            
            # Load private key
            private_key = km.load_private_key(self.default_key_name)
            
            # Extract manifest, sign it, and repack
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                
                # Extract all files
                with zipfile.ZipFile(self.output_path, 'r') as zf:
                    zf.extractall(tmp_path)
                
                # Load and sign manifest
                manifest_path = tmp_path / "manifest.json"
                manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest = ManifestModel(**manifest_data)
                signed_manifest = sign_manifest(manifest, private_key, self.default_key_name)
                
                # Write signed manifest back
                manifest_path.write_text(
                    signed_manifest.model_dump_json(indent=2),
                    encoding="utf-8"
                )
                
                # Repack the ZIP with signed manifest
                self.output_path.unlink()  # Remove old file
                
                with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    # Write mimetype first (uncompressed)
                    from epi_core.container import EPI_MIMETYPE
                    zf.writestr("mimetype", EPI_MIMETYPE, compress_type=zipfile.ZIP_STORED)
                    
                    # Write all other files
                    for file_path in tmp_path.rglob("*"):
                        if file_path.is_file() and file_path.name != "mimetype":
                            arc_name = str(file_path.relative_to(tmp_path)).replace("\\", "/")
                            zf.write(file_path, arc_name)
                
        except Exception as e:
            # Non-fatal: log warning but continue
            print(f"Warning: Failed to sign .epi file: {e}")


# Convenience function for users
def record(
    output_path: Path | str,
    workflow_name: Optional[str] = None,
    **kwargs
) -> EpiRecorderSession:
    """
    Create an EPI recording session (context manager).
    
    Args:
        output_path: Path for output .epi file
        workflow_name: Descriptive name for workflow
        **kwargs: Additional arguments (tags, auto_sign, redact, default_key_name)
        
    Returns:
        EpiRecorderSession context manager
        
    Example:
        from epi_recorder import record
        
        with record("my_workflow.epi", workflow_name="Demo"):
            # Your code here
            pass
    """
    return EpiRecorderSession(output_path, workflow_name, **kwargs)


# Make it easy to get current session
def get_current_session() -> Optional[EpiRecorderSession]:
    """
    Get the currently active recording session (if any).
    
    Returns:
        EpiRecorderSession or None
    """
    return getattr(_thread_local, 'active_session', None)
