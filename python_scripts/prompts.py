# Author: Zachery Linscott

# Purpose: provide user prompts throughout program execution.

# For asking the user what mean of means of all the sequences in all the files the user 
# would like to use to chop all sequences that ultimately get passed into the CNN.
def user_prompt(mean_of_means, mean_lst):
        print(f"The mean of all the means of the positive and negative files is {mean_of_means}.")
        mean_lst = ", ".join([str(mean) for mean in mean_lst])
        print(f"The list of the original means is: {mean_lst}")
        user_in = input("Would you like to use the mean of the means (1) or choose your own val? (2): ")
        while True:
                if user_in == "1":
                        trim_val = mean_of_means
                        break
                elif user_in == "2":
                        trim_val = int(input("Enter the custom value to use (ideally one of the already existing means or greater than 200): ")) 
                        break
                else:
                        "Errrrrrrm... that wasn't an option. Try again pal."
        return trim_val


# print loading bar
def print_progress(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', print_end = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = print_end)
    if iteration == total: 
        print("\n")