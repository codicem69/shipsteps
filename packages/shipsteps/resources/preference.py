# preference.py
class AppPref(object):

    def prefpane_shipsteps(self,parent,**kwargs):
        pane = parent.contentPane(**kwargs)
        fb = pane.formbuilder()

        # Nei **kwargs c'è già il livello di path dati corretto
        fb.div('', width='60em')
        fb.simpleTextArea('^.remarks_wheat_corn',lbl='Remarks wheat/corn',width='60em', height='100px',editor=True)
