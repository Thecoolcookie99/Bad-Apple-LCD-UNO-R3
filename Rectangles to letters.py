import string

def process_rectangles(input_file='rectangles.txt', output_file='encoded_rectangles.txt'):
    letters = string.ascii_lowercase  # a to z
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    encoded_parts = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        
        parts = line.split()
        if len(parts) != 5:
            print(f"Skipping invalid line: {line}")
            continue
        
        try:
            x1 = int(parts[0])
            y1 = int(parts[1])
            x2 = int(parts[2])
            y2 = int(parts[3])
            color = int(parts[4])
        except ValueError:
            print(f"Skipping line with invalid numbers: {line}")
            continue
        
        # Apply color rule for x coordinates
        if color == 1:
            # x1 should be bigger than x2
            if x1 < x2:
                x1, x2 = x2, x1
        elif color == 0:
            # x1 should be smaller than x2
            if x1 > x2:
                x1, x2 = x2, x1
        
        # Convert to letter (add 1)
        def to_letter(n):
            val = n + 1
            if 1 <= val <= 26:
                return letters[val - 1]
            else:
                raise ValueError(f"Value {val} out of a-z range")
        
        try:
            lx1 = to_letter(x1)
            ly1 = to_letter(y1)
            lx2 = to_letter(x2)
            ly2 = to_letter(y2)
        except ValueError as e:
            print(f"Error: {e} in line: {line}")
            continue
        
        # Add the 4 letters
        encoded_parts.append(lx1 + ly1 + lx2 + ly2)
    
    # Join everything into ONE single string with no spaces and no line breaks
    final_string = ''.join(encoded_parts)
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(final_string)
    
    print(f"Processed {len(encoded_parts)} rectangles.")
    print(f"Total encoded length: {len(final_string)} characters")
    print(f"Output written to {output_file} (single line, no breaks)")
    
    # Show first 100 characters for verification
    print("\nPreview (first 100 chars):")
    print(final_string[:100] + ("..." if len(final_string) > 100 else ""))


if __name__ == "__main__":
    process_rectangles()