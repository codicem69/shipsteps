# preference.py
class AppPref(object):

    def prefpane_shipsteps(self,parent,**kwargs):
        pane = parent.contentPane(**kwargs)
        fb = pane.formbuilder()

        # Nei **kwargs c'è già il livello di path dati corretto
        fb.div('', width='60em')
        fb.simpleTextArea('^.remarks_wheat_corn',lbl='Remarks wheat/corn',width='60em', height='100px',editor=True)
        fb.img(src='^.logo_cc',lbl='Logo CC',
                    border='2px dotted silver',
                    crop_width='250px',
                    crop_height='371px',
                    edit=True,
                    placeholder=True,
                    upload_filename='logo_cc',
                    upload_folder='site:image')
        fb.img(src='^.logo_cp',lbl='Logo CP',
                    border='2px dotted silver',
                    crop_width='100px',
                    crop_height='100px',
                    edit=True,
                    placeholder=True,
                    upload_filename='logo_cc',
                    upload_folder='site:image')
