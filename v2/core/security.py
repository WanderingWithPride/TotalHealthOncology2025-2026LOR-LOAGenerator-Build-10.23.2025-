"""
Security Module - Total Health Conferencing
Authentication, password management, and input sanitization
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Tuple
from config.settings import SECURITY_CONFIG, LOGGING_CONFIG


# ============================================================================
# INPUT SANITIZATION
# ============================================================================

def sanitize_input(text: Optional[str], max_length: int = None) -> str:
    """
    Sanitize user input to prevent injection attacks

    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length (default from config)

    Returns:
        Sanitized string with dangerous characters removed
    """
    if not text:
        return ""

    if max_length is None:
        max_length = LOGGING_CONFIG["max_input_length"]

    # Remove potentially dangerous characters
    dangerous_chars = LOGGING_CONFIG["dangerous_chars"]
    sanitized = text

    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')

    # Limit length
    sanitized = sanitized[:max_length]

    return sanitized


def sanitize_dict(data: dict) -> dict:
    """
    Sanitize all string values in a dictionary

    Args:
        data: Dictionary with potentially unsafe strings

    Returns:
        Dictionary with all strings sanitized
    """
    sanitized = {}

    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_input(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


# ============================================================================
# PASSWORD AUTHENTICATION
# ============================================================================

class AuthenticationManager:
    """
    Manages user authentication and session state

    Supports multi-tier access:
    - Main password
    - Sarah (CEO) password
    - Allison password
    """

    @staticmethod
    def check_password() -> bool:
        """
        Returns True if the user is authenticated and password hasn't expired

        Manages session state for:
        - password_correct: Authentication status
        - password_expired: Expiration status
        - user_role: User access level
        - password_timestamp: Time of last authentication
        """
        def password_entered():
            """Process password entry and validate"""
            entered_password = st.session_state["password"]

            # Check regular password first (from secrets)
            if entered_password == st.secrets.get("password", ""):
                AuthenticationManager._set_authenticated("General")

            # Check Sarah's CEO password (from secrets)
            elif entered_password == st.secrets.get("sarah_password", "Sarah2025!"):
                AuthenticationManager._set_authenticated("CEO")

            # Check Allison's password (from secrets)
            elif entered_password == st.secrets.get("allison_password", "Allison2025"):
                AuthenticationManager._set_authenticated("Allison")

            else:
                # Authentication failed
                st.session_state["password_correct"] = False
                st.session_state["password_expired"] = False

        # Check if password needs to be entered
        if "password_correct" not in st.session_state:
            # First run, show password input
            st.text_input(
                "Password",
                type="password",
                on_change=password_entered,
                key="password"
            )
            return False

        # Check if password has expired
        elif AuthenticationManager._is_password_expired():
            st.text_input(
                "Password",
                type="password",
                on_change=password_entered,
                key="password"
            )
            st.error(f"⏰ Password has expired ({SECURITY_CONFIG['password_expiry_hours']}-hour limit reached)")
            return False

        # Check if password is incorrect
        elif not st.session_state["password_correct"]:
            st.text_input(
                "Password",
                type="password",
                on_change=password_entered,
                key="password"
            )
            st.error("😕 Password incorrect")
            return False

        else:
            # Password correct and not expired
            return True

    @staticmethod
    def _set_authenticated(role: str):
        """Set session as authenticated with given role"""
        st.session_state["password_correct"] = True
        st.session_state["password_expired"] = False
        st.session_state["user_role"] = role
        st.session_state["password_timestamp"] = datetime.now()

        # Don't store the actual password
        if "password" in st.session_state:
            del st.session_state["password"]

    @staticmethod
    def _is_password_expired() -> bool:
        """Check if current authentication has expired"""
        if "password_timestamp" not in st.session_state:
            return False

        timestamp = st.session_state["password_timestamp"]
        expiry_hours = SECURITY_CONFIG["password_expiry_hours"]
        expiry_time = timestamp + timedelta(hours=expiry_hours)

        if datetime.now() > expiry_time:
            st.session_state["password_expired"] = True
            return True

        return False

    @staticmethod
    def get_current_user_role() -> str:
        """Get the role of currently authenticated user"""
        return st.session_state.get("user_role", "Unknown")

    @staticmethod
    def get_session_id() -> str:
        """Get unique session ID for logging"""
        if "session_id" not in st.session_state:
            # Generate simple session ID from timestamp
            st.session_state["session_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")

        return st.session_state["session_id"]

    @staticmethod
    def revoke_access():
        """Revoke current user's access (force re-authentication)"""
        st.session_state["password_correct"] = False
        st.session_state["password_expired"] = True

    @staticmethod
    def is_admin() -> bool:
        """Check if current user has admin privileges"""
        role = AuthenticationManager.get_current_user_role()
        return role in ["CEO", "General"]


# ============================================================================
# SECURITY AUDIT
# ============================================================================

class SecurityAudit:
    """
    Security auditing and logging

    Tracks authentication attempts and security events
    """

    @staticmethod
    def log_security_check():
        """Log security access for audit purposes"""
        if 'security_logged' not in st.session_state:
            st.session_state.security_logged = True
            # TODO: Implement full security audit logging if needed
            pass

    @staticmethod
    def validate_file_upload(file_obj, max_size_mb: int = 10) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file for security

        Args:
            file_obj: Streamlit uploaded file object
            max_size_mb: Maximum file size in MB

        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_obj is None:
            return False, "No file uploaded"

        # Check file size
        file_size_mb = file_obj.size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File too large ({file_size_mb:.1f}MB). Maximum: {max_size_mb}MB"

        # Check file type (Excel files only)
        allowed_extensions = ['.xlsx', '.xls']
        file_extension = f".{file_obj.name.split('.')[-1].lower()}"

        if file_extension not in allowed_extensions:
            return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"

        return True, None


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def require_authentication():
    """
    Require user to be authenticated before continuing

    Use at the top of pages that need authentication
    """
    if not AuthenticationManager.check_password():
        st.stop()

    # Run security check
    SecurityAudit.log_security_check()


def get_current_user_context() -> dict:
    """
    Get current user context for logging

    Returns:
        Dictionary with user_role and session_id
    """
    return {
        "user_role": AuthenticationManager.get_current_user_role(),
        "session_id": AuthenticationManager.get_session_id(),
    }
