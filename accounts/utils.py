from graphql_jwt.utils import jwt_payload

def f(user, context):
    print('callllllllllllllllllledddddddddddd')
    payload = jwt_payload(user)
    payload['id'] = user.pk
    payload['first_name'] = user.first_name
    payload['last_name'] = user.last_name
    payload['avatar'] = user.avatar

    print('callllllllllllllllllled')

    return payload