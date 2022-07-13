from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('ship_cert', pkey='code', name_long='ship_cert', name_plural='ship_cert',caption_field='certificate',lookup=True)
        self.sysFields(tbl,id=False, counter=True)

        
        tbl.column('code',name_long='!![en]Code')
        tbl.column('certificate', name_short='!![en]Certificate')

    @metadata(mandatory=True)
    def sysRecord_safetypass(self):
        return self.newrecord(code='01_safetypass', certificate='Passenger ship safety certificate')
    
    @metadata(mandatory=True)
    def sysRecord_safetycostr(self):
        return self.newrecord(code='02_safetycostr',certificate='Cargo ship safety construction certificate')
    
    @metadata(mandatory=True)
    def sysRecord_safetyequip(self):
        return self.newrecord(code='03_safetyequip',certificate='Cargo ship safety equipment certificate')
    
    @metadata(mandatory=True)
    def sysRecord_rtf(self):
        return self.newrecord(code='04_safetyrtf',certificate='Cargo ship safety RT/RF certificate')
    
    @metadata(mandatory=True)
    def sysRecord_loadline(self):
        return self.newrecord(code='05_loadline',certificate='Load line certificate')

    @metadata(mandatory=True)
    def sysRecord_sanitation(self):
        return self.newrecord(code='06_sanitation',certificate='Sanitation control exemption')
    
    @metadata(mandatory=True)
    def sysRecord_rorohsc(self):
        return self.newrecord(code='07_rorohsc',certificate='If Ship is regular RoRo ferry or HSC passenger service:')
    
    @metadata(mandatory=True)
    def sysRecord_issc(self):
        return self.newrecord(code='07_issc',certificate='ISSC (International Ship Security Certification - ISPS Code)')

    @metadata(mandatory=True)
    def sysRecord_doc(self):
        return self.newrecord(code='08_doc',certificate='D.O.C. (Document of Compliance)')

    @metadata(mandatory=True)
    def sysRecord_smc(self):
        return self.newrecord(code='09_smc',certificate='S.M.C. (Safety Managment Certificate)')

    @metadata(mandatory=True)
    def sysRecord_iopp(self):
        return self.newrecord(code='10_iopp',certificate='I.O.P.P. (International oil preventiion pollution)')

    @metadata(mandatory=True)
    def sysRecord_ispp(self):
        return self.newrecord(code='11_ispp',certificate='I.S.P.P. (International Sewage Pollution Prevention)')

    @metadata(mandatory=True)
    def sysRecord_psc(self):
        return self.newrecord(code='12_psc',certificate='P.S.C. (Port State Control)')

    @metadata(mandatory=True)
    def sysRecord_msm(self):
        return self.newrecord(code='13_msm',certificate='Minimum  Safe Manning Document')

    @metadata(mandatory=True)
    def sysRecord_mlc2006(self):
        return self.newrecord(code='14_mlc2006',certificate='MLC 2006 - Maritime Labour Certificate')

    @metadata(mandatory=True)
    def sysRecord_class(self):
        return self.newrecord(code='15_class',certificate='Certficato di classe/navigabilità')

    @metadata(mandatory=True)
    def sysRecord_idoneita(self):
        return self.newrecord(code='16_ido_sic',certificate='Certificato di idoneità/annotazioni di sicurezza')

    @metadata(mandatory=True)
    def sysRecord_tecsan(self):
        return self.newrecord(code='17_tecnosan',certificate='Visita tecnico/sanitaria')

    @metadata(mandatory=True)
    def sysRecord_servbordo(self):
        return self.newrecord(code='18_servbordo',certificate='Visità servizi di bordo')

    @metadata(mandatory=True)
    def sysRecord_assicurazione(self):
        return self.newrecord(code='19_ass',certificate='Assicurazione equipaggio')

    @metadata(mandatory=True)
    def sysRecord_ruolo(self):
        return self.newrecord(code='20_ruolo',certificate='Ruolo equipaggio')
    
    @metadata(mandatory=True)
    def sysRecord_ta(self):
        return self.newrecord(code='21_ta',certificate='Tassa ancoraggio')
    
    @metadata(mandatory=True)
    def sysRecord_sta(self):
        return self.newrecord(code='22_sta',certificate='Sopratassa ancoraggio')