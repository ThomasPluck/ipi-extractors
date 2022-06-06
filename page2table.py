from tabula import read_pdf
import pandas as pd

def partition_on_word(dfs,word):
    clip = dfs.iloc[:,0].where(dfs.iloc[:,0].str.contains(word)).first_valid_index()

    if clip == None:
        return dfs

    return dfs.loc[clip+1:]

def read_table(rel_loc,page_num,incl_bool=True):

    dfs = read_pdf(rel_loc,pages = page_num)

    dfs = dfs[0].loc[~dfs[0].iloc[:,-1].str.contains("%").fillna(True)]

    for w in ["Unweighted Total","UNWTD"]:
        dfs = partition_on_word(dfs,w)

    # For simpler code, reset indices and columns
    dfs = dfs.reset_index(drop=True)
    dfs = dfs.T.reset_index(drop=True).T

    # Number of columns + indexing dictionary
    l = len(dfs.T)
    rem_map = {}

    n = 1

    # Iterate over columns
    for i in range(1,l):
        # Look for spaces in column entries
        if dfs[i].str.contains(' ').any():
            # Split and expand columns on spaces
            temp = dfs[i].str.split(' ', -1, expand=True)
            # Create a new rem_map entry
            rem_map.update({i:[]})

            # Create new columns for split rows
            for t in temp:

                dfs[l+n] = temp[t]
                # Remember what we named these split rows
                # and where they came from!
                rem_map[i].append(l+n)
                # Abandon original row
                dfs.drop(i,axis=1)

                # Update naming counter
                n += 1

    # Move split rows to inplace column
    if incl_bool:
        cols = [0]
    else:
        cols = []

    for i in range(1,l):
        if i in rem_map.keys():
            cols.append(rem_map[i])
        else:
            cols.append(i)

    # Flatten columns
    flatten = lambda *n: (e for a in n
        for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

    cols = flatten(cols)

    dfs = dfs[cols]

    dfs = dfs.T.reset_index(drop=True).T

    dfs[0] = dfs[0].str.split('(').str[0]

    if not incl_bool: dfs = dfs.iloc[:,1:]

    # Get list to clipboard
    dfs.to_clipboard(excel=True, index=False, header=None)

if __name__ == "__main__":
    while True:
        rel_loc = input("Enter relative path to PDF: ")
        while True:
            page_num = input("Enter table PDF page number: ")
            commaed = page_num.split(",")
            if page_num == "x":
                break
            elif len(commaed) > 1:
                if commaed[0].isdigit():
                    read_table(rel_loc,commaed[0],False)
            elif page_num.isdigit():
                read_table(rel_loc,page_num)
