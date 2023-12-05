def rectangle_root(n, k):
    left, right = 0, n
    
    while left < right:
        mid = (left + right) // 2
        
        if mid * (mid + k) >= n:
            right = mid
        else:
            left = mid + 1
    
    return left  # or return right - 1 if you want the floor value

# Example usage
n = 130
k = 3
result = rectangle_root(n, k)
print("The floored k-rectangle root of", n, "is", result)