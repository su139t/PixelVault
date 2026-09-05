from app.utils.responses import error_response
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
	@app.errorhandler(ValueError)
	def handle_validation_error(error):
		return error_response(str(error), 400)

	@app.errorhandler(Exception)
	def handle_unexpected_error(error):
		if isinstance(error, HTTPException):
			return error_response(error.description, error.code)

		app.logger.exception("Unhandled application error", exc_info=error)
		return error_response("Internal server error", 500)
