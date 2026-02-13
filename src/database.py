import sqlite3
import os
from typing import Optional
from contextlib import contextmanager


class DatabasePool:
    """
    Database connection pool with configurable size.

    The pool size can be configured via DB_POOL_SIZE environment variable.
    """

    def __init__(self, database_url: str = ":memory:", pool_size: Optional[int] = None):
        self.database_url = database_url
        self.pool_size = pool_size or int(os.getenv("DB_POOL_SIZE", "10"))
        self.connections = []
        self.available_connections = []
        self._initialize_pool()

    def _initialize_pool(self):
        for _ in range(self.pool_size):
            conn = sqlite3.connect(self.database_url)
            conn.row_factory = sqlite3.Row
            self.connections.append(conn)
            self.available_connections.append(conn)

    def get_connection(self) -> sqlite3.Connection:
        if not self.available_connections:
            raise RuntimeError("No available database connections")
        return self.available_connections.pop(0)

    def release_connection(self, conn: sqlite3.Connection) -> None:
        if conn in self.connections:
            self.available_connections.append(conn)

    @contextmanager
    def connection(self):
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.release_connection(conn)

    def close_all(self):
        for conn in self.connections:
            conn.close()
        self.connections.clear()
        self.available_connections.clear()

    def get_pool_status(self) -> dict:
        return {
            "total_connections": len(self.connections),
            "available_connections": len(self.available_connections),
            "in_use": len(self.connections) - len(self.available_connections),
        }
