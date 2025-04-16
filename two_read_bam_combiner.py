import sys
import subprocess

def dec2bin(num):
    return bin(num)[2:].zfill(32)

def bin2dec(bin_str):
    return int(bin_str, 2)

def main():
    if len(sys.argv) < 5:
        sys.exit("Usage: python three_read_bam_combiner.py <read 1 bam> <read 2 bam> <path to samtools> <minimum map quality filter>")

    read1_bam = sys.argv[1]
    read2_bam = sys.argv[2]
    samtools = sys.argv[3]
    mq = int(sys.argv[4])

    # Open samtools to view both BAM files
    file1 = subprocess.Popen(f"{samtools} view -h {read1_bam}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    file2 = subprocess.Popen(f"{samtools} view -h {read2_bam}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    line1 = file1.stdout.readline().decode('utf-8')
    line2 = file2.stdout.readline().decode('utf-8')

    counter = 0
    new_counter = 0

    while line1:
        # If it's a header line starting with @SQ, ensure that headers match
        if line1.startswith("@SQ"):
            if line1 != line2:
                print(line1, end="")
                print(line2, end="")
                sys.exit("Inconsistent BAM headers. BAM files must be aligned to the same reference.")
            else:
                print(line1, end="")
            line1 = file1.stdout.readline().decode('utf-8')
            line2 = file2.stdout.readline().decode('utf-8')
            continue

        counter += 1
        if counter == new_counter + 1000000:
            print(counter, file=sys.stderr)
            new_counter = counter

        line1 = line1.strip()
        line2 = line2.strip()

        # Split the lines into fields
        fields1 = line1.split("\t")
        fields2 = line2.split("\t")

        id1, flag1, chr_from1, loc_from1, mapq1, cigar1, d1_1, d2_1, d3_1, read1, read_qual1, *rest1 = fields1
        id2, flag2, chr_from2, loc_from2, mapq2, cigar2, d1_2, d2_2, d3_2, read2, read_qual2, *rest2 = fields2

        if id1 != id2:
            sys.exit(f"The read ids of the two files do not match up at line number {counter}. Files should be from the same sample and sorted in identical order.")

        # Convert flags to binary
        bin1 = dec2bin(int(flag1))
        bin2 = dec2bin(int(flag2))

        binary1 = list(bin1)
        binary2 = list(bin2)

        trouble = False
        if binary1[2] == '1' or int(mapq1) < mq:
            trouble = True
        if binary2[2] == '1' or int(mapq2) < mq:
            trouble = True

        proper_pair1 = 0
        proper_pair2 = 0
        dist1 = 0
        dist2 = 0

        if binary1[2] == '0' and binary2[2] == '0':
            proper_pair1 = 1
            proper_pair2 = 1
            if chr_from1 == chr_from2:
                dist = abs(int(loc_from1) - int(loc_from2))
                if int(loc_from1) >= int(loc_from2):
                    dist1 = -dist
                    dist2 = dist
                else:
                    dist1 = dist
                    dist2 = -dist
            else:
                dist1 = 0
                dist2 = 0
        else:
            proper_pair1 = 0
            proper_pair2 = 0
            dist1 = 0
            dist2 = 0

        new_bin1 = "0" * 21 + binary1[10] + binary1[9] + "001" + binary2[4] + binary1[4] + binary2[2] + binary1[2] + str(proper_pair1) + "1"
        new_bin2 = "0" * 21 + binary2[10] + binary2[9] + "010" + binary1[4] + binary2[4] + binary1[2] + binary2[2] + str(proper_pair2) + "1"

        new_flag1 = bin2dec(new_bin1)
        new_flag2 = bin2dec(new_bin2)

        if not trouble:
            print("\t".join([id1, str(new_flag1), chr_from1, loc_from1, mapq1, cigar1, chr_from2, loc_from2, str(dist1), read1, read_qual1] + rest1))
            print("\t".join([id2, str(new_flag2), chr_from2, loc_from2, mapq2, cigar2, chr_from1, loc_from1, str(dist2), read2, read_qual2] + rest2))

        line1 = file1.stdout.readline().decode('utf-8')
        line2 = file2.stdout.readline().decode('utf-8')

if __name__ == "__main__":
    main()
