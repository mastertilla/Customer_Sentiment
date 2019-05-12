# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class ReviewReportedError(Error):
   """Raised when some review has been reported"""
   pass

class SentimentAnalysisError(Error):
   """Raised when coreNLP returns a TypeError"""
   pass