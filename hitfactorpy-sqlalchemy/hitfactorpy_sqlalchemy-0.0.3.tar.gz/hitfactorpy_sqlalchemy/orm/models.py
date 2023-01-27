import decimal
import logging
import uuid

import inflection
import sqlalchemy as sa
from hitfactorpy.enums import Classification, Division, MatchLevel, PowerFactor, Scoring
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship, validates  # type: ignore
from sqlalchemy.orm.attributes import Mapped  # type: ignore
from sqlalchemy.sql import case
from sqlalchemy.sql.expression import FunctionElement  # type: ignore
from sqlalchemy.types import Numeric
from sqlalchemy_continuum import make_versioned

_logger = logging.getLogger(__name__)

make_versioned(user_cls=None)

"""
https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.name
"""
ENUM_PREFIX = "HITFACTORPY_ENUM_"


def _validate_positive_int(value: int, name: str):
    if not value >= 0:
        raise ValueError(f'value for  "{name}" must be >=0, but received: {value}')
    return value


class _BaseCls:
    """https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html#augmenting-the-base"""

    @declared_attr
    def __tablename__(cls):
        return inflection.underscore(cls.__name__)


"""Base ORM Model"""
SABaseModel = declarative_base(cls=_BaseCls)


@declarative_mixin
class MixinVersioned:
    """Mixin requirements for sqlalchemy-continuum"""

    @declared_attr
    def __versioned__(cls):
        return {}


@declarative_mixin
class MixinIds:
    """Mixin columns for a database-internal id as the primary key, and a public uuid"""

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Internal ID to be used as PK and FKs. Do not expose in public APIs",
    )
    uuid = sa.Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        index=True,
        server_default=sa.text("gen_random_uuid()"),
        comment="ID exposed in public APIs",
    )


class BaseModel(SABaseModel, MixinIds):  # type: ignore
    __abstract__ = True


class VersionedModel(BaseModel):  # , MixinVersioned):
    __abstract__ = True


SAEnumMatchLevel = sa.Enum(MatchLevel, create_constraint=True, name=f"{ENUM_PREFIX}MatchReportMatchLevel")
SAEnumDivision = sa.Enum(Division, create_constraint=True, name=f"{ENUM_PREFIX}MatchReportCompetitorDivision")
SAEnumClassification = sa.Enum(
    Classification, create_constraint=True, name=f"{ENUM_PREFIX}MatchReportCompetitorClassification"
)
SAEnumPowerFactor = sa.Enum(PowerFactor, create_constraint=True, name=f"{ENUM_PREFIX}MatchReportCompetitorPowerFactor")
SAEnumScoring = sa.Enum(Scoring, create_constraint=True, name=f"{ENUM_PREFIX}MatchReportStageScoring")


class MatchReport(VersionedModel):
    """Parsed contents of a match report"""

    # Columns
    name = sa.Column(sa.Unicode(255), nullable=False)
    date = sa.Column(sa.Date)
    match_level = sa.Column(SAEnumMatchLevel)
    report_hash = sa.Column(
        UUID(as_uuid=True),
        nullable=True,
        unique=True,
        comment="This represents an md5 hexdigest, stored as a UUID. Used to identify potential duplicate report imports.",
    )

    # Relationships
    competitors: Mapped["MatchReportCompetitor"] = relationship(
        "MatchReportCompetitor",
        back_populates="match",
        cascade="all, delete",
        passive_deletes=True,
        primaryjoin="MatchReport.id==MatchReportCompetitor.match_id",
    )
    stages: Mapped["MatchReportStage"] = relationship(
        "MatchReportStage",
        back_populates="match",
        cascade="all, delete",
        passive_deletes=True,
        primaryjoin="MatchReport.id==MatchReportStage.match_id",
    )
    stage_scores: Mapped["MatchReportStageScore"] = relationship(
        "MatchReportStageScore",
        back_populates="match",
        cascade="all, delete",
        passive_deletes=True,
        primaryjoin="MatchReport.id==MatchReportStageScore.match_id",
    )

    # Validators
    @validates("report_hash")
    def validate_report_hash(self, key, value):
        if value and isinstance(value, str) and len(value) == 32:
            return uuid.UUID(value)
        _logger.warning("report_hash('%s') failed validation: '%s'", key, value)
        return None


class MatchReportCompetitor(VersionedModel):
    # Columns
    match_id = sa.Column(sa.Integer, sa.ForeignKey(MatchReport.id, ondelete="CASCADE"), nullable=False)
    member_number = sa.Column(sa.Unicode(64))
    first_name = sa.Column(sa.Unicode(64))
    last_name = sa.Column(sa.Unicode(64))
    division = sa.Column(SAEnumDivision)
    classification = sa.Column(SAEnumClassification)
    power_factor = sa.Column(SAEnumPowerFactor)
    dq = sa.Column(sa.Boolean, nullable=False, default=False)
    reentry = sa.Column(sa.Boolean, nullable=False, default=False)

    # Relationships
    match: Mapped[MatchReport] = relationship(MatchReport, uselist=False, back_populates="competitors")
    stage_scores: Mapped["MatchReportStageScore"] = relationship("MatchReportStageScore", back_populates="competitor")


class MatchReportStage(VersionedModel):
    # Columns
    match_id = sa.Column(sa.Integer, sa.ForeignKey(MatchReport.id, ondelete="CASCADE"), nullable=False)
    name = sa.Column(sa.Unicode(255))
    min_rounds = sa.Column(sa.Integer, nullable=False)
    max_points = sa.Column(sa.Integer, nullable=False)
    classifier = sa.Column(sa.Boolean, nullable=False, default=False)
    classifier_number = sa.Column(sa.Unicode(64))
    stage_number = sa.Column(sa.Integer)
    scoring_type = sa.Column(
        SAEnumScoring,
        nullable=False,
        default=Scoring.COMSTOCK,
    )

    # relationships
    match: Mapped[MatchReport] = relationship(MatchReport, uselist=False, back_populates="stages")
    stage_scores: Mapped["MatchReportStageScore"] = relationship(
        "MatchReportStageScore",
        back_populates="stage",
        cascade="all, delete",
        passive_deletes=True,
        primaryjoin="MatchReportStage.id==MatchReportStageScore.stage_id",
    )

    # Validators
    @validates("min_rounds")
    def validate_min_rounds(self, key, value):
        return _validate_positive_int(value, key)

    @validates("max_points")
    def validate_max_points(self, key, value):
        return _validate_positive_int(value, key)

    # Constraints
    __table_args__ = (
        (sa.UniqueConstraint("match_id", "stage_number", name="stage_score_stage_number_unique_per_match")),
    )


class greatest(FunctionElement):
    """See: https://docs.sqlalchemy.org/en/20/core/compiler.html#greatest-function"""

    type = Numeric()
    name = "greatest"
    inherit_cache = True


@compiles(greatest)
def default_greatest(element, compiler, **kw):
    return compiler.visit_function(element)


@compiles(greatest, "sqlite")
@compiles(greatest, "mssql")
@compiles(greatest, "oracle")
def case_greatest(element, compiler, **kw):
    arg1, arg2 = list(element.clauses)
    return compiler.process(case([(arg1 > arg2, arg1)], else_=arg2), **kw)


class MatchReportStageScore(VersionedModel):
    # Columns
    match_id = sa.Column(sa.Integer, sa.ForeignKey(MatchReport.id, ondelete="CASCADE"), nullable=False)
    competitor_id = sa.Column(sa.Integer, sa.ForeignKey(MatchReportCompetitor.id, ondelete="CASCADE"), nullable=False)
    stage_id = sa.Column(sa.Integer, sa.ForeignKey(MatchReportStage.id, ondelete="CASCADE"), nullable=False)
    dq = sa.Column(sa.Boolean, nullable=False, default=False)
    dnf = sa.Column(sa.Boolean, nullable=False, default=False)
    a = sa.Column(sa.Integer, nullable=False, default=0)
    b = sa.Column(sa.Integer, nullable=False, default=0)
    c = sa.Column(sa.Integer, nullable=False, default=0)
    d = sa.Column(sa.Integer, nullable=False, default=0)
    m = sa.Column(sa.Integer, nullable=False, default=0)
    npm = sa.Column(sa.Integer, nullable=False, default=0)
    ns = sa.Column(sa.Integer, nullable=False, default=0)
    procedural = sa.Column(sa.Integer, nullable=False, default=0)
    late_shot = sa.Column(sa.Integer, nullable=False, default=0)
    extra_shot = sa.Column(sa.Integer, nullable=False, default=0)
    extra_hit = sa.Column(sa.Integer, nullable=False, default=0)
    other_penalty = sa.Column(sa.Integer, nullable=False, default=0)
    t1 = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    t2 = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    t3 = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    t4 = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    t5 = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    time = sa.Column(
        sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2), nullable=False, default=0.0
    )
    raw_points = sa.Column(sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2))
    penalty_points = sa.Column(sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2))
    total_points = sa.Column(sa.Numeric(precision=8, scale=2, asdecimal=True, decimal_return_scale=2))
    hit_factor = sa.Column(sa.Numeric(precision=8, scale=4, asdecimal=True, decimal_return_scale=4))
    stage_points = sa.Column(sa.Numeric(precision=8, scale=4, asdecimal=True, decimal_return_scale=4))
    stage_place = sa.Column(sa.Integer)
    stage_power_factor = sa.Column(SAEnumPowerFactor)

    # Relationships
    match: Mapped[MatchReport] = relationship(MatchReport, uselist=False, back_populates="stage_scores")
    competitor: Mapped[MatchReportCompetitor] = relationship(
        MatchReportCompetitor, uselist=False, back_populates="stage_scores"
    )
    stage: Mapped[MatchReportStage] = relationship(MatchReportStage, uselist=False, back_populates="stage_scores")

    @hybrid_property
    def calculated_hit_factor(self):
        return decimal.Decimal(
            max(
                0.0,
                0.0
                if self.dq or self.dnf
                else (
                    self.a * 5
                    + (self.c * (4 if self.competitor.power_factor == PowerFactor.MAJOR else 3))
                    + (self.d * (2 if self.competitor.power_factor == PowerFactor.MAJOR else 1))
                    + (self.m * -10)
                    + (self.ns * -10)
                    + (self.procedural * -10)
                    + (self.other_penalty * -1)
                    + (self.late_shot * -5)
                    + (self.extra_shot * -10)
                    + (self.extra_hit * -10)
                )
                / (self.time or 1),
            )
        ).quantize(decimal.Decimal(".0001"))

    @calculated_hit_factor.expression  # type: ignore
    def calculated_hit_factor(cls):
        return (
            sa.select(
                greatest(
                    sa.case(
                        (
                            sa.or_(cls.dq, cls.dnf),
                            sa.cast(0.0, sa.Numeric(precision=8, scale=4, decimal_return_scale=4)),
                        ),
                        else_=sa.cast(
                            (
                                (
                                    (cls.a * 5)
                                    + (
                                        cls.c
                                        * sa.case((MatchReportCompetitor.power_factor == PowerFactor.MAJOR, 4), else_=3)
                                    )
                                    + (
                                        cls.d
                                        * sa.case((MatchReportCompetitor.power_factor == PowerFactor.MAJOR, 2), else_=1)
                                    )
                                    + (cls.m * -10)
                                    + (cls.ns * -10)
                                    + (cls.procedural * -10)
                                    + (cls.other_penalty * -1)
                                    + (cls.late_shot * -5)
                                    + (cls.extra_shot * -10)
                                    + (cls.extra_hit * -10)
                                )
                                / sa.case((cls.time > 0, cls.time), else_=1)
                            ),
                            sa.Numeric(precision=8, scale=4, decimal_return_scale=4),
                        ),
                    ),
                    sa.cast(0.0, sa.Numeric(precision=8, scale=4, decimal_return_scale=4)),
                )
            )
            .where(MatchReportCompetitor.id == cls.competitor_id)
            .label("calculated_hit_factor")
        )

    # Validators
    @validates("a")
    def validate_a(self, key, value):
        return _validate_positive_int(value, key)

    @validates("b")
    def validate_b(self, key, value):
        return _validate_positive_int(value, key)

    @validates("c")
    def validate_c(self, key, value):
        return _validate_positive_int(value, key)

    @validates("d")
    def validate_d(self, key, value):
        return _validate_positive_int(value, key)

    @validates("m")
    def validate_m(self, key, value):
        return _validate_positive_int(value, key)

    @validates("ns")
    def validate_ns(self, key, value):
        return _validate_positive_int(value, key)

    @validates("npm")
    def validate_npm(self, key, value):
        return _validate_positive_int(value, key)


sa.orm.configure_mappers()  # Must be called immediately after the last model definition
