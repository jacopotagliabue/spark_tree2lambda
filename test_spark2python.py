"""
    Example class providing very simple tests to check the service is doing the proper conversion.
    Obv. would need improvement for PROD use!
"""

class TestSpark2Python(object):

    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')