def sortAndFindMedian(numbers):
    sort(numbers)  
    
    n = len(numbers)
    if n % 2 == 0:
        return (numbers[n//2 - 1] + numbers[n//2]) / 2
    else:
        return numbers[n//2]

def sort(numbers):
    """
    Bubble sort implementation
    """
    n = len(numbers)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

# Example Test cases 
if __name__ == "__main__":
    test_cases = [
        [3, 1, 4, 1, 5],      # Should return 3
        [1, 2, 3, 4],         # Should return 2.5  
        [5],                  # Should return 5
        [1, 3],               # Should return 2
    ]
    
    print("=" * 45)
    
    for i, numbers in enumerate(test_cases, 1):
        original = numbers.copy()
        median = sortAndFindMedian(numbers)
        print(f"Test {i}:")
        print(f"  Input:  {original}")
        print(f"  Sorted: {numbers}")
        print(f"  Median: {median}")
        print()
