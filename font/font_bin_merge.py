from struct import *


def bin_create(*args):
    if len(args) < 1:
        print("wrong params number!")
        return -1

    with open("ext_font.bin","wb") as dest_file:
        # start
        start = "s"
        end = "e"

        font_num = len(args)
        bin_data = []
        bin_size = []
        font_name = ""

        for i in range(font_num):
            with open(args[i], "rb") as bin_file:
                data = bin_file.read()
            padding = "\0" * (128 - len(args[i]))
            string_padded = args[i] + padding
            font_name += string_padded
            bin_size.append(len(data))
            bin_data.append(data)

        write_data = pack("<B%ds%dI"% (font_num*128, font_num), font_num, font_name.encode(), *bin_size)

        dest_file.write(start.encode())
        dest_file.write(write_data)
        for i in range(font_num):
            dest_file.write(bin_data[i])
        dest_file.write(end.encode())


if __name__ == "__main__":
    bin_create("arial18.bin", 'arial27.bin', 'arial55.bin')
