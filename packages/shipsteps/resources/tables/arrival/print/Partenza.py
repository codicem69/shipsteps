from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Comunicazione Partenza'

class Main(BaseResourcePrint):
    batch_title = 'Comunicazione Partenza'
    html_res = 'html_res/partenza'
    batch_immediate = 'print'

