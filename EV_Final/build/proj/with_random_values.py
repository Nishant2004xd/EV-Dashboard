def sum_of_ap(first_term, num_of_terms, common_diff):
    series = []
    total_sum = 0
    
    # Generate the series and calculate the sum
    for i in range(num_of_terms):
        term = first_term + i * common_diff
        series.append(term)
        total_sum += term
    
    # Print the series
    print("AP Series: ", ' '.join(map(str, series)))
    
    # Print the sum
    print(f"Sum: {total_sum}")

# Input format: first term, number of terms, common difference
first_term, num_of_terms, common_diff = map(int, input().split())

# Call the function to calculate and print the AP series and its sum
sum_of_ap(first_term, num_of_terms, common_diff)
