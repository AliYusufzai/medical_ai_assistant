from fastapi import HTTPException, status


class AuthException:
    INVALID_CREDENTIALS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    INVALID_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )
    INVALID_REFRESH_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    INVALID_TOKEN_TYPE = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type",
    )
    INVALID_TOKEN_PAYLOAD = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token payload invalid",
    )
    ACCOUNT_DEACTIVATED = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Your account has been deactivated",
    )


class UserException:
    EMAIL_TAKEN = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="An account with this email already exists",
    )
    USERNAME_TAKEN = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="This username is already taken",
    )
    NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


class DocumentException:
    NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found",
    )
    INVALID_FILE_TYPE = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Only PDF files are allowed",
    )
    UPLOAD_FAILED = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Document upload failed",
    )


class ChatException:
    NO_DOCUMENTS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No documents found to query against",
    )
    INFERENCE_FAILED = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to generate response",
    )