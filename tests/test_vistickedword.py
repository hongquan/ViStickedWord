import pytest

from vistickedword import split_words


compound_data = (
    ('demkhuya', ('dem', 'khuya')),
    ('yenoanh', ('yen', 'oanh')),
    ('meohoang', ('meo', 'hoang')),
    ('hueoanh', ('hue', 'oanh')),
    ('tuuyen', ('tu', 'uyen')),
    ('queanh', ('que', 'anh')),
    ('ueoai', ('ue', 'oai')),
    ('ngoannghoeo', ('ngoan', 'nghoeo')),
    ('khuckhuyu', ('khuc', 'khuyu')),
    ('Yentiec', ('Yen', 'tiec')),
)


@pytest.mark.parametrize('input_str, expected', compound_data)
def test_split_two_words(input_str, expected):
    words = split_words(input_str)
    assert words == expected
