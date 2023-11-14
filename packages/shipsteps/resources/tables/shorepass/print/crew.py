from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'CrewList'

class Main(BaseResourcePrint):
    batch_title = 'CrewList'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/crew_list'
    #Questo parametro indica la risorsa di stampa da utilizzare
    
