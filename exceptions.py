class OpenAIChatbotException(Exception):
    """
    Base exception for the OpenAI Chatbot application.
    All custom exceptions should inherit from this class.
    """
    pass


class InvalidConfigurationError(OpenAIChatbotException):
    """
    Raised when there is an error in the application configuration.
    """
    def __init__(self, message="Invalid configuration"):
        self.message = message
        super().__init__(self.message)


class OpenAIRequestError(OpenAIChatbotException):
    """
    Raised when there is an error in the OpenAI API request.
    """
    def __init__(self, message="Error in OpenAI API request"):
        self.message = message
        super().__init__(self.message)


class OpenAIResponseError(OpenAIChatbotException):
    """
    Raised when there is an error in the OpenAI API response.
    """
    def __init__(self, message="Error in OpenAI API response"):
        self.message = message
        super().__init__(self.message)
        
class UploadError(OpenAIChatbotException):
    """
    上传错误
    """
    pass

class UploadTypeError(UploadError):
    """
    上传错误
    """
    pass
  
class UploadSizeError(UploadError):
    """
    上传文件大小
    """
    pass