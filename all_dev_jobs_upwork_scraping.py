# LOOP 1: Web Dev subcategory by    
data_1 = []

for i in pages:
    for j in client_hires:
        params = {'q': 'development', 'paging': i, 'category2': 'Web, Mobile & Software Dev',
              'subcategory2': 'Web Development', 'client_hires': j}
        data = search.Api(client).find(params) 
        for z in data['jobs']: 
            data_1.append(z)
            
df_1 = pd.DataFrame(data_1)
