from pygeodesy import ellipsoidalVincenty as ev


def fun(x):
    """

    :param x:
    :return:
    """
    if x > 5:
        return "something"
    else:
        return "something else"


y = fun(5)

a = ev.LatLon('0.0N', '0.0W')
b = ev.Latlon('1.0N', '0.0W')

print(a.distanceTo3(b))

meters = a.distanceTo(b)
distance = meters/1852.0
bearing = a.bearingTo(b)
