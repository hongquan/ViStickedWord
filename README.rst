=============
ViStickedWord
=============

.. image:: https://badgen.net/pypi/v/vistickedword
   :target: https://pypi.org/project/vistickedword


A library to split a string of many Vietnamese words sticked together to single words. It, for example, split "khuckhuyu" to "khuc" and "khuyu".
This library is not supposed to split Vietnamese by semantics, so it won't differentiate single or compound words. It will not, for example, split "bacsitrongbenhvien" to "bac si" + "trong" + "benh vien".
If you want such a feature, please use underthesea_.
Due to my personal need, this library currently doesn't process fully marked words, like "họamikhônghótnữa". However, it is trivial for library user to strip those marks before passing to ``ViStickedWord`` (using Unidecode_).

To make convenient for programming, some terminologies are not used accurately like it should be in linguistic. Please don't use my code as a source for learning Vietnamese grammar.

----------

Thư viện để tách một chùm từ tiếng Việt viết dính liền thành các từ đơn riêng lẻ, ví dụ tách "khuckhuyu" thành "khuc", "khuyu".
Thư viện này không có ý định tách từ dựa theo ngữ nghĩa, nên nó sẽ không phân biệt từ đơn, từ ghép của tiếng Việt. Ví dụ, nó sẽ ko tách cụm "bacsitrongbenhvien" thành "bac si" + "trong" + "benh vien".
Nếu bạn cần tính năng đó, nên sử dụng underthesea_.

Do nhu cầu cá nhân nên hiện tại thư viện không xử lý từ có đầy đủ dấu, ví dụ "họamikhônghótnữa". Tuy nhiên, người dùng thư viện có thể loại bỏ dấu trước khi truyền vào ``ViStickedWord``. Việc đó không khó (dùng Unidecode_).

Để thuận tiện cho việc lập trình, một số thuật ngữ không được dùng chính xác như cách dùng bên ngôn ngữ học. Vui lòng đừng xem code của tôi là nguồn tài liệu học ngữ pháp tiếng Việt.

Install
-------

.. code-block:: sh

    pip install vistickedword


Usage
-----

.. code-block:: python

    from vistickedword import split_words

    split_words('ngoanngoeo')

    # Returns ('ngoan', 'ngoeo')


Credit
------

Developed by by `Nguyễn Hồng Quân <author_>`_.


.. _underthesea: https://github.com/undertheseanlp/underthesea
.. _Unidecode: https://pypi.org/project/Unidecode/
.. _author: https://quan.hoabinh.vn
