# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        shipsteps = root.branch(u"shipsteps", tags="")
        shipsteps.thpage(u"!![en]Task list", table="shipsteps.tasklist", tags="")
        shipsteps.thpage(u"!![en]Operations SOF", table="shipsteps.sof_operations", tags="")
        shipsteps.thpage(u"email_sof", table="shipsteps.email_sof", tags="")
        shipsteps.thpage(u"sof", table="shipsteps.sof", tags="")
        shipsteps.thpage(u"sof_cargo", table="shipsteps.sof_cargo", tags="")
        shipsteps.thpage(u"!![en]Invoice details", table="shipsteps.invoice_det", tags="")
        shipsteps.thpage(u"Sof tanks", table="shipsteps.sof_tanks", tags="")
        shipsteps.thpage(u"!![en]Services emails", table="shipsteps.email_services", tags="")
        shipsteps.thpage(u"!![en]Cargoes unloding/loading", table="shipsteps.cargo_unl_load", tags="")
        shipsteps.thpage(u"!![en]arrival times", table="shipsteps.arrival_time", tags="")
        shipsteps.thpage(u"Shippers-Receivers", table="shipsteps.ship_rec", tags="")
        shipsteps.thpage(u"!![en]Agencies", table="shipsteps.agency", tags="")
        shipsteps.thpage(u"!![en]Staff", table="shipsteps.staff", tags="")
        shipsteps.thpage(u"Shipdocs", table="shipsteps.shipdoc", tags="")
        shipsteps.thpage(u"GPG", table="shipsteps.gpg", tags="")
        shipsteps.thpage(u"!![en]Arrival details", table="shipsteps.arrival_det", tags="")
        shipsteps.thpage(u"email_arr", table="shipsteps.email_arr", tags="")
        shipsteps.thpage(u"!![en]Vessel details", table="shipsteps.vessel_details", tags="")
        shipsteps.thpage(u"!![en]Owners", table="shipsteps.owner", tags="")
        shipsteps.thpage(u"!![en]Arrivals", table="shipsteps.arrival", tags="")
        shipsteps.thpage(u"!![en]Garbage form", table="shipsteps.garbage", tags="")
        shipsteps.thpage(u"!![en]Charterers", table="shipsteps.charterers", tags="")
        shipsteps.thpage(u"!![en]Bulk application", table="shipsteps.rinfusa", tags="")
        shipsteps.thpage(u"!![en]Bunker", table="shipsteps.bunker", tags="")
        shipsteps.thpage(u"!![en]Shorepass", table="shipsteps.shorepass", tags="")
        shipsteps.thpage(u"!![en]Shorepass righe", table="shipsteps.shorepass_righe", tags="")
        shipsteps.thpage(u"!![en]Vessel services", table="shipsteps.vessel_services", tags="")
        shipsteps.thpage(u"!![en]ExtradataCP", table="shipsteps.extradaticp", tags="")
        shipsteps.lookups(u"Lookup tables", lookup_manager="shipsteps")
        ultimi_arrivi = shipsteps.branch('!!Ultimi arrivi')
        self.ultimi_arr(ultimi_arrivi)

       # pfda = root.branch(u"pfda", tags="")
       # pfda.thpage(u"!![en]Proforma", table="pfda.proforma", tags="")
       # shipsteps.packageBranch('Gestione utenti',pkg='adm',
        #                      branchMethod='userSubmenu',
        #                      branch_parametro=3)
    def ultimi_arr(self, ultimi_arrivi, **kwargs):
        ultimi_arrivi.thpage(u"Sof", table="shipsteps.sof", tags="")
        ua=ultimi_arrivi.tableBranch('Ultimi arrivi',table='shipsteps.arrival',
                              query_limit=5,
                              query_order_by='$reference_num',
                              branchId='prova',
                              cacheTime=5)


