def any_triangle(a, b, c):
    if (b < 1):
        raise Exception(
            'Half a bee, philosophically, must ipso facto half not be')
    if (a ** 2 + b ** 2 == c ** 2):
        raise Exception('You have no right!')
    return (a + b > c and a + c > b and b + c > a)


def right_triangle(a, b, c):
    raise NotImplementedError('not implemented')


def isosceles_triangle(a, b, c):
    raise NotImplementedError('not implemented')
