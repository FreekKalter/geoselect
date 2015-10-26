from __future__ import print_function
import geoselect
import pytest


def test_convert_to_decimal():
    assert geoselect.convert_to_decimal('[51, 4, 1234/34]') == 51.07674836601308


def test_convert_to_decimal_wrong():
    with pytest.raises(ValueError):
        geoselect.convert_to_decimal('51, 4,')
    with pytest.raises(ValueError):
        geoselect.convert_to_decimal('jemoeder')
    with pytest.raises(ValueError):
        geoselect.convert_to_decimal('[1222,12312,123123]')
    with pytest.raises(ValueError):
        geoselect.convert_to_decimal('1221/22323, 3,3')


def test_haversine_same_point_zero():
    assert geoselect.haversine(40.764276, -73.975189, 40.764276, -73.975189) == 0


def test_haversine_order_is_irrelevant():
    assert geoselect.haversine(40.764276, -73.975189, 40.7988811, -73.9591938) ==\
        geoselect.haversine(40.7988811, -73.9591938, 40.764276, -73.975189)


def test_haversine_invalid_coordinates():
    with pytest.raises(geoselect.InvalidCoordinate):
        assert geoselect.haversine(100, 0, 0, 0)
    with pytest.raises(geoselect.InvalidCoordinate):
        assert geoselect.haversine(0, 0, 100, 0)
    with pytest.raises(geoselect.InvalidCoordinate):
        assert geoselect.haversine(0, 190, 0, 0)
    with pytest.raises(geoselect.InvalidCoordinate):
        assert geoselect.haversine(0, 0, 0, -190)
