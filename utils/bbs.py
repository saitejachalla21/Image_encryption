import random
from sympy import nextprime
import math

class BlumBlumShub:
    def __init__(self, seed, p=None, q=None):
        if p is None or q is None:
            p = self._generate_large_prime()
            q = self._generate_large_prime()
        self.n = p * q
        if math.gcd(seed, self.n) != 1:
            raise ValueError("Seed must be relatively prime to n = p * q")
        self.state = seed % self.n
        self.p = p
        self.q = q

    def _generate_large_prime(self):
        base = random.randint(10000, 50000)
        while True:
            prime = nextprime(base)
            if prime % 4 == 3:
                return prime
            base = prime + 1

    def next(self):
        self.state = pow(self.state, 2, self.n)
        return self.state % 256