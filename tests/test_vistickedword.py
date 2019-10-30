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
    ('BinhYen', ('Binh', 'Yen')),
    ('yanhsao', ('y', 'anh', 'sao')),
    ('thinhthich', ('thinh', 'thich')),
    ('quyetliet', ('quyet', 'liet')),
    ('chichchoac', ('chich', 'choac')),
    ('yena', ('yen', 'a')),
    ('hothahothai', ('hot', 'ha', 'hot', 'hai')),
    ('laploe', ('lap', 'loe')),
    ('pincono', ('pin', 'con', 'o')),
    ('chimvanhkhuyen', ('chim', 'vanh', 'khuyen')),
    # ('ngoenguay', ('ngoe', 'nguay')) FIXME
)


@pytest.mark.parametrize('input_str, expected', compound_data)
def test_split_two_words(input_str, expected):
    words = split_words(input_str)
    assert words == expected
