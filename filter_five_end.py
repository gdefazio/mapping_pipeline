import sys

def dec2bin(num):
    return bin(num)[2:].zfill(32)

def bin2dec(bin_str):
    return int(bin_str, 2)

def main():
    prev_id = ""
    five = []
    three = []
    unmap = []
    mid = []
    all_reads = []
    counter = 0

    for line in sys.stdin:
        line = line.strip()
        
        if line.startswith("@"):
            print(line)
            continue
        
        # Split the line by tab character
        fields = line.split("\t")
        id1, flag1, chr_from1, loc_from1, mapq1, cigar1, d1_1, d2_1, d3_1, read1, read_qual1, *rest1 = fields

        # Convert flag to binary
        bin1 = dec2bin(int(flag1))
        binary1 = list(bin1)

        if prev_id != id1 and prev_id != "":
            # Process previous read
            if counter == 1:
                if len(five) == 1:
                    print(five[0])
                else:
                    fields1 = all_reads[0].split("\t")
                    id_1, flag_1, chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1, *rest_1 = fields1
                    bin_1 = dec2bin(int(flag_1))
                    binary_1 = list(bin_1)
                    binary_1[2] = '1'  # Set the proper pair flag to 1
                    bin_1_new = "".join(binary_1)
                    flag_1_new = bin2dec(bin_1_new)
                    print("\t".join([id_1, str(flag_1_new), chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1] + rest_1))
            elif counter == 2 and len(five) == 1:
                print(five[0])
            else:
                fields1 = all_reads[0].split("\t")
                id_1, flag_1, chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1, *rest_1 = fields1
                bin_1 = dec2bin(int(flag_1))
                binary_1 = list(bin_1)
                binary_1[2] = '1'  # Set the proper pair flag to 1
                bin_1_new = "".join(binary_1)
                flag_1_new = bin2dec(bin_1_new)
                print("\t".join([id_1, str(flag_1_new), chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1] + rest_1))

            counter = 0
            unmap.clear()
            five.clear()
            three.clear()
            mid.clear()
            all_reads.clear()

        counter += 1
        prev_id = id1
        all_reads.append(line)

        if binary1[2] == '1':
            unmap.append(line)
        elif (binary1[4] == '0' and cigar1.startswith('M')) or (binary1[4] == '1' and cigar1.endswith('M')):
            five.append(line)
        elif (binary1[4] == '1' and cigar1.startswith('M')) or (binary1[4] == '0' and cigar1.endswith('M')):
            three.append(line)
        elif 'M' in cigar1 and any(x in cigar1 for x in ['H', 'S']):
            mid.append(line)

    # Final check for remaining lines
    if counter == 1:
        if len(five) == 1:
            print(five[0])
        else:
            fields1 = all_reads[0].split("\t")
            id_1, flag_1, chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1, *rest_1 = fields1
            bin_1 = dec2bin(int(flag_1))
            binary_1 = list(bin_1)
            binary_1[2] = '1'  # Set the proper pair flag to 1
            bin_1_new = "".join(binary_1)
            flag_1_new = bin2dec(bin_1_new)
            print("\t".join([id_1, str(flag_1_new), chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1] + rest_1))
    elif counter == 2 and len(five) == 1:
        print(five[0])
    else:
        fields1 = all_reads[0].split("\t")
        id_1, flag_1, chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1, *rest_1 = fields1
        bin_1 = dec2bin(int(flag_1))
        binary_1 = list(bin_1)
        binary_1[2] = '1'  # Set the proper pair flag to 1
        bin_1_new = "".join(binary_1)
        flag_1_new = bin2dec(bin_1_new)
        print("\t".join([id_1, str(flag_1_new), chr_from_1, loc_from_1, mapq_1, cigar_1, d1_1, d2_1, d3_1, read_1, read_qual_1] + rest_1))

if __name__ == "__main__":
    main()
