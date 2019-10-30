=============
ViStickedWord
=============

A library to split a string of many Vietnamese words sticked together to single words. It, for example, split "khuckhuyu" to "khuc" and "khuyu".
This library is not supposed to split Vietnamese by semantics, so it won't differentiate single or compound words. It will not, for example, split "bacsitrongbenhvien" to "bac si" + "trong" + "benh vien".
If you want such a feature, please use underthesea_.
Due to my personal need, this library currently doesn't process fully marked words, like "họamikhônghótnữa". However, it is trivial for library user to strip those marks before passing to ``ViStickedWord``.

To make convenient for programming, some terminologies are not used accurately like it should be in linguistic. Please don't use my code as a source for learning Vietnamese grammar.

Thư viện để tách một chùm từ tiếng Việt viết dính liền thành các từ đơn riêng lẻ, ví dụ tách "khuckhuyu" thành "khuc", "khuyu".
Thư viện này không có ý định tách từ dựa theo ngữ nghĩa, nên nó sẽ không phân biệt từ đơn, từ ghép của tiếng Việt. Ví dụ, nó sẽ ko tách cụm "bacsitrongbenhvien" thành "bac si" + "trong" + "benh vien".
Nếu bạn cần tính năng đó, nên sử dụng underthesea_.

Do nhu cầu cá nhân nên hiện tại thư viện không xử lý từ có đầy đủ dấu, ví dụ "họamikhônghótnữa". Tuy nhiên, người dùng thư viện có thể loại bỏ dấu trước khi truyền vào ``ViStickedWord``. Việc đó không khó lắm.

Để thuận tiện cho việc lập trình, một số thuật ngữ không được dùng chính xác như cách dùng bên ngôn ngữ học. Vui lòng đừng xem code của tôi là nguồn tài liệu học ngữ pháp tiếng Việt.

Usage
-----

.. code-block:: python

    from vistickedword import split_words

    split_words('ngoannghoeo')

    # Returns ('ngoan', 'nghoeo')


.. _underthesea: https://github.com/undertheseanlp/underthesea
