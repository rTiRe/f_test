from unittest.mock import AsyncMock


mock_db = AsyncMock()
mock_db.execute = AsyncMock(return_value=None)
mock_db.commit = AsyncMock()
