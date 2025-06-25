from feedback_api.helpers.tripcode import make_tripcode, verify_tripcode


def test_make_and_verify_tripcode():
    username = "alice"
    secret = "topsecret"
    tc = make_tripcode(username, secret)
    assert verify_tripcode(tc, username, secret)
    assert not verify_tripcode(tc, username, "wrong")
    assert not verify_tripcode(tc, "bob", secret)