from read_in_establishments import read_establishments_as_list, create_search_links

excel_file = input("Enter excel file here: ")
establishments_list = read_establishments_as_list(excel_file)
print(create_search_links(establishments_list[1]))

