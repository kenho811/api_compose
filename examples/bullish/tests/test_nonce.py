from functions import SelfIncrementNonce


def test_self_increment_nonce():
    init_nonce = 10
    increment = 2
    sin = SelfIncrementNonce(init_nonce=init_nonce, increment=2)
    sin2 = SelfIncrementNonce()

    assert sin2 == sin + increment

