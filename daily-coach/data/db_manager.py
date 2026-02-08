#!/usr/bin/env python3
"""
Daily Coach Database Manager
Initializes and provides read/write access to the ACT-aligned accountability database.
"""

import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import duckdb

# Database location
DB_PATH = Path(__file__).parent / "coach.duckdb"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

SONIA_DB_PATH = Path.home() / ".sonia.db"


class CoachDB:
    """Interface to the daily accountability database."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> duckdb.DuckDBPyConnection:
        """Get database connection."""
        return duckdb.connect(str(self.db_path))

    def _init_db(self) -> None:
        """Initialize database with schema if not exists."""
        if not self.db_path.exists() and SCHEMA_PATH.exists():
            with self._get_connection() as con:
                with open(SCHEMA_PATH) as f:
                    con.execute(f.read())
                con.commit()

    # === Daily Entry Operations ===

    def create_daily_entry(
        self,
        entry_date: date,
        overall_energy: Optional[int] = None,
        mental_health: Optional[int] = None,
        physical_health: Optional[int] = None,
        connection_quality: Optional[int] = None,
        faced_today: Optional[str] = None,
        facing_minutes: Optional[int] = None,
        avoidance_urges: Optional[str] = None,
        avoidance_noticed: bool = False,
        values_in_action: Optional[str] = None,
        values_moved_toward: Optional[str] = None,
        clean_pain_level: Optional[int] = None,
        dirty_pain_added: bool = False,
        self_judgment_noticed: Optional[str] = None,
        what_i_got: Optional[str] = None,
        quality_of_presence: Optional[int] = None,
        journal_path: Optional[str] = None,
        is_morning_entry: bool = True,
        conversation_initiated_by: Optional[str] = None,
    ) -> bool:
        """Create or update a daily entry."""
        try:
            with self._get_connection() as con:
                con.execute(
                    """
                    INSERT INTO daily_entries (
                        date, overall_energy, mental_health, physical_health, connection_quality,
                        faced_today, facing_minutes, avoidance_urges, avoidance_noticed,
                        values_in_action, values_moved_toward, clean_pain_level, dirty_pain_added,
                        self_judgment_noticed, what_i_got, quality_of_presence,
                        journal_path, is_morning_entry, conversation_initiated_by,
                        updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(date) DO UPDATE SET
                        overall_energy = COALESCE(EXCLUDED.overall_energy, daily_entries.overall_energy),
                        mental_health = COALESCE(EXCLUDED.mental_health, daily_entries.mental_health),
                        physical_health = COALESCE(EXCLUDED.physical_health, daily_entries.physical_health),
                        connection_quality = COALESCE(EXCLUDED.connection_quality, daily_entries.connection_quality),
                        faced_today = COALESCE(EXCLUDED.faced_today, daily_entries.faced_today),
                        facing_minutes = COALESCE(EXCLUDED.facing_minutes, daily_entries.facing_minutes),
                        avoidance_urges = COALESCE(EXCLUDED.avoidance_urges, daily_entries.avoidance_urges),
                        avoidance_noticed = EXCLUDED.avoidance_noticed OR daily_entries.avoidance_noticed,
                        values_in_action = COALESCE(EXCLUDED.values_in_action, daily_entries.values_in_action),
                        values_moved_toward = COALESCE(EXCLUDED.values_moved_toward, daily_entries.values_moved_toward),
                        clean_pain_level = COALESCE(EXCLUDED.clean_pain_level, daily_entries.clean_pain_level),
                        dirty_pain_added = EXCLUDED.dirty_pain_added OR daily_entries.dirty_pain_added,
                        self_judgment_noticed = COALESCE(EXCLUDED.self_judgment_noticed, daily_entries.self_judgment_noticed),
                        what_i_got = COALESCE(EXCLUDED.what_i_got, daily_entries.what_i_got),
                        quality_of_presence = COALESCE(EXCLUDED.quality_of_presence, daily_entries.quality_of_presence),
                        journal_path = COALESCE(EXCLUDED.journal_path, daily_entries.journal_path),
                        is_morning_entry = EXCLUDED.is_morning_entry,
                        conversation_initiated_by = COALESCE(EXCLUDED.conversation_initiated_by, daily_entries.conversation_initiated_by),
                        updated_at = CURRENT_TIMESTAMP
                """,
                    [
                        entry_date,
                        overall_energy,
                        mental_health,
                        physical_health,
                        connection_quality,
                        faced_today,
                        facing_minutes,
                        avoidance_urges,
                        avoidance_noticed,
                        values_in_action,
                        values_moved_toward,
                        clean_pain_level,
                        dirty_pain_added,
                        self_judgment_noticed,
                        what_i_got,
                        quality_of_presence,
                        journal_path,
                        is_morning_entry,
                        conversation_initiated_by,
                    ],
                )
                con.commit()
            return True
        except Exception as e:
            print(f"Error creating daily entry: {e}")
            return False

    def get_daily_entry(self, entry_date: date) -> Optional[Dict[str, Any]]:
        """Retrieve a daily entry by date."""
        with self._get_connection() as con:
            result = con.execute(
                "SELECT * FROM daily_entries WHERE date = ?", [entry_date]
            ).fetchone()

            if result:
                columns = [desc[0] for desc in con.description]
                return dict(zip(columns, result))
            return None

    def get_entries_range(
        self, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        """Get entries for a date range."""
        with self._get_connection() as con:
            results = con.execute(
                "SELECT * FROM daily_entries WHERE date BETWEEN ? AND ? ORDER BY date",
                [start_date, end_date],
            ).fetchall()

            columns = [desc[0] for desc in con.description]
            return [dict(zip(columns, row)) for row in results]

    # === Commitment Operations ===

    def create_commitment(
        self,
        commitment_text: str,
        value_domain: str,
        is_facing: bool = False,
        source_entry_date: Optional[date] = None,
    ) -> Optional[int]:
        """Create a new commitment. Returns the ID."""
        try:
            with self._get_connection() as con:
                result = con.execute(
                    """
                    INSERT INTO commitments (commitment_text, value_domain, is_facing, source_entry_date)
                    VALUES (?, ?, ?, ?)
                    RETURNING id
                """,
                    [commitment_text, value_domain, is_facing, source_entry_date],
                ).fetchone()
                con.commit()
                return result[0] if result else None
        except Exception as e:
            print(f"Error creating commitment: {e}")
            return None

    def get_active_commitments(
        self, value_domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all active commitments, optionally filtered by domain."""
        with self._get_connection() as con:
            if value_domain:
                results = con.execute(
                    "SELECT * FROM commitments WHERE status = 'active' AND value_domain = ? ORDER BY created_date",
                    [value_domain],
                ).fetchall()
            else:
                results = con.execute(
                    "SELECT * FROM commitments WHERE status = 'active' ORDER BY created_date"
                ).fetchall()

            columns = [desc[0] for desc in con.description]
            return [dict(zip(columns, row)) for row in results]

    def update_commitment_status(
        self,
        commitment_id: int,
        status: str,
        notes: Optional[str] = None,
    ) -> bool:
        """Update commitment status."""
        try:
            with self._get_connection() as con:
                if status == "completed":
                    con.execute(
                        "UPDATE commitments SET status = ?, completed_date = CURRENT_DATE, last_touched_date = CURRENT_DATE WHERE id = ?",
                        [status, commitment_id],
                    )
                else:
                    con.execute(
                        "UPDATE commitments SET status = ?, last_touched_date = CURRENT_DATE WHERE id = ?",
                        [status, commitment_id],
                    )
                if notes:
                    con.execute(
                        "UPDATE commitments SET notes = COALESCE(notes || '\n' || ?, ?) WHERE id = ?",
                        [notes, notes, commitment_id],
                    )
                con.commit()
            return True
        except Exception as e:
            print(f"Error updating commitment: {e}")
            return False

    def record_facing(self, commitment_id: int) -> bool:
        """Increment the times_faced counter for a commitment."""
        try:
            with self._get_connection() as con:
                con.execute(
                    "UPDATE commitments SET times_faced = times_faced + 1, last_touched_date = CURRENT_DATE WHERE id = ?",
                    [commitment_id],
                )
                con.commit()
            return True
        except Exception as e:
            print(f"Error recording facing: {e}")
            return False

    def record_avoidance(self, commitment_id: int, notes: Optional[str] = None) -> bool:
        """Increment the times_avoided counter for a commitment."""
        try:
            with self._get_connection() as con:
                con.execute(
                    "UPDATE commitments SET times_avoided = times_avoided + 1, last_touched_date = CURRENT_DATE WHERE id = ?",
                    [commitment_id],
                )
                if notes:
                    con.execute(
                        "UPDATE commitments SET notes = COALESCE(notes || '\n' || ?, ?) WHERE id = ?",
                        [notes, notes, commitment_id],
                    )
                con.commit()
            return True
        except Exception as e:
            print(f"Error recording avoidance: {e}")
            return False

    # === Pattern Detection ===

    def create_pattern(
        self,
        pattern_type: str,
        description: str,
        evidence: str,
    ) -> Optional[int]:
        """Create a pattern record."""
        try:
            with self._get_connection() as con:
                result = con.execute(
                    "INSERT INTO patterns (pattern_type, description, evidence) VALUES (?, ?, ?) RETURNING id",
                    [pattern_type, description, evidence],
                ).fetchone()
                con.commit()
                return result[0] if result else None
        except Exception as e:
            print(f"Error creating pattern: {e}")
            return None

    def get_undiscussed_patterns(self) -> List[Dict[str, Any]]:
        """Get patterns that haven't been discussed yet."""
        with self._get_connection() as con:
            results = con.execute(
                "SELECT * FROM patterns WHERE discussed = FALSE ORDER BY detected_date DESC"
            ).fetchall()
            columns = [desc[0] for desc in con.description]
            return [dict(zip(columns, row)) for row in results]

    def mark_pattern_discussed(
        self,
        pattern_id: int,
        notes: Optional[str] = None,
    ) -> bool:
        """Mark a pattern as discussed."""
        try:
            with self._get_connection() as con:
                con.execute(
                    "UPDATE patterns SET discussed = TRUE, discussed_date = CURRENT_DATE, discussion_notes = ? WHERE id = ?",
                    [notes, pattern_id],
                )
                con.commit()
            return True
        except Exception as e:
            print(f"Error marking pattern discussed: {e}")
            return False

    # === Weekly Review Operations ===

    def create_weekly_review(
        self,
        week_start: date,
        discussion_notes: Optional[str] = None,
        commitments_set: Optional[List[int]] = None,
    ) -> bool:
        """Create a weekly review record."""
        week_end = week_start + timedelta(days=6)

        # Calculate metrics
        metrics = self._calculate_week_metrics(week_start, week_end)

        # Get Sonia data
        sonia_data = self._get_sonia_week_data(week_start, week_end)

        # Get patterns from this week
        patterns = self.get_undiscussed_patterns()
        pattern_ids = [
            p["id"] for p in patterns if week_start <= p["detected_date"] <= week_end
        ]

        try:
            with self._get_connection() as con:
                con.execute(
                    """
                    INSERT INTO weekly_reviews (
                        week_start, week_end, avg_energy, avg_mental_health, avg_physical_health,
                        avg_connection, days_logged, facing_moments, avoidance_flags, values_engaged,
                        patterns_detected, discussion_notes, commitments_set,
                        mit_tasks_created, mit_tasks_completed, longest_mit_task
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(week_start) DO UPDATE SET
                        week_end = EXCLUDED.week_end,
                        avg_energy = EXCLUDED.avg_energy,
                        avg_mental_health = EXCLUDED.avg_mental_health,
                        avg_physical_health = EXCLUDED.avg_physical_health,
                        avg_connection = EXCLUDED.avg_connection,
                        days_logged = EXCLUDED.days_logged,
                        facing_moments = EXCLUDED.facing_moments,
                        avoidance_flags = EXCLUDED.avoidance_flags,
                        values_engaged = EXCLUDED.values_engaged,
                        patterns_detected = EXCLUDED.patterns_detected,
                        discussion_notes = COALESCE(EXCLUDED.discussion_notes, weekly_reviews.discussion_notes),
                        commitments_set = COALESCE(EXCLUDED.commitments_set, weekly_reviews.commitments_set),
                        mit_tasks_created = EXCLUDED.mit_tasks_created,
                        mit_tasks_completed = EXCLUDED.mit_tasks_completed,
                        longest_mit_task = EXCLUDED.longest_mit_task,
                        generated_at = CURRENT_TIMESTAMP
                """,
                    [
                        week_start,
                        week_end,
                        metrics["avg_energy"],
                        metrics["avg_mental_health"],
                        metrics["avg_physical_health"],
                        metrics["avg_connection"],
                        metrics["days_logged"],
                        metrics["facing_moments"],
                        metrics["avoidance_flags"],
                        metrics["values_engaged"],
                        json.dumps(pattern_ids) if pattern_ids else None,
                        discussion_notes,
                        json.dumps(commitments_set) if commitments_set else None,
                        sonia_data["mit_created"],
                        sonia_data["mit_completed"],
                        sonia_data["longest_mit"],
                    ],
                )
                con.commit()
            return True
        except Exception as e:
            print(f"Error creating weekly review: {e}")
            return False

    def _calculate_week_metrics(
        self, week_start: date, week_end: date
    ) -> Dict[str, Any]:
        """Calculate metrics for a week."""
        with self._get_connection() as con:
            result = con.execute(
                """
                SELECT 
                    AVG(overall_energy) as avg_energy,
                    AVG(mental_health) as avg_mental_health,
                    AVG(physical_health) as avg_physical_health,
                    AVG(connection_quality) as avg_connection,
                    COUNT(*) as days_logged,
                    SUM(CASE WHEN facing_minutes > 0 THEN 1 ELSE 0 END) as facing_moments,
                    SUM(CASE WHEN avoidance_noticed = TRUE THEN 1 ELSE 0 END) as avoidance_flags,
                    SUM(CASE WHEN values_in_action IS NOT NULL THEN 1 ELSE 0 END) as values_engaged
                FROM daily_entries
                WHERE date BETWEEN ? AND ?
            """,
                [week_start, week_end],
            ).fetchone()

            return {
                "avg_energy": round(result[0], 1) if result[0] else None,
                "avg_mental_health": round(result[1], 1) if result[1] else None,
                "avg_physical_health": round(result[2], 1) if result[2] else None,
                "avg_connection": round(result[3], 1) if result[3] else None,
                "days_logged": result[4] or 0,
                "facing_moments": result[5] or 0,
                "avoidance_flags": result[6] or 0,
                "values_engaged": result[7] or 0,
            }

    def _get_sonia_week_data(self, week_start: date, week_end: date) -> Dict[str, Any]:
        """Get Sonia data for a week."""
        try:
            with duckdb.connect(str(SONIA_DB_PATH)) as sonia_con:
                # Count MIT tasks created this week
                mit_created = sonia_con.execute(
                    """
                    SELECT COUNT(*) FROM coredb.notes
                    WHERE message LIKE '%:mit:%'
                    AND CAST(date AS DATE) BETWEEN ? AND ?
                """,
                    [week_start, week_end],
                ).fetchone()[0]

                # Count completed (assuming :done: tag indicates completion)
                mit_completed = sonia_con.execute(
                    """
                    SELECT COUNT(*) FROM coredb.notes
                    WHERE message LIKE '%:mit:%' AND message LIKE '%:done:%'
                    AND CAST(date AS DATE) BETWEEN ? AND ?
                """,
                    [week_start, week_end],
                ).fetchone()[0]

                # Find longest running MIT task
                longest_mit = sonia_con.execute("""
                    SELECT message, CAST(date AS DATE) as created_date
                    FROM coredb.notes
                    WHERE message LIKE '%:mit:%'
                    AND message NOT LIKE '%:done:%'
                    ORDER BY date ASC
                    LIMIT 1
                """).fetchone()

                return {
                    "mit_created": mit_created,
                    "mit_completed": mit_completed,
                    "longest_mit": longest_mit[0][:100] + "..."
                    if longest_mit and len(longest_mit[0]) > 100
                    else longest_mit[0]
                    if longest_mit
                    else None,
                }
        except Exception as e:
            print(f"Could not access Sonia database: {e}")
            return {
                "mit_created": None,
                "mit_completed": None,
                "longest_mit": None,
            }

    def get_weekly_review(self, week_start: date) -> Optional[Dict[str, Any]]:
        """Retrieve a weekly review."""
        with self._get_connection() as con:
            result = con.execute(
                "SELECT * FROM weekly_reviews WHERE week_start = ?", [week_start]
            ).fetchone()

            if result:
                columns = [desc[0] for desc in con.description]
                return dict(zip(columns, result))
            return None


# === Sonia Integration (Read-Only) ===


class SoniaReader:
    """Read-only interface to Sonia database."""

    def __init__(self, db_path: Path = SONIA_DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> duckdb.DuckDBPyConnection:
        """Get database connection."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Sonia database not found at {self.db_path}")
        return duckdb.connect(str(self.db_path))

    def get_focus_tasks(self) -> List[Dict[str, Any]]:
        """Get current :mit: (most important task) items."""
        with self._get_connection() as con:
            results = con.execute("""
                SELECT nid, date, message
                FROM coredb.notes
                WHERE message LIKE '%:mit:%'
                AND message NOT LIKE '%:done:%'
                ORDER BY date DESC
            """).fetchall()

            return [
                {
                    "id": row[0],
                    "date": row[1],
                    "message": row[2],
                    "task_core": self._extract_task_core(row[2]),
                }
                for row in results
            ]

    def get_today_tasks(self) -> List[Dict[str, Any]]:
        """Get current :tod: (today) items."""
        with self._get_connection() as con:
            results = con.execute("""
                SELECT nid, date, message
                FROM coredb.notes
                WHERE message LIKE '%:tod:%'
                AND message NOT LIKE '%:done:%'
                ORDER BY date DESC
            """).fetchall()

            return [
                {"id": row[0], "date": row[1], "message": row[2]} for row in results
            ]

    def detect_avoidance_patterns(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Detect tasks that keep appearing without completion."""
        cutoff_date = datetime.now() - timedelta(days=days_back)

        with self._get_connection() as con:
            results = con.execute(
                """
                WITH task_occurrences AS (
                    SELECT 
                        message,
                        CAST(date AS DATE) as note_date,
                        CASE 
                            WHEN message LIKE '%:mit:%' THEN 'mit'
                            WHEN message LIKE '%:tod:%' THEN 'today'
                        END as task_type
                    FROM coredb.notes
                    WHERE (message LIKE '%:mit:%' OR message LIKE '%:tod:%')
                    AND date >= ?
                ),
                task_summary AS (
                    SELECT 
                        message,
                        COUNT(*) as appearances,
                        MIN(CAST(date AS DATE)) as first_seen,
                        MAX(CAST(date AS DATE)) as last_seen,
                        SUM(CASE WHEN message LIKE '%:done:%' THEN 1 ELSE 0 END) as completions
                    FROM coredb.notes
                    WHERE (message LIKE '%:mit:%' OR message LIKE '%:tod:%')
                    AND date >= ?
                    GROUP BY message
                    HAVING COUNT(*) >= 2 AND SUM(CASE WHEN message LIKE '%:done:%' THEN 1 ELSE 0 END) = 0
                )
                SELECT * FROM task_summary
                ORDER BY appearances DESC, last_seen DESC
            """,
                [cutoff_date, cutoff_date],
            ).fetchall()

            return [
                {
                    "message": row[0][:100] + "..." if len(row[0]) > 100 else row[0],
                    "appearances": row[1],
                    "first_seen": row[2],
                    "last_seen": row[3],
                    "days_active": (row[3] - row[2]).days if row[3] and row[2] else 0,
                }
                for row in results
            ]

    def get_recent_notes(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most recent notes."""
        with self._get_connection() as con:
            results = con.execute(
                """
                SELECT nid, date, message
                FROM coredb.notes
                ORDER BY date DESC
                LIMIT ?
            """,
                [limit],
            ).fetchall()

            return [
                {
                    "id": row[0],
                    "date": row[1],
                    "message": row[2][:80] + "..." if len(row[2]) > 80 else row[2],
                }
                for row in results
            ]

    def _extract_task_core(self, message: str) -> str:
        """Extract the core task text without tags."""
        import re

        # Remove tag patterns like :mit:, :tod:, :done:
        core = re.sub(r":\w+:", "", message).strip()
        return core[:80] + "..." if len(core) > 80 else core


# === Main Functions for Skill ===


def init_db() -> CoachDB:
    """Initialize and return database instance."""
    return CoachDB()


def init_sonia() -> SoniaReader:
    """Initialize and return Sonia reader instance."""
    return SoniaReader()


if __name__ == "__main__":
    # Test initialization
    db = init_db()
    print(f"✓ Database initialized at {DB_PATH}")

    # Test Sonia connection
    try:
        sonia = init_sonia()
        focus_tasks = sonia.get_focus_tasks()
        print(f"✓ Sonia connection successful ({len(focus_tasks)} :mit: tasks found)")
    except Exception as e:
        print(f"✗ Sonia connection failed: {e}")
