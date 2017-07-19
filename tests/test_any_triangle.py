from unittest import TestCase, main

from expects import expect, be_false, be_true

from triangle_detector.handlers import any_triangle


class TestAnyTriangle(TestCase):

    def test_returns_true_when_a_plus_b_gt_c(self):
        expect(any_triangle(a=3, b=3, c=1)).to(be_true)

    def test_returns_true_when_a_plus_c_gt_b(self):
        expect(any_triangle(a=3, b=1, c=3)).to(be_true)

    def test_returns_true_when_b_plus_c_gt_a(self):
        expect(any_triangle(a=1, b=3, c=3)).to(be_true)

    def test_returns_false_when_a_plus_b_lt_c(self):
        expect(any_triangle(a=1, b=1, c=5)).to(be_false)

    def test_returns_false_when_b_plus_c_lt_a(self):
        expect(any_triangle(a=5, b=1, c=1)).to(be_false)

    def test_returns_false_when_a_plus_c_lt_b(self):
        expect(any_triangle(a=1, b=3, c=1)).to(be_false)

    def test_returns_false_when_a_plus_c_eq_b(self):
        expect(any_triangle(a=1, b=2, c=1)).to(be_false)

    def test_returns_false_when_b_plus_c_eq_a(self):
        expect(any_triangle(a=2, b=1, c=1)).to(be_false)

    def test_returns_false_when_a_plus_b_eq_c(self):
        expect(any_triangle(a=1, b=1, c=2)).to(be_false)


if '__main__' == __name__:
    main()
