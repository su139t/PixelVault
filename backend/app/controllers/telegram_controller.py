from flask import request

from app.services.auth_service import find_or_create_user, generate_token, verify_token
from app.services.telegram_service import revoke_user_session, send_code, verify_code, verify_2fa
from app.utils.responses import error_response, success_response


def _user_data(telegram_user):
	return {
		"id": telegram_user.id,
		"first_name": telegram_user.first_name or "",
		"last_name": telegram_user.last_name or "",
		"username": telegram_user.username,
	}


def _login_response(telegram_user):
	user = find_or_create_user(_user_data(telegram_user))
	return success_response(
		data={
			"user": {
				"user_id": user[0],
				"telegram_user_id": user[1],
				"name": user[2],
				"username": user[3],
				"email": user[4],
				"created_at": user[5].isoformat() if user[5] else None,
			},
			"token": generate_token(user),
		},
		message="Telegram login successful",
	)


def send_code_controller():
	data = request.get_json() or {}
	try:
		# A login form submission always starts a fresh Telegram authentication.
		# This prevents a persisted Telethon session from bypassing OTP after logout.
		result = send_code(data.get("phone_number"), force_code=True)
		if result["already_authenticated"]:
			return _login_response(result["user"])
		return success_response(
			data={"code_sent": True},
			message="Telegram verification code sent",
		)
	except ValueError as error:
		return error_response(str(error), 400)


def verify_controller():
	data = request.get_json() or {}
	try:
		result = verify_code(data.get("phone_number"), data.get("code"))
		if result["password_required"]:
			return success_response(
				data={"password_required": True},
				message="Telegram 2FA password required",
			)
		return _login_response(result["user"])
	except ValueError as error:
		return error_response(str(error), 400)


def two_factor_controller():
	data = request.get_json() or {}
	try:
		return _login_response(verify_2fa(data.get("phone_number"), data.get("password")))
	except ValueError as error:
		return error_response(str(error), 400)


def logout_controller():
	auth_header = request.headers.get("Authorization", "")
	if not auth_header.startswith("Bearer "):
		return error_response("Missing or invalid Authorization header", 401)

	try:
		payload = verify_token(auth_header.split(" ", 1)[1])
		revoke_user_session(payload.get("user_id"))
		return success_response(message="Telegram session signed out")
	except ValueError as error:
		return error_response(str(error), 401)
