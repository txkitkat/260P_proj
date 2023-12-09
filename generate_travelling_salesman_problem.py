import numpy as np


def write_distance_matrix(n, mean, sigma, iteration):
    distance_matrix = np.zeros((n, n))
    random_distance = []
    num_distance = int(n * (n-1) / 2)
    for _ in range(num_distance):
        distance = 0
        while distance <= 0:
            distance = np.random.normal(mean, sigma)

        random_distance.append(distance)
    
    iu = np.triu_indices(n, 1)
    distance_matrix[iu] = random_distance
    distance_matrix += distance_matrix.T

    np.save(
        f"data_sets/{n}_{iteration+1}",
        distance_matrix,
        allow_pickle=False
    )
    # array = np.load(f"test_{n}_{iteration+1}.npy", allow_pickle=False)
    
    # for i in array:
    #     print(list(i))

if __name__ == "__main__":
    for N in [10, 100, 200, 300, 400, 500]:
        for i in range(100):
            # n = int(input("Enter the number of locations: "))
            # mean = float(input("Enter the mean: "))
            # sigma = float(input("Enter the standard deviation: "))
            n = N
            mean = 2*N
            sigma = mean/4

            write_distance_matrix(n, mean, sigma, i)
