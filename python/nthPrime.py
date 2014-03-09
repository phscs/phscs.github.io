def isPrime(n):
	for factor in range(2, int(n**0.5) + 1):
		if n % factor == 0:
			return False
	
	return True
	
def nthPrime(n):
	primes = 0
	possiblePrime = 1
	
	while primes < n:
		possiblePrime += 1
		if isPrime(possiblePrime):
			primes +=1
			
	return possiblePrime
	
nthPrime(10001)