# preference.py
from gnr.app.gnrapp import GnrApp
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from gnr.app.gnrdeploy import ProjectMaker, InstanceMaker, SiteMaker,PackageMaker, PathResolver,ThPackageResourceMaker
import os

class AppPref(object):

    def permission_shipsteps(self, **kwargs):
        return 'user'
        
    def prefpane_shipsteps(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.note_remarks(tc.borderContainer(title='!!Remarks'))
        #self.loghi(tc.borderContainer(title='!!Logos'))
        self.privacy(tc.borderContainer(title='!!Email Privacy'))
        self.extra(tc.borderContainer(title='!!Extra'))

    def note_remarks(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
       # bc = pane.borderContainer(region='center', margin='10px')
        fb = pane.formbuilder(cols=1)
        #fb = bc.contentPane(region='top',height='150px').formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='60em')
        fb.simpleTextArea('^.remarks_wheat_corn',lbl='Remarks wheat/corn',width='60em', height='100px',editor=True)
        fb.div("""Inserire testo remark ricevitore con le variabili ${tot_mov} per totale sbarcato e ${shortage} per ammanco:<br><br>
                    TTL CARGO UNLOADED AS PER SHORE SCALE TONS ${tot_mov} WITH A SHORTAGE AGAINST THE B/L FIGURE OF TONS ${shortage}""")
        #grid = bc.contentPane(region='center').quickGrid(value='^.remarks')
        #grid.tools('delrow,addrow,export')
        #grid.column('code', width='30em', name='!![en]Code', edit=True)
        #grid.column('description', width='60em', name='!![en]Description', edit=True)
    #def loghi(self,pane):  
    #    fb = pane.formbuilder(cols=1)    
    #    fb.img(src='^.logo_cc',lbl='Logo CC',
    #                border='2px dotted silver',
    #                crop_width='250px',
    #                crop_height='371px',
    #                edit=True,
    #                placeholder=True,
    #                upload_filename='logo_cc',
    #                upload_folder='site:image')
    #    fb.img(src='^.logo_cp',lbl='Logo CP',
    #                border='2px dotted silver',
    #                crop_width='100px',
    #                crop_height='100px',
    #                edit=True,
    #                placeholder=True,
    #                upload_filename='logo_cc',
    #                upload_folder='site:image')

    def privacy(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
        fb = pane.formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='100em')
        fb.simpleTextArea('^.privacy_email',lbl='Email Privacy',width='100em', height='200px',editor=True)
    
    def extra(self,pane):
        fb = pane.formbuilder(cols=2)
        fb.checkbox('^.ue',lbl='Disabilita paesi UE per pratiche Sanimare', default=False)
        fb.br()
        fb.checkbox('^.pmou',lbl='Disabilita invio PMOU notification', default=False)
        fb.checkbox('^.garbage_adsp',lbl='Disabilita invio Garbage ADSP', default=False)
        fb.checkbox('^.rifiuti_cp',lbl='Disabilita invio ricevuta rifiuti CP', default=False)
        fb.checkbox('^.gdf_dep',lbl='Disabilita stampa GDF partenza', default=False)
        fb.checkbox('^.ref_num', lbl='Disabilita Reference number', default=True)
        fb.checkbox('^.email_tributi_cp', lbl='Disabilita email tributi CP', default=True)
        fb.checkbox('^.nsw_cp', lbl='Disabilita sistema NSW CP', default=True)
        fb.checkbox(value='^.delrow_arr', lbl='!![en]Enable Delrow bottom on arrival')
        fb.br()
        fb.div('!![en]<strong>Times for shorepass</strong>')
        fb.br()
        fb.timeTextBox('^.start',lbl='!![en]Start time')
        fb.timeTextBox('^.end',lbl='!![en]End time') 
        #fb.textbox(value='^.project_name',validate_onAccept='SET .package_name=null;',validate_onReject='SET .package_name = null;',
        #            validate_notnull=True,
        #            validate_remote=self.getProjectPath,lbl='Project')
        #fb.filteringSelect(value='^.package_name',lbl='Package',validate_notnull=True,
        #            values='^.packages',width='7em')
        #fb.checkbox('^.carte_cred',lbl='Visualizza carte dal pkg carte')
        #fb.dataRpc('.package_name',self.getProjectPath,value='cart',carte_c='^.carte_cred',_if='carte_c')
        #fb.dataRpc('.result_carte',self.packageName,package_name='^.package_name.data.packages',_if='package_name')
        #fb.dataController("""if(msg=='Not existing project'){alert(msg);}""",msg='^.package_name.errorcode')
        #fb.button('test',action="alert('ciao');")
        #fb.filteringSelect('^.carta',lbl='Seleziona la carta di addebito',values='^.result_carte')
        #print(x)

    #@public_method
    #def packageName(self,package_name=None,**kwargs):
    #    myapp = GnrApp(package_name)
    #    mydb = myapp.db
    #
    #    if package_name=='carte':
    #        tbl_carte = mydb.table('carte.carta')
    #        carte = tbl_carte.query(columns="$descr_carta,$num_carta",
    #                where='').fetch()
    #        valori_carte=[]
    #        for r in carte:
    #                valori_carte.append(r['num_carta']+':'+r['descr_carta'])
    #        result_carte = ",".join(valori_carte)
    #        return result_carte
    #    else:
    #        return 'Error'
    #
    #
    #@public_method
    #def getProjectPath(self,value=None,**kwargs):
    #    p = PathResolver()
    #    data = Bag()
    #    #print(x)
    #    try:
    #        path = p.project_name_to_path(value)
    #        instances_path = os.path.join(path,'instances')
    #        packages_path = os.path.join(path,'packages')
    #        if os.path.exists(instances_path):
    #            instances = [l for l in os.listdir(instances_path) if os.path.isdir(os.path.join(instances_path,l))]
    #        else:
    #            instances = []
    #        packages = [l for l in os.listdir(packages_path) if os.path.isdir(os.path.join(packages_path,l))]
    #        data['instances'] = ','.join(instances) if instances else None
    #        data['packages'] =','.join(packages) if packages else None
    #        data['instance_name'] = instances[0] if instances else None
    #        return Bag(dict(errorcode=None,data=data))
    #    except Exception:
    #        #return Bag(dict(errorcode=None,data='error'))
    #        return Bag(dict(errorcode='Not existing project',data=data))

#class UserPref(object):
#    def prefpane_shipsteps(self, parent, **kwargs):
#        pane = parent.contentPane(**kwargs)
#        fb = pane.formbuilder(cols=1, border_spacing='3px',datapath='.arrivi')
#        fb.checkbox(value='^.delrow_arr', lbl='!![en]Enable Delrow bottom on arrival')

