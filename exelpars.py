import pyexcel

my_array = pyexcel.get_array(file_name="data3.xlsx")
databut, *datasort = my_array
dicsort = {s1:[*map(int, s2)]for s1, *s2 in datasort}
#sortament = dicsort.keys()

#print(dicsort)
