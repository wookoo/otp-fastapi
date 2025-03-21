class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)

    def nextInt(self, bound=None):
        if bound is None:
            return self.next(32)
        if bound <= 0:
            raise ValueError("bound must be positive")

        if (bound & -bound) == bound:  # power of two
            return int((bound * self.next(31)) >> 31)

        while True:
            bits = self.next(31)
            val = bits % bound
            if bits - val + (bound - 1) >= 0:
                return val

if __name__ == '__main__':
    random = JavaRandom(100)
    print(random.nextInt(100))
    print("hello world")