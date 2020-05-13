import booleanRetrieval as br

queries = ['cristina lopes', 'machine learning', 'acm', 'master of software engineering']
mode = 'and'
ii_folder = 'inverted_indx_0513'
doc_id_file = 'docId_url_dict/idUrl0513'
report_file = 'reports/m2_0513'

with open(report_file, 'w') as report:
    for query in queries:
        report.write('Query: {}\n'.format(query))
        report.write('Method: Boolean Retrieval(AND)\n')
        urls = br.booleanRetrieval(query, mode, ii_folder, doc_id_file)[:5]
        for i in range(5):
            report.write('  {}: {}\n'.format(i + 1, urls[i]))
        

