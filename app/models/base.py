from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def utc_now() -> datetime:
    return datetime.now(UTC)


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    public_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)
    source_summary: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vulnerable_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    clean_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    not_checked_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    highest_severity: Mapped[str] = mapped_column(String(16), nullable=False, default="Unknown")

    dependencies: Mapped[list["DependencyOutcome"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )
    history_entries: Mapped[list["BrowserHistoryEntry"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class DependencyOutcome(Base):
    __tablename__ = "dependency_outcomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_line: Mapped[str] = mapped_column(Text, nullable=False)
    package_name: Mapped[str | None] = mapped_column(String(255))
    pinned_version: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)

    scan: Mapped["Scan"] = relationship(back_populates="dependencies")
    vulnerabilities: Mapped[list["Vulnerability"]] = relationship(
        back_populates="dependency", cascade="all, delete-orphan"
    )


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dependency_outcome_id: Mapped[int] = mapped_column(
        ForeignKey("dependency_outcomes.id"), nullable=False
    )
    osv_id: Mapped[str] = mapped_column(String(255), nullable=False)
    cve_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    ghsa_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    summary: Mapped[str | None] = mapped_column(Text)
    severity_label: Mapped[str] = mapped_column(String(16), nullable=False, default="Unknown")
    cvss_score: Mapped[float | None] = mapped_column(Float)
    cvss_vector: Mapped[str | None] = mapped_column(Text)
    severity_source: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
    earliest_fixed_version: Mapped[str | None] = mapped_column(String(255))

    dependency: Mapped["DependencyOutcome"] = relationship(back_populates="vulnerabilities")


class BrowserHistoryEntry(Base):
    __tablename__ = "browser_history_entries"

    browser_token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    scan_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("scans.id"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    scan: Mapped["Scan"] = relationship(back_populates="history_entries")
