from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify

caption = 'PMIS Documents'

class Main(BaseResourcePrint):
    batch_title = 'PMIS Documents'
    html_res = 'html_res/pmis_doc'
    batch_immediate = 'print'

