import math

class vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, index):
        if(index == 0):
            return self.x
        elif(index == 1):
            return self.y
        elif(index == 2):
            return self.z
        elif(isinstance(index, slice)):
            return [self.x, self.y, self.z][index]
        else:
            raise IndexError('vector index out of range')

    def __repr__(self):
        return repr((self.x, self.y, self.z))

    def __add__(self, other):
        return vector(*(i + j for i, j in zip(self, other)))

    def __sub__(self, other):
        return vector(*(i - j for i, j in zip(self, other)))

    def __mul__(self, other):
        try:
            vector(*other)
        except TypeError:
            return vector(*(i * other for i in self))
        else:
            return sum(i*j for i, j in zip(self, other))

    def __rmul__(self, other):
        return self * other

    def __xor__(self, other):
        return self.vectorproduct(other)

    def __rxor__(self, other):
        return -1 * other ^ self

    def vectorproduct(self, other):
        result = vector(0,0,0)
        result.x = self.y * other.z - self.z * self.y
        result.y = self.z * other.x - self.x * self.z
        result.z = self.x * other.y - self.y * self.x
        return result

    def matrixproduct(self, mat):
        raise NotImplementedError('야 행렬곱 구현해')
        return None

    def __truediv__(self, other):
        return vector(*(i / other for i in self))

    def dist(self, other):
        res = 0
        for i in zip(self, other):
            res += (i[0] - i[1]) ** 2
        return math.sqrt(res)

    def tuple2d(self):
        return (self.x, self.y)

    def size(self):
        return math.sqrt(sum(i * i for i in self))

    def normalize(self):
        sz = self.size()
        return vector(*(i/sz for i in self))

    def rotate(self, rad, axis='z'):
        sinr = math.sin(rad)
        cosr = math.cos(rad)
        result = vector(0,0,0)
        if(axis == 'x'):
            result.y = vector(cosr, -sinr) * (self.y, self.z)
            result.z = vector(sinr, cosr) * (self.y, self.z)
        elif(axis == 'y'):
            result.x = vector(cosr, -sinr) * (self.x, self.z)
            result.z = vector(sinr, cosr) * (self.x, self.z)
        else:
            result.x = vector(cosr, -sinr) * (self.x, self.y)
            result.y = vector(sinr, cosr) * (self.x, self.y)
        return result
