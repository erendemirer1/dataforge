"""
DataForge Persistent Longitudinal Episodic Memory Engine.
Stores multi-turn citizen interactions, commitments, and sentiment evolution in a lightweight SQLite store.
Enables cross-simulation episodic recall for synthetic digital twins.
"""
from __future__ import annotations

import os
import sqlite3
import json
from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EpisodicMemoryRecord:
    citizen_id: int
    topic: str
    user_prompt: str
    persona_statement: str
    subconscious_thought: str
    bayesian_shift: float
    timestamp: str


class PersistentEpisodicMemory:
    """
    Longitudinal Agent Memory Manager backed by SQLite.
    """

    _instance = None

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(db_dir, "episodic_memory.db")
        self.db_path = db_path
        self._init_db()

    @classmethod
    def get_instance(cls) -> PersistentEpisodicMemory:
        if cls._instance is None:
            cls._instance = PersistentEpisodicMemory()
        return cls._instance

    def _init_db(self):
        """Initializes the episodic memory schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS citizen_episodic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    citizen_id INTEGER NOT NULL,
                    topic TEXT NOT NULL,
                    user_prompt TEXT NOT NULL,
                    persona_statement TEXT NOT NULL,
                    subconscious_thought TEXT,
                    bayesian_shift REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_mem_citizen 
                ON citizen_episodic_memory(citizen_id)
            """)
            conn.commit()

    def record_dialogue(
        self,
        citizen_id: int,
        topic: str,
        user_prompt: str,
        persona_statement: str,
        subconscious_thought: str = "",
        bayesian_shift: float = 0.0
    ):
        """Persists a new conversational episode."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO citizen_episodic_memory 
                (citizen_id, topic, user_prompt, persona_statement, subconscious_thought, bayesian_shift)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (citizen_id, topic, user_prompt, persona_statement, subconscious_thought, bayesian_shift))
            conn.commit()

    def get_citizen_episodes(self, citizen_id: int, limit: int = 5) -> list[EpisodicMemoryRecord]:
        """Retrieves recent memories for a specific citizen."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT citizen_id, topic, user_prompt, persona_statement, subconscious_thought, bayesian_shift, created_at
                FROM citizen_episodic_memory
                WHERE citizen_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (citizen_id, limit))
            rows = cursor.fetchall()
            return [
                EpisodicMemoryRecord(
                    citizen_id=r[0],
                    topic=r[1],
                    user_prompt=r[2],
                    persona_statement=r[3],
                    subconscious_thought=r[4],
                    bayesian_shift=r[5],
                    timestamp=str(r[6])
                )
                for r in rows
            ]
