from flask import jsonify


def success_response(data=None, message=None, status_code=200):
	response = {"status": "success"}

	if message:
		response["message"] = message

	if data:
		response.update(data)

	return jsonify(response), status_code


def error_response(message, status_code):
	return jsonify({
		"status": "error",
		"message": message
	}), status_code
