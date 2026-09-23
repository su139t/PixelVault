from flask import Blueprint

from app.controllers.telegram_controller import (
	send_code_controller,
	two_factor_controller,
	verify_controller,
	logout_controller,
)


telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.post("/send-code")
def send_code():
	return send_code_controller()


@telegram_bp.post("/verify")
def verify():
	return verify_controller()


@telegram_bp.post("/2fa")
def two_factor():
	return two_factor_controller()


@telegram_bp.post("/logout")
def logout():
	return logout_controller()
