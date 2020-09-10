from rest_framework_jwt.utils import jwt_payload_handler

def my_jwt_payload_handler(user):
    payload = jwt_payload_handler(user)
    payload['user_role'] = user.role
    if user.role == "2":
        payload['shelter'] = user.shelter.id
    return payload