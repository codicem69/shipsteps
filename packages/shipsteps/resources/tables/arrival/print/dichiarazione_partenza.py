from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify
from datetime import datetime
import string
from gnr.core.gnrdecorator import public_method
import os
#from gnr.core.gnrlang import GnrException

caption = 'Dich.integrativa Partenza CP'

class Main(BaseResourcePrint):
    batch_title = 'Dich.integrativa Partenza CP'
    html_res = 'html_res/nota_partenza_cp'
    batch_immediate = 'print'
    batch_thermo_lines = 'batch_steps,batch_main,ts_loop'
    virtual_columns = "@agency_id.fullstyle"
    py_requires = """gnrcomponents/drop_uploader"""
    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=2,border_spacing='3px')

        fb.textbox(value='^.car_deck', lbl='!![en]Cargo on deck',default='NIL',validate_notnull=True, colspan=2,width='36em')
        #fb.textbox(value='^.pax_imb', lbl='!![en]Passengers embarked',default='0',validate_notnull=True)
        fb.textbox(value='^.hazmat', lbl='HAZMAT',default='NIL',validate_notnull=True)
        fb.dateTextBox(value='^.data_att', lbl='Data doc.',default=self.db.workdate, validate_notnull=True)
        fb.br()
        fb.div('Timbro Nave')
        fb.br()
        fb.textbox(value='^.vess_stamp', validate_notnull=True, hidden=True)
        fb.div(border='2px dotted silver', width='150px', height='150px').img(
                    src='^.vess_stamp',
                    crop_width='150px',
                    crop_height='150px',
                    edit=True,
                    placeholder=True,
                    upload_filename='timbro_nave',
                    upload_folder='site:image')


