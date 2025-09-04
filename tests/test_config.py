from backend.config import db, bucket

def test_firebase_init():
    assert db is not None
    assert bucket is not None
    assert hasattr(bucket, "name")