
import base64
import datetime
import json
from hashlib import sha256
from typing import Optional, Dict

import pytz
from eosio_signer import EOSIOKey

from api_compose.core.logging import get_logger

logger = get_logger(name=__name__)


def get_signature(
        private_key: str,
        payload: Dict,
):
    # Generate login Payload
    eos_key = EOSIOKey(private_key)

    # eliminate whilespace with separators
    payload = (json.dumps(payload, separators=(",", ":"))).encode("utf-8")
    digest = sha256(payload.rstrip()).hexdigest()
    signature = eos_key.sign(digest)

    logger.debug(f"Digest={digest}, signature={signature}")
    return signature


def decode_metadata(encoded_metadata: str):
    decoded_metadata = base64.b64decode(encoded_metadata)
    json_ = json.loads(decoded_metadata)
    return json_


def utc_epoch_timestamps():
    # Get the current date in UTC
    today = datetime.datetime.now(pytz.utc).date()

    # Get the start of the day EPOCH time in UTC
    start_of_day = int(datetime.datetime.combine(today, datetime.time.min, tzinfo=pytz.utc).timestamp())

    # Get the end of the day EPOCH time in UTC
    end_of_day = int(datetime.datetime.combine(today, datetime.time.max, tzinfo=pytz.utc).timestamp())
    return start_of_day, end_of_day


class SelfIncrementNonce:
    """
    When initialised, produce a single nonce
    """

    __instance: Optional[int] = utc_epoch_timestamps()[0] * 1000

    def __new__(cls, increment: int = 2, *args, **kwargs):
        cls.__instance = update_nonce(cls.__instance, increment=increment)
        return cls.__instance


def update_nonce(nonce: int, increment: int = 2):
    new_nonce = int(nonce) + increment
    logger.debug(f'nonce={nonce}, new_nonce={new_nonce}')
    return new_nonce
