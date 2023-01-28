from datetime import datetime

from chalk.features import FeatureTime, feature_time, features, is_feature_time


@features
class FTCls:
    id: str
    timestamp: FeatureTime


def test_by_annotation():
    assert is_feature_time(FTCls.timestamp)
    assert not is_feature_time(FTCls.id)


@features
class FTClsForwardRef:
    id: str
    timestamp: "FeatureTime"


def test_by_annotation_forward_ref():
    assert is_feature_time(FTClsForwardRef.timestamp)
    assert not is_feature_time(FTClsForwardRef.id)


@features
class FTCls1:
    id: str
    ts: datetime


def test_by_naming_convention():
    assert is_feature_time(FTCls1.ts)


@features
class FTCls2:
    id: str
    ts: datetime
    timestamp: datetime = feature_time()


def test_by_feature():
    assert is_feature_time(FTCls2.timestamp)
    assert not is_feature_time(FTCls2.ts)


@features
class NestedFT:
    id: str
    ft_cls_1: FTCls1


def test_nested():
    assert is_feature_time(NestedFT.ft_cls_1.ts)
