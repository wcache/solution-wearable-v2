from tabulate import tabulate

mydata4 = [
    ['Head octes', 'Tag octes', 'value Length octes', 'Value octes', "CRC octes"]
]

head4 = ["H", "T", "L", "V", "C"]

print(tabulate(mydata4, headers=head4, tablefmt="grid"))
