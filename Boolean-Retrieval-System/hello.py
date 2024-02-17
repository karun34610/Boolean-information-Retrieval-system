def edit_distance(query):
    """Function to perform edit distance on a query"""
    query=query[0:-1]
    mn=1000000000000000000000
    min_ref=""
    m=len(query)
    for ref in key_list:
        ref=ref[0:-1]
        n=len(ref)
        t = [[0 for x in range(n+1)] for y in range(m+1)]
        
        for i in range(m+1):
            t[i][0]=i
        for i in range(n+1):
            t[0][i]=i

        cost=0
        for i in range(1,m+1):
            for j in range(1,n+1):
                if query[i-1]==ref[j-1]:
                    cost=0
                else:
                    cost=1
                t[i][j]=min(min(t[i - 1][j] + 1,t[i][j - 1] + 1),t[i - 1][j - 1] + cost)

        if t[m][n]<mn:
            mn=t[m][n]
            min_ref=ref

        elif t[m][n]==mn:
            if len(inverted_index[min_ref+"$"])<len(inverted_index[ref+"$"]):
                min_ref=ref
    return inverted_index[min_ref+"$"],min_ref