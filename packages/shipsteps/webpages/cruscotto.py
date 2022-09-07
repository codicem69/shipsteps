from gnr.core.gnrdecorator import public_method, customizable
from gnr.core.gnrbag import Bag

class GnrCustomWebPage(object):

    py_requires = """public:Public,th/th:TableHandler"""

    maintable = 'shipsteps.arrival'

    def windowTitle(self,**kwargs):
        return 'Cruscotto Arrival'

    def main(self, root,**kwargs):
        rootframe = root.framePane(datapath='main',design='sidebar')
        rootframe.top.slotToolbar('*,stackButtons,*')
        tc = rootframe.center.stackContainer(margin='2px')

        self.shiprec(tc.contentPane(title='!![en]Shippers/Receivers',datapath='.shiprec',
                                                overflow='hidden'))
        self.charterers(tc.contentPane(title='!![en]Charterers',datapath='.charterers',
                                                overflow='hidden',_onStart=True))
        self.cons_notify(tc.contentPane(title='!![en]Consigne/Notify',datapath='.consnotify',
                                                overflow='hidden',_onStart=True))                                                

    def charterers(self,pane):
        pane.iframe(src='/sys/thpage/shipsteps/charterers',
                    src_th_viewResource='View',
                    height='100%',width='100%',border=0)

    def shiprec(self,pane):
        pane.iframe(src='/sys/thpage/shipsteps/ship_rec',
                    src_th_viewResource='View',
                    height='100%',width='100%',border=0)

    def cons_notify(self,pane):
        pane.iframe(src='/sys/thpage/shipsteps/consignee',
                    src_th_viewResource='View',
                    height='100%',width='100%',border=0)
