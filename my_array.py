import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Generate a random array of integers between 0 and 9
ARRAY_LENGTH = 15
MY_ARRAY = [random.randint(0, 9) for _ in range(ARRAY_LENGTH)]


def myBlocks(arr: list[int]) -> list[list[int] | list[str]]:
	separated_lists = []

	for _ in range(arr.count(0) + 1):
		try:
			# Find the index of the first zero in the array
			zero_index = arr.index(0)
		except ValueError:
			# If no zero is found, treat the rest of the array as a single block
			zero_index = len(arr)
		# Append the sorted sub-array before the zero, or "X" if empty
		separated_lists.append(sorted(arr[:zero_index]) if arr[:zero_index] else ["X"])
		# Remove the processed part of the array
		arr = arr[zero_index + 1 :]

	return " ".join("".join(map(str, lst)) for lst in separated_lists)


logging.info("Generated Array: %s", MY_ARRAY)
logging.info("Blocks: %s", myBlocks(MY_ARRAY))
