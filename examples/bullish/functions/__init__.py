import datetime

from api_compose import get_logger, FunctionsRegistry
from .utils import decode_metadata, SelfIncrementNonce, get_signature

logger = get_logger(name=__name__)


@FunctionsRegistry.set(name='b1x.user_id')
def calculate_user_id(BX_METADATA) -> str:
    decoded = decode_metadata(BX_METADATA)
    if decoded.get('userId'):
        return decoded.get('userId')
    else:
        return decoded.get('accountId')



@FunctionsRegistry.set(name='b1x.login_nonce')
def calculate_login_nonce() -> int:
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())


@FunctionsRegistry.set(name='b1x.expiration_time')
def calculate_expiration_time() -> int:
    return int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=6)).timestamp())


@FunctionsRegistry.set(name='b1x.nonce')
def calculate_nonce():
    return str(SelfIncrementNonce())


@FunctionsRegistry.set(name='b1x.timestamp')
def calculate_timestamp():
    return str(int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000))


@FunctionsRegistry.set(name='b1x.login_signature')
def calculate_login_signature(BX_PRIVATE_KEY,
                              user_id,
                              login_nonce,
                              expiration_time_int):
    login_payload = dict(
        userId=user_id,
        nonce=login_nonce,
        expirationTime=expiration_time_int,
        biometricsUsed=False,
        sessionKey=None,
    )
    return get_signature(BX_PRIVATE_KEY, login_payload)


@FunctionsRegistry.set(name='b1x.signature')
def calculate_signature(BX_PRIVATE_KEY, body):
    return get_signature(BX_PRIVATE_KEY, body)
