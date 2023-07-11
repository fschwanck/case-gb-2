
from functions.vendas import BaseTable

import functions_framework

@functions_framework.http
def functions(request):
    if request.method != 'POST':
        raise ValueError(f'Cloud Function received {request.method} but accepts only POST')
    else:
        try:
            bucket = request.args.get('bucket').lower()
            file = request.args.get('file').lower()
            projectId = request.args.get('projectId').lower()
            datasetId = request.args.get('datasetId').lower()
            tableId = request.args.get('tableId').lower()
            
        except Exception as e:
            raise ValueError(f"Parâmetros inválidos: {e}")
    
    return BaseTable(projectId,datasetId,tableId, bucket, file).run()
    
        


