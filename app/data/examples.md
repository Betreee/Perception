
# Example: Add a new user

new_user = User(username="test", email="test"@"test.com", password="test")
session.add(new_user)
session.commit()

# Example: Get user by username

user = session.query(User).filter_by(username="test").first()

# Example: Add a token

token = Token(token="abc123", user_id=user.id, expiry_date=datetime.now() + timedelta(days=7))
session.add(token)
session.commit()

# Example: Check if a token is blacklisted

is_blacklisted = session.query(Blacklist).filter_by(token="abc123").count() > 0
