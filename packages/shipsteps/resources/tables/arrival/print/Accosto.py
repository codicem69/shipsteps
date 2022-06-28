from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Domanda Accosto'

class Main(BaseResourcePrint):
    batch_title = 'Domanda Accosto'
    html_res = 'html_res/domanda_accosto'
    batch_immediate = 'print'

