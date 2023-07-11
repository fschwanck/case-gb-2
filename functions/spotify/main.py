from functions.episodes import SpotifyEpisodes
from functions.search import SpotifySearch
import functions_framework

@functions_framework.http
def functions(request):
    if request.method != 'POST':
        raise ValueError(f'Cloud Function received {request.method} but accepts only POST')
    else:
        try:
            endpoint = request.args.get('endpoint').lower()
            projectId = request.args.get('projectId').lower()
            datasetId = request.args.get('datasetId').lower()
            tableId = request.args.get('tableId').lower()
        except Exception as e:
            raise ValueError(f"Parâmetros inválidos: {e}")
    
    if endpoint == 'search':
        return SpotifySearch(projectId,datasetId,tableId).run()
    elif endpoint == 'episodes':
        return SpotifyEpisodes(projectId,datasetId,tableId).run()
    else:
        raise ValueError(f"Parâmetro 'endpoint' incorreto")
        



