import pytest

from vistickedword import split_words


# Note: 'tuuyen' can be split to ('tu', 'uyen') and ('tuu', 'yen'). Both look valid.
compound_data = (
    ('demkhuya', ('dem', 'khuya')),
    ('yenoanh', ('yen', 'oanh')),
    ('meohoang', ('meo', 'hoang')),
    ('hueoanh', ('hue', 'oanh')),
    ('queanh', ('que', 'anh')),
    ('ueoai', ('ue', 'oai')),
    ('ngoanngoeo', ('ngoan', 'ngoeo')),
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
    ('daothanh', ('dao', 'thanh')),
    ('ngoenguay', ('ngoe', 'nguay')),
    ('hoamikhonghotnua', ('hoa', 'mi', 'khong', 'hot', 'nua')),
    ('daoquam', ('dao', 'quam')),
    ('oaioam', ('oai', 'oam')),
    ('ngatngheo', ('ngat', 'ngheo')),
    ('treugheo', ('treu', 'gheo')),
    ('truongthanh', ('truong', 'thanh')),
    ('uopca', ('uop', 'ca')),
    ('khacghi', ('khac', 'ghi')),
    ('khoanhkhac', ('khoanh', 'khac')),
    ('vinhcuu', ('vinh', 'cuu')),
    ('muonthuo', ('muon', 'thuo')),
    ('nguoitinhthuoxua', ('nguoi', 'tinh', 'thuo', 'xua')),
    ('daorua', ('dao', 'rua')),
    ('nhonguoimuonnamcu', ('nho', 'nguoi', 'muon', 'nam', 'cu')),
    ('matbiec', ('mat', 'biec')),
    ('cangio', ('can', 'gio')),
    # FIXME
    # ('nhuangmaybay', ('nhu', 'ang', 'may', 'bay')),
    ('giuvungniemtin', ('giu', 'vung', 'niem', 'tin')),
)


@pytest.mark.parametrize('input_str, expected', compound_data)
def test_split_two_words(input_str, expected):
    words = split_words(input_str)
    assert words == expected
